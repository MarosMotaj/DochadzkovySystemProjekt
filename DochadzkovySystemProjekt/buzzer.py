#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
from time import sleep

class Buzzer:

    def __init__(self, pin=18):
        self.pin = pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, False)

    def run_buzzer(self):
        while True:
            GPIO.output(self.pin, True)
            sleep(2)
            GPIO.output(self.pin, False)
            break
