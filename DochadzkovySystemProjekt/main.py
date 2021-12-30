#!/usr/bin/env python
# -*- coding: utf8 -*-

from rfid_rc522 import RFID


if __name__ == '__main__':
    rfid = RFID("AA1")
    rfid.run_rfid()


