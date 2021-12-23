#!/usr/bin/env python
# -*- coding: utf8 -*-

import mysql.connector

# Host je IP adresa PC kde bezi MySQL databaza
# user a password je uzivatel z MySQL servra, vytvoreny na MySQL serveri


def print_data():
    mysql_database = mysql.connector.connect(host="192.168.0.100",
                                             user="root",
                                             password="Montoza1857",
                                             database="dochadzkovy_system")


    my_cursor = mysql_database.cursor()
    # Vykona zadane SQL prikazy
    my_cursor.execute("select * from employees")

    # Vypise data na zadanom indexe
    data = my_cursor.fetchall().pop(0)

    # for i in data:
    #     print(i)
    mysql_database.close()

    return data[1]+" "+data[2]

