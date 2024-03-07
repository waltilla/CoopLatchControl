import machine
import urequests as requests
import network
import datetime
import socket
import time
from utime import sleep
from machine import Pin
import tm1637

# import thread module
import _thread


#button config

# 7 Segment Display Config
mydisplay = tm1637.TM1637(clk=Pin(16), dio=Pin(17))
mydisplay.brightness(0)
mydisplay.show("love")

# ----- WLAN Config -----
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("StarDestroyer","aaasssddd")
sleep(7)    #Add time to make sure its connected


def get_datetime_tuple():
    timeAPI = 'https://timeapi.io/api/Time/current/coordinate?latitude=57.70&longitude=11.97' # lat lon gothenburg
    d = requests.get(timeAPI).json() #Return
    return ((d.get('year'), d.get('month'), d.get('day'),0, d.get('hour'), d.get('minute'), d.get('seconds'), 0))

def addZeroInSecounds(sec):
    if len(sec) == 1:
        return "0" + sec
    else:
        return sec
print(1)


# Set time
rtc = machine.RTC()
rtc.datetime(get_datetime_tuple())
print(rtc.datetime())

sta_if = network.WLAN(network.STA_IF)
ip = sta_if.ifconfig()[0]
print(ip)

addr = socket.getaddrinfo('0.0.0.0', 4441)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)


print(1)

last_state = False
current_state = False
isOpen = True
timeToOpen = '08'
timeToCLose = '17'

def clock_thread():

    while True:
        #show time on 7segment display
        sleep(5)
        time = str(rtc.datetime()).split(",")
        hour = addZeroInSecounds(str(time[4]).replace(' ', ''))
        minutes = addZeroInSecounds(str(time[5]).replace(' ', ''))
        mydisplay.show(hour + minutes)

        #open and close hatch by time
        if(hour == '08' and isOpen == False):
            rtc.datetime(get_datetime_tuple())
            request = requests.get('http://192.168.1.224/open_hatch')
            sleep(22)
            request.close()
            isOpen = True

        if(hour == '17' and isOpen == True):
            rtc.datetime(get_datetime_tuple())
            print("close")
            request2 = requests.get('http://192.168.1.224/close_hatch')
            sleep(22)
            request2.close()
            isOpen = False
        print("here")

def setValueThread():

    while True:
        print("here to")
        cl, addr = s.accept()
        request = cl.recv(1024)
        line = str(request)



        print("here trrrr")

        if "set_true" in line:
            isOpen = True
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send("Hatch isOpen is set to True")
            cl.close()
            mydisplay.show("TRUE")
            sleep(5)
        if "set_false" in line:
            isOpen = False
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send("Hatch isOpen is set to False")
            cl.close()
            mydisplay.show("FLSE")
            sleep(5)



second_thread = _thread.start_new_thread(clock_thread, ())
setValueThread()








