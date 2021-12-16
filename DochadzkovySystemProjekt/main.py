import lcd_driver
from time import sleep


mylcd = lcd_driver.lcd()

# Do metody sa vklada ako druhy argument riadok na display kde sa to vypise
mylcd.lcd_display_string("     Hello lcd", 2)
sleep(5)
mylcd.lcd_clear()
