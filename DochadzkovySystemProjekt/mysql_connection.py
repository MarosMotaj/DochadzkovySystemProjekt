#!/usr/bin/env python
# -*- coding: utf8 -*-

import mysql.connector

"""
        host="34.116.128.160",
        user="rpi_i_s_u",
        password="rpi_i_s_u",
        database="RPI_ATTEND"

        Tabulky v RPI_ATTEND databaze:
        TG_LINE_PAR      return data[1]+" "+data[2]
        TG_OPS_2         return data[1]
        TG_OPS_LIST     tu sa priraduje cislo karty uzivatelovi, return data[1]"""

class SQL:

    # Host je IP adresa PC kde bezi MySQL databaza
    # user a password je uzivatel z MySQL servra, vytvoreny na MySQL serveri
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.mysql_database = mysql.connector.connect(host=self.host,
                                                      user=self.user,
                                                      password=self.password,
                                                      database=self.database)
        self.my_cursor = self.mysql_database.cursor()

    def insert_user_id(self):
        self.my_cursor.execute("UPDATE TG_OPS_LIST SET OPS_CHIP='122-79-161-190-42' WHERE ID='2'")
        # musi byt commit inaksie neurobi zmeny po zapise
        self.mysql_database.commit()

    def print_table_data(self):
        # Vykona zadane SQL prikazy
        # vypise vsetky data v riadkoch
        # my_cursor.execute("select * from TG_OPS_LIST")

        # vypise vsetky nazvy stlpcov
        self.my_cursor.execute("SELECT * FROM TG_OPS_LIST")

        # Vypise data na zadanom indexe
        data = self.my_cursor.fetchall()

        for i in data:
            print(i)

        self.mysql_database.close()

        # return data[1]  # +" "+data[2] -pri metode  data = my_cursor.fetchall().pop(0)


