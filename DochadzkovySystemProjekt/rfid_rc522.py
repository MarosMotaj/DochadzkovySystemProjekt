#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import mfrc522 as MFRC522
from led import Led
from lcd_display import LCD
from clock import Clock
from mysql_connection import SQL
from button import Button
from buzzer import Buzzer
import signal
import time


class RFID:

    def __init__(self, device_name):
        self.device_name = device_name
        GPIO.setwarnings(False)
        self.continue_reading = True
        self.signal = signal.signal(signal.SIGINT, self.end_read)
        self.MIFAREReader = MFRC522.MFRC522()
        self.sql = SQL("34.116.128.160", "rpi_i_s_u", "rpi_i_s_u", "RPI_ATTEND")
        self.lcd = LCD()
        self.green_led = Led(37)
        self.red_led = Led(31)
        self.clock = Clock()
        self.buzzer = Buzzer()
        self.login_button = Button(29)
        self.date, self.time, self.hour, self.minutes = self.clock.clock_time()

    # Capture SIGINT for cleanup when the script is aborted
    def end_read(self):
        # global continue_reading
        self.continue_reading = False
        GPIO.cleanup()

    def check_if_user_logged(self):
        self.sql.connect_to_sql()
        self.line_name = self.sql.get_line_name()
        tag_to, ops_id, tag_since = self.sql.check_if_user_logged()
        self.lcd.lcd_print_data("Pripojene na SQL", 2, 1)
        self.lcd.lcd_print_data(f"{self.date}       {self.device_name}", 0, 1)
        self.lcd.lcd_print_data(f"              {self.sql.get_line_name()}", 0, 2)
        self.lcd.lcd_print_data(f"AC:{ops_id}", 0, 3)
        self.lcd.lcd_print_data(f"FROM: {str(tag_since)[11:16]}  "
                                f"{str(tag_since)[2:4]}."
                                f"{str(tag_since)[8:11].strip()}.", 0, 4)
        self.sql.mysql_database.close()

    def run_rfid(self):
        try:
            self.red_led.off()
            self.green_led.on()
            self.check_if_user_logged()
        except:
            self.green_led.off()
            self.red_led.on()
            self.lcd.lcd_print_data("Nepripojene na SQL", 2, 0)
            quit()

        # This loop keeps checking for chips. If one is near it will get the UID and authenticate
        while self.continue_reading:
            print("Pripojene na SQL server?: "+str(self.sql.mysql_database.is_connected()))
            # Scan for cards
            (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)

            # If a card is found
            if status == self.MIFAREReader.MI_OK:
                print("Karta bola detekovana")

            # Get the UID of the card
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == self.MIFAREReader.MI_OK:
                self.lcd.clear()
                try:
                    detected_chip_number = str(uid[0])+"-"+str(uid[1])+"-"+ str(uid[2])+"-"+str(uid[3])+"-"+str(uid[4])
                    if self.sql.check_chip_number(detected_chip_number)[1] is False:
                        self.red_led.on()
                        self.lcd.lcd_print_data("Karta nerozpoznana", 0, 2)
                        self.lcd.lcd_print_data("ID:" + str(uid[0]) + "-" + str(uid[1]) + "-" + str(uid[2]) + "-" + str(
                            uid[3]) + '-' + str(
                            uid[4]), 1, 1)
                        self.buzzer.run_buzzer()
                        self.red_led.off()
                        self.lcd.clear()
                        self.check_if_user_logged()
                    else:
                        self.lcd.lcd_print_data("ID:" + str(uid[0]) + "-" + str(uid[1]) + "-" + str(uid[2]) + "-" + str(
                            uid[3]) + '-' + str(
                            uid[4]), 1, 1)
                        self.lcd.lcd_print_data("Karta rozpoznana", 0, 2)
                        self.buzzer.run_buzzer()
                        self.lcd.lcd_print_data("Stlac prichod/odchod", 0, 2)
                        while True:
                            if self.login_button.button_callback() is True:
                                print("tlacitko stlacene")
                                self.sql.insert_user(self.sql.get_line_name(), detected_chip_number)
                                time.sleep(1)
                                break
                        self.lcd.clear()
                        self.check_if_user_logged()

                        print(self.sql.print_table_data())

                except Exception as e:
                    print(e)
                    self.lcd.lcd_print_data("Chyba", 0, 2)

                # # Print UID
                # print("UID karty: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(
                #     uid[3]) + ',' + str(
                #     uid[4]))
                # self.lcd.lcd_print_data("ID:" + str(uid[0]) + "-" + str(uid[1]) + "-" + str(uid[2]) + "-" + str(
                #                         uid[3]) + '-' + str(
                #                         uid[4]), 1, 1)
                #
                # # This is the default key for authentication
                # # key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                #
                # # Select the scanned tag
                # self.MIFAREReader.MFRC522_SelectTag(uid)

                # self.lcd.clear()

                # # ENTER Your Card UID here
                # my_uid = [122, 79, 161, 190, 42]
                #
                # # Check to see if card UID read matches your card UID
                # if uid == my_uid:  # Open the Doggy Door if matching UIDs
                #     self.lcd.clear()
                #     self.led.green_led_on()
                #     try:
                #         self.sql.connect_to_sql()
                #         print(self.sql.mysql_database.is_connected())
                #     except:
                #         print("SQL je nedostupne")
                #         self.lcd.lcd_print_data("Vypadok SQL spojenia", 2, 1)
                #         quit()
                #     print(self.sql.get_line_name())
                #     self.lcd.lcd_print_data("Vstup povoleny", 2, 1)
                #     print("Vstup povoleny")
                #     self.led.green_led_off()
                #     self.lcd.clear()
                #     self.sql.mysql_database.close()
                #     print(self.sql.mysql_database.is_connected())
                #
                #
                # else:  # Don't open if UIDs don't match
                #     self.lcd.clear()
                #     self.led.red_led_on()
                #     self.lcd.lcd_print_data("Vstup zamietnuty", 2, 1)
                #     print("Vstup zamietnuty")
                #     self.led.red_led_off()
                #     self.lcd.clear()
