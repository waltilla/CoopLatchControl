import machine
import urequests as requests
import time
import network
from lib import tm1637
from machine import Pin
from dht22 import DHT22
from utime import sleep

# 7 Segment Display Config
mydisplay = tm1637.TM1637(clk=Pin(27), dio=Pin(26))
mydisplay.brightness(0)

mydisplay.number(int(1))
sleep(1)
print("ese")

# Temp/Humidity Sensor Config
dht = Pin(11,Pin.IN,Pin.PULL_UP)
dht11 = DHT22(dht,None,dht11=True)

print("ese")


# WLAN Config
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("StarDestroyer","aaasssddd")
mydisplay.number(int(1))
sleep(10)
print("ese")

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
            request = requests.get("192.168.1.244:80/open_hatch")
            print("open")
            request.close()
            isOpen = True
            time.sleep(1)
        if(isOpen == True):
            request = requests.get("192.168.1.244:80/close_hatch")
            request.close()
            isOpen = False
            time.sleep(1)

        time.sleep(2)

    last_state = current_state


