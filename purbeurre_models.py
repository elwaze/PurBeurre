#! /usr/bin env python3
# coding: utf-8

"""
Classes to build the objects stored in the database.

"""

from purbeurre_repositories import ProductRepository
from purbeurre_repositories import CategoryRepository
from purbeurre_repositories import StoreRepository
from purbeurre_repositories import UserRepository
from database import db


class Product:
    """
    Class building products and managing their interactions with other objects.
    """

    objects = ProductRepository(db)

    def __init__(
            self,
            link=None,
            name=None,
            nutriscore=None,
            category=None,
            stores=None,
            users=None
    ):
        self.link = link
        self.name = name
        self.nutriscore = nutriscore
        self.category = category
        self.stores = stores
        self.users = users

    @property
    def insert_sql_query_product(self):
        """returns the SQL script to insert a product in the product table"""

        return 'INSERT IGNORE INTO product (link, name, nutriscore, category_name) VALUES ("{}", "{}", "{}", "{}");'.format(self.link, self.name, self.nutriscore, self.category)

    def insert_sql_query_store(self, store):
        """returns the SQL script to insert a store in the store table"""

        return 'INSERT IGNORE INTO store (name) VALUES ("{}");'.format(store)

    def insert_sql_query_prod_store_relation(self, store):
        """returns the SQL script to insert a product and a store in the product_store_relation table"""

        return 'INSERT IGNORE INTO product_store_relation (product_link, store_name) VALUES ("{}", "{}");'.format(self.link, store)

    def insert_into_db(self):
        """inserts the product int the database"""
        self.objects.insert_by_model(self)

    @property
    def select_sql_query_info(self):
        """returns the SQL script to get product information from the product table"""

        return 'SELECT name, nutriscore FROM product WHERE link = "{}";'.format(self.link)

    @property
    def select_sql_query_stores(self):
        """returns the SQL script to get stores related to a product in the product_store_relation"""

        return 'SELECT store_name FROM product_store_relation WHERE product_link = "{}";'.format(self.link)

    @property
    def select_sql_query_substitute(self):
        """returns the SQL script to get healthy products related to a product in the products_users_relation"""
        return 'SELECT good_product_link FROM products_users_relation WHERE bad_product_link = "{}";'.format(self.link)


class Category:
    """
    Class building categories and managing their interactions with other objects.
    """

    objects = CategoryRepository(db)

    def __init__(
            self,
            name=None
    ):
        self.name = name

    @property
    def insert_sql_query(self):
        """returns the SQL script to insert a category in the category table"""

        return 'INSERT IGNORE INTO category (name) VALUES ("{}")'.format(self.name)

    @property
    def select_sql_query_products(self):
        """returns the SQL script to get products in the product table for a defined category"""

        return 'SELECT name, link, nutriscore FROM product WHERE category_name = "{}";'.format(self.name)

    @property
    def select_sql_query_better_products(self):
        """returns the SQL script to get products in the product table for a defined category, ordered by nutriscore"""

        return 'SELECT * FROM product WHERE category_name = "{}" ORDER BY nutriscore ASC;'.format(self.name)

    def insert_into_db(self):
        """inserts the category into the database"""

        self.objects.insert_by_model(self)


class Store:
    """
    Class building stores and managing their interactions with other objects.
    """

    objects = StoreRepository(db)

    def __init__(
            self,
            name=None,
            products=None
    ):
        self.name = name
        self.products = products


class User:
    """
    Class building users and managing their interactions with other objects.
    """

    objects = UserRepository(db)

    def __init__(
            self,
            email_address=None,
            products=None
    ):
        self.email_address = email_address
        self.products = products

    @property
    def insert_sql_query(self):
        """returns the SQL script to insert a user in the user table"""

        return 'INSERT IGNORE INTO user (email_address) VALUES ("{}");'.format(self.email_address)

    def insert_into_db(self):
        """inserts the user into the database"""

        self.objects.insert_by_model(self)

    def insert_sql_query_prod_user_relation(self, good_product, bad_product):
        """returns the SQL script to insert a product , substitute and user in the products_users_relation table"""

        return """INSERT IGNORE INTO products_users_relation 
        (good_product_link, bad_product_link, user_email_address) 
        VALUES("{}", "{}", "{}");""".format(
                good_product.link, bad_product.link, self.email_address)

    @property
    def select_sql_query_prod(self):
        """returns the SQL script to get unhealthy products in the products_users_relation table for a defined user"""

        return 'SELECT DISTINCT bad_product_link FROM products_users_relation WHERE user_email_address = "{}";'.format(
            self.email_address)
