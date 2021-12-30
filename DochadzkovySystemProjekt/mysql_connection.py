#!/usr/bin/env python
# -*- coding: utf8 -*-

import mysql.connector


class SQL:

    # Host je IP adresa PC kde bezi MySQL databaza
    # user a password je uzivatel z MySQL servra, vytvoreny na MySQL serveri
    def __init__(self, host, user, password, database):
        self.mysql_database = None
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
    def sql_check_if_somebody_is_logged(self):
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

    # Odhlasenie operatora
    def logoff_operator(self, line_name, ops_id):
        self.connect_to_sql()
        my_cursor = self.mysql_database.cursor()
        my_cursor.execute(f"SELECT ID, LINE, OPS_ID, TAG_SINCE, TAG_TO FROM TG_OPS_2 WHERE LINE='STR_4' AND OPS_ID"
                          f"='{ops_id}' ORDER BY ID DESC LIMIT 1")
        data = my_cursor.fetchall().pop(0)
        id = data[0]
        tag_since = data[3]
        tag_to = data[4]
        if tag_to is not None and tag_since is not None:
            my_cursor.execute(f"INSERT INTO TG_OPS_2(LINE, OPS_ID, TAG_TO) VALUES ('{line_name}','{ops_id}',NOW())")
        if tag_since is not None and tag_to is None:
            my_cursor.execute(f"UPDATE TG_OPS_2 set TAG_TO=NOW() WHERE ID='{id}'")

        self.mysql_database.commit()
        self.mysql_database.close()

    # Over ci je cip v databaze
    def check_chip_number(self, detected_chip_number):
        self.connect_to_sql()
        my_cursor = self.mysql_database.cursor()
        try:
            my_cursor.execute(f"SELECT ID, OPS_ID, OPS_CHIP FROM TG_OPS_LIST WHERE OPS_CHIP"
                              f"='{detected_chip_number}' ORDER BY ID DESC LIMIT 1")
            data = my_cursor.fetchall().pop(0)
            ops_id = data[1]
            self.mysql_database.close()
            return ops_id, True
        except:
            return "Karta nepresla", False

    # Prihlasenie operatora
    def login_operator(self, line_name, ops_id):
        self.connect_to_sql()
        my_cursor = self.mysql_database.cursor()
        my_cursor.execute(f"INSERT INTO TG_OPS_2(LINE, OPS_ID, TAG_SINCE) VALUES ('{line_name}','{ops_id}',NOW())")
        self.mysql_database.commit()
        self.mysql_database.close()

    # Testovacia metoda
    def print_table_data(self):
        self.connect_to_sql()
        my_cursor = self.mysql_database.cursor()
        my_cursor.execute("SELECT * FROM TG_OPS_2")

        data = my_cursor.fetchall()

        for i in data:
            print(i)

        self.mysql_database.close()



