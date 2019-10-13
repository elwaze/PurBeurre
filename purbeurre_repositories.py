#! /usr/bin env python3
# coding: utf-8

"""
Class BaseRepository and its children. Manages interactions with the ihm and with the database.

"""


class BaseRepository:
    """Master class initiating the database relation."""

    def __init__(self, db):
        self.db = db


class ProductRepository(BaseRepository):
    """Class inheriting from BaseRepository and managing the interactions for products"""

    def get_better_products_by_category(self, category):
        """
        Querying better products in a chosen category in the database.

        :param category: category of the products.

        :return better_products: products of the same category ordered by nutriscore level.

        """

        better_products = self.db.query(category.select_sql_query_better_products)
        return better_products

    def get_products_by_category(self, category):
        """
        Querying products in a chosen category in the database.

        :param category: category of the products.

        :return products: products of the same category.

        """

        products = self.db.query(category.select_sql_query_products)
        return products

    def get_products_by_user(self, user):
        """
        Querying products in the favorites of a chosen user in the database.

        :param user: user id.

        :return products: favorites products of the user.

        """

        products = self.db.query(user.select_sql_query_prod)
        return products

    def get_product_info(self, product):
        """
        Querying a product name and nutriscore in the database.

        :param product: product.

        :return product_name, product_nutriscore: name and nutriscore of the product.

        """

        return self.db.query(product.select_sql_query_info)
        # result = self.db.query(product.select_sql_query_info)
        # return result

    def get_substitute(self, product):
        """
        Querying a product substitute saved in favorites in the database.

        :param product: product to be substituted.

        :return substitute: product substitute saved in favorites.

        """

        substitute = self.db.query(product.select_sql_query_substitute)
        return substitute

    def insert_by_model(self, product):
        """
        Inserting a product and its information and relationships in the database.

        :param product: product to be inserted.

        """

        self.db.query(product.insert_sql_query_product)
        for store in product.stores:
            self.db.query(product.insert_sql_query_store(store))
            self.db.query(product.insert_sql_query_prod_store_relation(store))


class CategoryRepository(BaseRepository):
    """Class inheriting from BaseRepository and managing the interactions for categories"""

    def insert_by_model(self, category):
        """
        Inserting a category in the database.

        :param category: category to be inserted.

        """

        self.db.query(category.insert_sql_query)

    def get_categories(self):
        """
        Querying categories in the database.

        :return categories: categories found in the database.

        """

        categories = self.db.query('SELECT name FROM category;')
        return categories


class StoreRepository(BaseRepository):
    """Class inheriting from BaseRepository and managing the interactions for stores"""

    def get_stores_by_product(self, product):
        """
        Querying stores associated to a product in thr product_store_relation table of the database.

        :param product: product.

        :return stores_list: list of the srores associated to the product found in the database.

        """

        stores = self.db.query(product.select_sql_query_stores)
        stores_list = []
        for store in stores:
            stores_list.append(store["store_name"])
        return stores_list


class UserRepository(BaseRepository):
    """Class inheriting from BaseRepository and managing the interactions for users"""

    def insert_by_model(self, user):
        """
        Inserting a user in the database.

        :param user: user to be inserted.

        """

        self.db.query(user.insert_sql_query)

    def insert_favorite(self, user, bad_product, good_product):
        """
        Inserting user's favorite in the products_users_relation table of the database:
        bad product and its substitute.

        :param user: user.
        :param bad_product: product to be inserted.
        :param good_product: substitute.

        """

        self.db.query(user.insert_sql_query_prod_user_relation(good_product, bad_product))
