#! /usr/bin env python3
# coding: utf-8

"""
IHM module with the code used to run the entire program.
The main code is at the end of the file.

"""

from clint.textui import colored, puts, prompt, indent

from purbeurre_models import Product, Category, Store, User
import off_requestor


def hello():
    """
    Runing off requestor to request the api
    and register products in the database.
    Initiating dialog with user and registering its id in the database.

    :return user: user registered in the database.

    """

    # runs the requests to OFF
    # loads the OFF API data to database
    off_requestor.off_requestor()

    puts(colored.magenta("BONJOUR !"))

    # asks for user identification. Registers in db if new user.
    user_id = prompt.query(
        "Veuillez renseigner votre adresse e-mail afin d'être identifié : ")
    user = User(user_id)
    user.insert_into_db()

    return user


def user_choice():
    """
    Asks the user to choose to look in his favorites or search a new product.
    If the user enters a wrong choice, asks to choose again (recursively).

    :return response: 1 or 2.

    """

    puts(colored.blue("Voulez-vous : "))
    with indent(4):
        puts(colored.blue("1 : Retrouver vos aliments substitués"))
        puts(colored.blue("2 : Rechercher un nouvel aliment"))
    try:
        response = int(prompt.query(" "))
    except ValueError:
        puts(colored.red("Attention : vous devez obligatoirement "
                         "rentrer 1 ou 2 pour continuer."))
        return user_choice()
    else:
        # asking again in case of wrong choice
        choice_list = [1, 2]
        if response not in choice_list:
            puts(colored.red("Attention : vous devez obligatoirement "
                             "rentrer 1 ou 2 pour continuer."))
            return user_choice()
        else:
            return response


def new_search(user):
    """
    Does a new research.

    :param user: user previously registered. Used to register a favorite.

    """

    # asks the user to choose a category among the categories registered
    category = category_selection()
    category = Category(name=category)
    # asks the user to choose among products registered in this category
    product = product_selection(category=category)
    product = Product(link=product[1], name=product[0], nutriscore=product[2])
    # searches for a substitute
    substitute = Product.objects.get_better_products_by_category(category)
    substitute = substitute[0]
    substitute = Product(
        link=substitute["link"],
        name=substitute["name"],
        nutriscore=substitute["nutriscore"])
    substitute.stores = Store.objects.get_stores_by_product(substitute)
    substitute_proposal(substitute, product)

    save_product = [{'selector': 'o', 'prompt': 'oui', 'return': 1},
                    {'selector': 'n', 'prompt': 'non', 'return': 0}]
    favorite = prompt.options(
        "voulez-vous enregistrer ce produit dans vos favoris ? ", save_product)
    if favorite:
        User.objects.insert_favorite(user, product, substitute)


def favorites_search(user):
    """
    Searches for saved substituted products.

    :param user: user previously registered.
            Used to find his favorites in the database.

    """

    product = product_selection(user=user)
    product = Product(link=product[1], name=product[0], nutriscore=product[2])
    substitute = Product.objects.get_substitute(product)[0]
    substitute = Product(link=substitute["good_product_link"])
    substitute.stores = Store.objects.get_stores_by_product(substitute)
    substitute.name, substitute.nutriscore = Product.objects.get_prod_info(
        substitute)[0]
    substitute_proposal(substitute, product)


def category_selection():
    """
    Asks the user to choose in which category to look for a product.
    If the user enters a wrong choice, asks to choose again (recursively).

    :return categories[category_number]: chosen category.

    """

    puts(colored.green("Rentrez le numéro de la catégorie "
                       "choisie pour accéder aux produits : "))
    # getting categories from the database
    categories = []
    for element in Category.objects.get_categories():
        categories.append(element['name'])
    # asking the user to choose
    for i in range(len(categories)):
        with indent(4):
            puts(colored.blue(str(i + 1) + ' : ' + categories[i]))
    try:
        category_number = int(prompt.query(" "))
        category_number = category_number - 1
    except ValueError:
        # asking again in case of wrong choice
        puts(colored.red("Attention : vous devez rentrer un nombre"
                         " de la liste de catégories"))
        return category_selection()
    else:
        if category_number in range(len(categories)):
            return categories[category_number]
        else:
            # asking again in case of wrong choice
            puts(colored.red("Attention : vous devez rentrer un nombre"
                             " de la liste de catégories"))
            return category_selection()


def product_selection(category=None, user=0):
    """
    Asks the user to choose which product to compare.
    If user = 0, looks in the category's products.
    Else, looks in the user's favorites.
    If the user enters a wrong choice, asks to choose again (recursively).

    :param category: category where to find products.
    :param user: user where to look for favourite products.

    :return products[product_number]: chosen product.

    """

    puts(colored.green(
        "Rentrez le numéro du produit choisi pour accéder à un substitut : "))
    products = []
    # if user_id = 0, searching by category
    if user == 0:
        prods = Product.objects.get_products_by_category(category)
        for element in prods:
            products.append((
                element['name'], element['link'], element['nutriscore']))
    # else, searching in the favorite products of the user
    else:
        prods = list(Product.objects.get_products_by_user(user))
        for element in prods:
            product = Product(link=element["bad_product_link"])
            product.name, product.nutriscore = Product.objects.get_prod_info(
                product)[0]
            products.append((product.name, product.link, product.nutriscore))

    # asking the user to choose
    for i in range(len(products)):
        with indent(4):
            puts(colored.blue(str(i + 1) + ' : ' + products[i][0]))
    try:
        product_number = int(prompt.query(" "))
        product_number = product_number - 1
    except ValueError:
        # asking again in case of wrong choice
        puts(colored.red("Attention : vous devez rentrer un nombre "
                         "de la liste de produits"))
        return product_selection(category=category, user=user)
    else:
        if product_number in range(len(products)):
            return products[product_number]
        else:
            # asking again in case of wrong choice
            puts(colored.red("Attention : vous devez rentrer un nombre "
                             "de la liste de produits"))
            return product_selection(category=category, user=user)


def substitute_proposal(substitute, product):
    """
    Displays the substitute found and its information.

    :param substitute: substitute found.
    :param product: product to substitute.

    """
    if substitute.nutriscore == product.nutriscore:
        puts(colored.green("Nous n'avons pas trouvé de produit plus sain que "
                           "" + product.name + "."))
    else:
        puts(colored.green(
            "Nous vous proposons de consommer "
            "" + substitute.name + " à la place de " + product.name))
        puts(colored.green("Plus d'infos : "))
        with indent(4):
            puts(colored.green("Nutriscore : " + str(substitute.nutriscore)))
            puts(colored.green("Magasins où l'acheter : " + ', '.join(map(
                str, substitute.stores))))
            puts(colored.green(
                "Lien vers le descriptif OpenFoodFacts : " + substitute.link))


def main():
    """
    Main function running the code

    """

    user = hello()
    # starting while loop to run the app or quit
    while_quit = 0
    while while_quit == 0:

        # asks if the user wants to see it's favorites or search new products
        choice = user_choice()

        if choice == 2:
            new_search(user)
        else:
            favorites_search(user)

        # going out of while loop.
        quit_options = [{'selector': 'o', 'prompt': 'oui', 'return': 0},
                        {'selector': 'n', 'prompt': 'non', 'return': 1}]
        while_quit = prompt.options("Souhaitez-vous continuer ?", quit_options)


if __name__ == "__main__":
    main()
