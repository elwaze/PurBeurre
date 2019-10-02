#! /usr/bin env python3
# coding: utf-8

"""
Connection to the database.

"""

import records
import os

db = records.Database('mysql+mysqlconnector://root:{}@localhost/OFF'.format(os.environ.get('P5_MYSQL_PASSWORD')))
