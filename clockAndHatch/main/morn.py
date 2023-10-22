import machine
import urequests as requests
import time
import network
from lib import tm1637
from machine import Pin
from utime import sleep

# 7 Segment Display Config
mydisplay = tm1637.TM1637(clk=Pin(27), dio=Pin(26))
mydisplay.brightness(0)

mydisplay.number(int(1))
sleep(1)
print("ese")


# WLAN Config
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("StarDestroyer","aaasssddd")
mydisplay.number(int(1))
sleep(10)

door_bell = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)


status = wlan.ifconfig()
print('ip = ' + status[0])

last_state = False
current_state = False
isOpen = False

while True:

    current_state = door_bell.value()
    if last_state == False and current_state == True:

        if(isOpen == False):
            print("open")
            request = requests.get('http://192.168.1.224/open_hatch')

            #request = requests.get('http://worldtimeapi.org/api/timezone/Europe/Stockholm"')

            sleep(10)
            print(request.content)
            request.close()
            isOpen = True
            time.sleep(1)
        else:
            print("close")
            request2 = requests.get('http://192.168.1.224/close_hatch')
            print(request2.content)
            request2.close()
            isOpen = False
            time.sleep(10)

        time.sleep(2)

    last_state = current_state




