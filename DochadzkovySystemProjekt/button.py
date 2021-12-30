#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO


class Button:

    def __init__(self, button_pin):
        self.button_pin = button_pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def button_callback(self):

        if GPIO.input(self.button_pin) == GPIO.HIGH:
            return True
        else:
            return False





