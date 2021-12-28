#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO


class Led:

    def __init__(self, green_pin=37, red_pin=31):
        self.green_pin = green_pin
        self.red_pin = red_pin
        self.on = 1
        self.off = 0
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.red_pin, GPIO.OUT)

    def green_led_on(self):
        GPIO.output(self.green_pin, self.on)

    def green_led_off(self):
        GPIO.output(self.green_pin, self.off)

    def red_led_on(self):
        GPIO.output(self.red_pin, self.on)

    def red_led_off(self):
        GPIO.output(self.red_pin, self.off)