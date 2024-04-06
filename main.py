# Weather Collector
import network
import urequests
from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd
from secrets import SSID, PW, openweather
#Setup the I2C LCD
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
lcd.blink_cursor_on()

 # secrets.py file contains Wi-Fi details
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

while wlan.isconnected() == False:
    wlan.connect(SSID, PW)
    print("No connection")
    lcd.putstr("No connection")
    sleep(2)
    lcd.clear()
else:
    ifconfig = wlan.ifconfig()
    lcd.backlight_on()
    print(ifconfig[0])
    lcd.putstr("IP ADDRESS")
    lcd.putstr("\n"+ifconfig[0])
    sleep(5)
    lcd.clear()

while True:
    for i in range(3):
        lcd.backlight_off()
        lcd.putstr("Fetching\nweather")
        sleep(0.5)
        lcd.backlight_on()
        sleep(0.5)
        lcd.clear()
    r = urequests.get("http://api.openweathermap.org/data/2.5/weather?q=Blackpool,UK&appid="+openweather+"&units=metric").json()
    weather = r["weather"]
    temperature = r["main"]["temp"]
    weather = (weather[0]["main"])
    lcd.clear()
    lcd.backlight_on()
    lcd.putstr(weather)
    lcd.putstr("\nTemp: "+str(temperature)+"C")
    sleep(300)
    lcd.clear()
    