#! /usr/bin env python3
# coding: utf-8

import requests


class Off_Requests():
    def get_categories(self):
        # get categories from the OpenFoodFacts' API
        request_categories = requests.get('https://fr.openfoodfacts.org/categories&json=1')
        categories_json = request_categories.json()
        data_tags = categories_json.get('tags')
        data_categories = []
        for data in data_tags:
            data_categories.append(data_tags.get('name', 'None'))
        category_number = 0
        while category_number < 10:
            print(data_categories[category_number])
            # self.cursor = self.db.cursor()
            # add_category = ("INSERT INTO Category" "(category)" "VALUES('{}')".format(data_categories[category_number]))
            # self.cursor.execute(add_category)
            # self.db.commit()
            # self.cursor.close()
            category_number += 1

            #         # self.cursor = self.db.cursor()
            #         # add_category = ("INSERT INTO Category" "(category)" "VALUES('{}')".format(data_categories[category_tested]))
            #         # self.cursor.execute(add_category)
            #         # self.db.commit()
            #         # self.cursor.close()
