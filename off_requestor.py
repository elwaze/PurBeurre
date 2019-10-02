#! /usr/bin env python3
# coding: utf-8

import requests

from purbeurre_models import Product, Category, Store, User


def sort_and_register_products(products, category_name):
    for i in (range(0, len(products) - 1)):
        for product in products[i]:
            url = product.get('url')
            name = product.get('product_name_fr')
            nutriscore = product.get('nutrition_grades')
            stores = product.get('stores')
            country = product.get('countries')
            if all([url, name, nutriscore, stores, country.lower().strip() == "france"]):
                # insert product in database
                options = {
                    "name": name,
                    "link": url,
                    "nutriscore": nutriscore,
                    "category": category_name,
                    "stores": [stores]
                }
                product = Product(**options)
                product.insert_into_db()


def get_products(category_name, url, products):
    products_ = []
    pages_count = 1
    needed_pages = products / 20
    # if we take too many pages, it's too long for demo
    if needed_pages > 3:
        needed_pages = 3
    while pages_count < needed_pages:
        # we request pages one by one
        request_products = requests.get(url + '&json=' + str(pages_count))
        products_json = request_products.json()
        products_.append(products_json.get('products'))
        pages_count += 1
        sort_and_register_products(products_, category_name)


def get_categories(data_tags):
    category_selected = 0
    for idx, data in enumerate(data_tags):
        name = data['name']
        products = data['products']
        # for a useful category, we want at least 100 products
        if products > 100:
            if ":" not in name and "-" not in name:
                category_registered = Category(name=name)
                category_registered.insert_into_db()
                # get products for this category
                get_products(name, data['url'], products)
                category_selected += 1

        if category_selected == 5:
            break


def off_requestor():
    # get categories from the OpenFoodFacts' API
    request_categories = requests.get('https://fr.openfoodfacts.org/categories&json=1')
    categories_json = request_categories.json()
    data_tags = categories_json.get('tags')
    # make some sorting and get products
    get_categories(data_tags)


if __name__ == "__main__":
    off_requestor()
