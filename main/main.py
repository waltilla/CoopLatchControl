import socket
import network
import tm1637
from machine import Pin
from utime import sleep
from dht22 import DHT22

# 7 Segment Display Config
mydisplay = tm1637.TM1637(clk=Pin(16), dio=Pin(17))
mydisplay.brightness(0)

# Temp/Humidity Sensor Config
dht = Pin(11,Pin.IN,Pin.PULL_UP)
dht11 = DHT22(dht,None,dht11=True)


# WLAN Config
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("StarDestroyer","aaasssddd")
sta_if = network.WLAN(network.STA_IF)
ip = sta_if.ifconfig()[0]
print(ip)

#Print IP to Pico W
for i in range(3):
    mydisplay.show("strt")
    sleep(1)
    for x in ip.split("."):
        print(mydisplay.number(int(x)))
        sleep(1)

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

#Show IP on Display
print(addr)
closed = True

while True:
    #show scrolling text
    # update display
    Temp,Humid = dht11.read()
    mydisplay.temperature(Temp)
    sleep(1)
    mydisplay.number(Humid)
    sleep(1)

    cl, addr = s.accept()
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if "open_hatch" in line:

            if closed == True:
                print("open hatch cause closed")
                print("code for open hatch")
                closed = False
            else:
                print("already open")
            break

        if "close_hatch" in line:

            if closed == False:
                print("closing hatch")
                print("code for closing hatch")
                closed = True
            else:
                print("already closed")
            break

        if not line or line == b'\r\n':
            break

    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
    cl.send("Temp: " + str(Temp) + "C Humidity: " + str(Humid))
    cl.close()


