import lcd_driver
import mysql_connection
from time import sleep


mylcd = lcd_driver.lcd()

# Do metody sa vklada ako druhy argument riadok na display kde sa to vypise
mylcd.lcd_display_string(mysql_connection.print_data(), 2)
sleep(5)
mylcd.lcd_clear()
