#! /usr/bin env python3
# coding: utf-8

"""
Connection to the database.

"""

import records
import os

db = records.Database('mysql+mysqlconnector://{}:{}@{}/{}'.format(
     os.environ.get("PURBEURRE_DB_USER"),
     os.environ.get("PURBEURRE_DB_PASSWORD"),
     os.environ.get("PURBEURRE_DB_IP"),
     os.environ.get("PURBEURRE_DB_NAME")))

# db = records.Database('mysql+mysqlconnector://root:Uhqjr#2019@localhost/OFF')

