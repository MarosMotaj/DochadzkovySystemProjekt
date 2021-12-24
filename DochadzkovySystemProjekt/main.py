#!/usr/bin/env python
# -*- coding: utf8 -*-

from rfid_rc522 import RFID
from mysql_connection import SQL

rfid = RFID()
sql = SQL("34.116.128.160", "rpi_i_s_u", "rpi_i_s_u", "RPI_ATTEND")

if __name__ == '__main__':
    # rfid.run_rfid()
    # sql.insert_user_id()
    sql.print_table_data()

