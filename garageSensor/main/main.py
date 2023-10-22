from machine import Pin
import utime
import socket
from utime import sleep

import network

# Distance sensor config
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

# 7 Segment Display Config
mydisplay = tm1637.TM1637(clk=Pin(27), dio=Pin(26))
mydisplay.brightness(0)

# WLAN Config
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("StarDestroyer","aaasssddd")
mydisplay.number(int(15))
sleep(15)

sta_if = network.WLAN(network.STA_IF)
ip = sta_if.ifconfig()[0]
print(ip)

# Print IP on display Pico W
for i in range(1):
    mydisplay.show("strt")
    sleep(1)
    for x in ip.split("."):
        mydisplay.number(int(x))
        print("ye")
        sleep(1)

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

def checkDistance():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    return (timepassed * 0.0343) / 2 # Distance from object in cm


while True:
    mydisplay.show("wait")
    cl, addr = s.accept()
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if "distance" in line:
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
            cl.send(checkDistance())
            cl.close()
        if not line or line == b'\r\n':
            break
