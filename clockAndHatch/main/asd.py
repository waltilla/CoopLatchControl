import socket
import network
import tm1637
from dht22 import DHT22
from machine import Pin
from utime import sleep

# Temp/Humid sensor config
dht = Pin(16,Pin.IN,Pin.PULL_UP)
dht11 = DHT22(dht,None,dht11=True)

# 7 Segment Display Config
mydisplay = tm1637.TM1637(clk=Pin(3), dio=Pin(2))
mydisplay.brightness(0)

# WLAN Config
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("StarDestroyer","aaasssddd")
sleep(10)
sta_if = network.WLAN(network.STA_IF)
ip = sta_if.ifconfig()[0]

# Print IP on display Pico W
for i in range(2):
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

while True:

    mydisplay.show("wait")
    cl, addr = s.accept()
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if "temp" in line:
            Temp,Humid = dht11.read()
            returnMessage = "temp," + Temp +",humid," + Humid
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
            cl.send(returnMessage)
            cl.close()

        if not line or line == b'\r\n':
            break