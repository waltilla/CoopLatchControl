import machine
import urequests as requests
import network
import datetime
import time
from utime import sleep
from machine import Pin
import tm1637

#button config

# 7 Segment Display Config
mydisplay = tm1637.TM1637(clk=Pin(16), dio=Pin(17))
mydisplay.brightness(0)
mydisplay.show("helo")

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


# Set time
rtc = machine.RTC()
rtc.datetime(get_datetime_tuple())
print(rtc.datetime())


last_state = False
current_state = False
isOpen = False

while True:

    #show time on 7segment display
    sleep(5)
    time = str(rtc.datetime()).split(",")
    minutesWithSpace = str(time[4]) + addZeroInSecounds(str(time[5]))
    mydisplay.show(minutesWithSpace.replace(' ', ''))

    #open and close hatch by time
    if(time[4] == 8 and isOpen == False):
        rtc.datetime(get_datetime_tuple())
        request = requests.get('http://192.168.1.224/open_hatch')
        sleep(22)
        request.close()
        isOpen = True

    if(time[4] == 18 and isOpen == True):
        rtc.datetime(get_datetime_tuple())
        print("close")
        request2 = requests.get('http://192.168.1.224/close_hatch')
        sleep(22)
        request2.close()
        isOpen = False












