#!/usr/bin/env python
# -*- coding: utf8 -*-

from datetime import datetime
import time


class Clock:

    def clock_time(self):

        while True:
            date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S/%p")
            date, time1 = date_time.split()
            time2, time3 = time1.split('/')
            hour, minutes, seconds = time2.split(':')

            if 12 < int(hour) < 24:
                clock_time = date+ ' ' + str(int(hour) - 12) + ':' + minutes + ':' + seconds + '' + time3
            else:
                clock_time = time2 + ' ' + time3

            return clock_time

