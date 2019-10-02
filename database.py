#! /usr/bin env python3
# coding: utf-8

import records

db = records.Database('mysql+mysqlconnector://root:Uhqjr#2019@localhost/OFF')

# var d'environnement pour ne pas écrire mon mdp en clair.
# => "mysql://username:{}@hostname:port/table".format(os.environ.get('P5_MYSQL_PASSWORD')
