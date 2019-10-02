#! /usr/bin env python3
# coding: utf-8


# lieu qui contient les methodes qui permettront de realiser les opérations utiles dans l'appli
# (ex get_unhealthy_products_by_category)
# c'est ici qu'on a le sql: toute la couche d'acces a la bdd
# méthodes spécifiques pour les interactions avec la bdd. C'est ces repositories là qui vont se connecter à la bdd

class BaseRepository:
    def __init__(self, db):
        self.db = db


class ProductRepository(BaseRepository):

    def get_better_products_by_category(self, category):
        better_products = self.db.query(category.select_sql_query_better_products)
        return better_products

    def get_products_by_category(self, category):
        products = self.db.query(category.select_sql_query_products)
        return products

    def get_products_by_user(self, user):
        products = self.db.query(user.select_sql_query_prod)
        return products

    def get_product_name(self, product):
        product_name = self.db.query(product.select_sql_query_name)
        return product_name

    def get_substitute(self, product):
        substitute = self.db.query(product.select_sql_query_substitute)
        return substitute

    def insert_by_model(self, product):
        """
        :param product:
        :type product: purbeurre_models.Product
        :return:
        """
        # requete sql de type insert:
        rows = self.db.query(product.insert_sql_query_product)
        for store in product.stores:
            rows = self.db.query(product.insert_sql_query_store(store))
            rows = self.db.query(product.insert_sql_query_prod_store_relation(store))


class CategoryRepository(BaseRepository):

    def insert_by_model(self, category):
        """
        :param category:
        :type category: purbeurre_models.Category
        :return:
        """
        # requete sql de type insert:
        rows = self.db.query(category.insert_sql_query)

    def get_category_by_product(self, product):
        category = self.db.query(product.select_sql_query_cat)
        return category

    def get_categories(self):
        categories = self.db.query('SELECT name FROM category;')
        return categories

    def get_products_by_category(self, category):
        category_products = self.db.query(category.select_sql_query_prod)
        return category_products


class StoreRepository(BaseRepository):

    def get_stores_by_product(self, product):
        stores = self.db.query(product.select_sql_query_stores)
        stores_list = []
        for store in stores:
            stores_list.append(store["store_name"])
        return stores_list


class UserRepository(BaseRepository):

    def insert_by_model(self, user):
        rows = self.db.query(user.insert_sql_query)

    def insert_favorite(self, user, bad_product, good_product):
        rows = self.db.query(user.insert_sql_query_prod_user_relation(bad_product, good_product))

    def get_favorites_by_user(self, user):
        favorites = self.db.query(user.select_sql_query_favorites)

    def get_products_by_user(self, user):
        user_products = self.db.query(user.select_sql_query_prod)
        return user_products
