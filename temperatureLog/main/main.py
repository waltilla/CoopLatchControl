
#
#   Final Version 1.0 All ok
#
import socket
import network
import tm1637
from dht22 import DHT22
from machine import Pin
from utime import sleep

# Temp/Humid sensor config
dht = Pin(0,Pin.IN,Pin.PULL_UP)
dht11 = DHT22(dht,None,dht11=True)
dhtUte = Pin(0,Pin.IN,Pin.PULL_UP)
dht11Ute = DHT22(dhtUte,None,dht11=True)

# 7 Segment Display Config
mydisplay = tm1637.TM1637(clk=Pin(2), dio=Pin(3))
mydisplay.brightness(0)

# WLAN Config
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("StarDestroyer","aaasssddd")

sleep(7)

sta_if = network.WLAN(network.STA_IF)
ip = sta_if.ifconfig()[0]
print(ip)
# Print IP on display Pico W
for i in range(1):
    mydisplay.show("strt")
    for x in ip.split("."):
        mydisplay.number(int(x))
        print("ye")

addr = socket.getaddrinfo('0.0.0.0', 4441)[0][-1]

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)


while True:
    print("ok")
    cl, addr = s.accept()
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()

        if not line or line == b'\r\n':
            break

    Temp,Humid = dht11.read()
    uTemp,uHumid = dht11Ute.read()

    returnMessage = "temp_inside," + str(Temp) +",humid_inside," + str(Humid) + ",temp_outside," + str(uTemp) +",humid_outside," + str(uHumid)
    print(returnMessage)
    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(returnMessage)
    cl.close()




