#!/usr/bin/env python
# -*- coding: utf8 -*-

import lcd_driver
from time import sleep


class LCD:

    def __init__(self):
        self.lcd = lcd_driver.lcd()

    def lcd_print_data(self, data, refresh_time, row):
        # Do metody sa vklada ako druhy argument riadok na display kde sa to vypise
        self.lcd.lcd_display_string(str(data), row)
        sleep(refresh_time)

    def clear(self):
        self.lcd.lcd_clear()
