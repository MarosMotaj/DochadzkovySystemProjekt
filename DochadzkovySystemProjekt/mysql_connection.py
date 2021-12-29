#!/usr/bin/env python
# -*- coding: utf8 -*-
import time

import mysql.connector
import socket

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

    def connect_to_sql(self):
        self.mysql_database = mysql.connector.connect(host=self.host,
                                                      user=self.user,
                                                      password=self.password,
                                                      database=self.database)

    # Ziska nazov pracovnej linky
    def get_line_name(self):
        self.connect_to_sql()
        my_cursor = self.mysql_database.cursor()
        my_cursor.execute("SELECT LINE FROM TG_LINE_PAR WHERE VALUE_CHAR='AA1'")
        data = my_cursor.fetchall().pop(0)
        line_name = data[0]
        self.mysql_database.close()
        return line_name

    # Kontrola ci je niekto nalogovany
    def check_if_user_logged(self):
        self.connect_to_sql()
        my_cursor = self.mysql_database.cursor()
        my_cursor.execute("SELECT ID, LINE, OPS_ID, TAG_SINCE, TAG_TO FROM TG_OPS_2 WHERE LINE='STR_4' ORDER BY ID DESC LIMIT 1")
        data = my_cursor.fetchall().pop(0)
        tag_to = data[4]
        self.mysql_database.close()
        if tag_to is None:
            tag_to = data[4]
            ops_id = data[2]
            tag_since = data[3]
        else:
            tag_to = "---------- ----------"
            ops_id = "--------"
            tag_since = "---------- ----------"

        return tag_to, ops_id, tag_since

    def check_chip_number(self, detected_chip_number):
        print(detected_chip_number)
        self.connect_to_sql()
        my_cursor = self.mysql_database.cursor()
        try:
            my_cursor.execute(f"SELECT ID, OPS_ID, OPS_CHIP FROM TG_OPS_LIST WHERE OPS_CHIP='{detected_chip_number}' ORDER BY ID DESC LIMIT 1")
            data = my_cursor.fetchall().pop(0)
            id = data[0]
            ops_id = data[1]
            ops_chip = data[2]
            self.mysql_database.close()
            return ops_id, True
        except:
            return "Karta nepresla", False

    def insert_user(self, line_name, ops_id):
        self.connect_to_sql()
        my_cursor = self.mysql_database.cursor()
        my_cursor.execute(f"INSERT INTO TG_OPS_2(LINE, OPS_ID, TAG_SINCE) VALUES ('{line_name}','{ops_id}',NOW())")
        # musi byt commit inaksie neurobi zmeny po zapise
        self.mysql_database.commit()
        self.mysql_database.close()

    def print_table_data(self):
        # Vykona zadane SQL prikazy
        # vypise vsetky data v riadkoch
        # my_cursor.execute("select * from TG_OPS_LIST")

        self.connect_to_sql()
        my_cursor = self.mysql_database.cursor()
        # vypise vsetky nazvy stlpcov
        my_cursor.execute("SELECT * FROM TG_OPS_2")

        # Vypise data na zadanom indexe
        data = my_cursor.fetchall()

        for i in data:
            print(i)

        self.mysql_database.close()

        # return data[1]  # +" "+data[2] -pri metode  data = my_cursor.fetchall().pop(0)


