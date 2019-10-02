#! /usr/bin env python3
# coding: utf-8

from purbeurre_repositories import ProductRepository
from purbeurre_repositories import CategoryRepository
from purbeurre_repositories import StoreRepository
from purbeurre_repositories import UserRepository
from database import db


class Product:
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
        self.stores = stores    # collection / liste (si ordonné)
        self.users = users  # collection / liste (si ordonné)

    @property
    def insert_sql_query_product(self):
        return 'INSERT IGNORE INTO product (link, name, nutriscore, category_name) VALUES ("{}", "{}", "{}", "{}");'.format(
            self.link, self.name, self.nutriscore, self.category)

    def insert_sql_query_store(self, store):
        return 'INSERT IGNORE INTO store (name) VALUES ("{}");'.format(store)

    def insert_sql_query_prod_store_relation(self, store):
        return 'INSERT IGNORE INTO product_store_relation (product_link, store_name) VALUES ("{}", "{}");'.format(self.link, store)

    def insert_into_db(self):
        self.objects.insert_by_model(self)

    @property
    def select_sql_query_name(self):
        return 'SELECT name FROM product WHERE link = "{}";'.format(self.link)

    @property
    def select_sql_query_stores(self):
        return 'SELECT store_name FROM product_store_relation WHERE product_link = "{}";'.format(self.link)

    @property
    def select_sql_query_substitute(self):
        return 'SELECT good_product_link FROM products_users_relation WHERE bad_product_link = "{}";'.format(self.link)


class Category:
    objects = CategoryRepository(db)

    def __init__(
            self,
            name=None
    ):
        self.name = name

    @property
    def insert_sql_query(self):
        return 'INSERT IGNORE INTO category (name) VALUES ("{}")'.format(self.name)

    @property
    def select_sql_query_products(self):
        return 'SELECT name, link, nutriscore FROM product WHERE category_name = "{}";'.format(self.name)

    @property
    def select_sql_query_better_products(self):
        return 'SELECT * FROM product WHERE category_name = "{}" ORDER BY nutriscore ASC;'.format(self.name)

    def insert_into_db(self):
        self.objects.insert_by_model(self)

    def get_from_db(self):
        self.objects.get_categories()


class Store:
    objects = StoreRepository(db)

    def __init__(
            self,
            name=None,
            products=None
    ):
        self.name = name
        self.products = products


class User:
    objects = UserRepository(db)

    def __init__(
            self,
            email_adress=None,
            products=None
    ):
        self.email_adress = email_adress
        self.products = products

    @property
    def insert_sql_query(self):
        return 'INSERT IGNORE INTO user (email_adress) VALUES ("{}");'.format(self.email_adress)

    def insert_into_db(self):
        self.objects.insert_by_model(self)

    def insert_sql_query_prod_user_relation(self, good_product, bad_product):
        return 'INSERT IGNORE INTO products_users_relation (good_product_link, bad_product_link, user_email_adress) VALUES("{}", "{}", "{}");'.format(
                good_product.link, bad_product.link, self.email_adress)

    @property
    def select_sql_query_prod(self):
        return 'SELECT bad_product_link FROM products_users_relation WHERE user_email_adress = "{}";'.format(self.email_adress)


if __name__ == "__main__":
    pass
    # ex pr recup tous les prod de la bdd :
    # products = Product.objects.get_products()
    # pr recup prod d'1 cat :
    # catprod = Product.objects.get_products_by_category(category_name)
# enreg unn nouveau prod :
#new_prod_categories = Categorie.object.get_by_name(category_name) ?
# new_product = Product.object.insert(link, name, nutriscore, stores, new_prod_categories)
