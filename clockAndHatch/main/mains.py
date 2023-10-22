import machine
import urequests as requests
import network
from lib import tm1637, datetime

from machine import Pin
from utime import sleep

door_bell = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_DOWN)

# 7 Segment Display Config
mydisplay = tm1637.TM1637(clk=Pin(16), dio=Pin(17))
mydisplay.brightness(0)

# WLAN Config
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("StarDestroyer","aaasssddd")
mydisplay.show("INIT")

#Add time to connect
sleep(1)

status = wlan.ifconfig()
ip = status[0]

#Print ip
print('ip = ' + ip)
for splitted_ip_number in ip.split("."):
    mydisplay.number(int(splitted_ip_number))
    sleep(0)

last_state = False
current_state = False
isOpen = False


# Time API
timeAPI = 'https://timeapi.io/api/Time/current/coordinate?latitude=57.70&longitude=11.97' # lat lon gothenburg

time = requests.get(timeAPI).json()
minute = time.get('minute')
hour = time.get('hour')
print(minute)
time_obj = datetime.time(hour, minute)  # Given time object
date_today = datetime.date.today()  # Today's date
datetime_obj = datetime.datetime.combine(date_today, time_obj)  # Combine date and time
one_minute = datetime.timedelta(minutes=1)  # One minute timedelta

secounds60 = 1
while True:

    sleep(1)
    secounds60 += 1

    numberss = str(datetime_obj.time())

    numbers = numberss.split(":")
    mydisplay.show(str(numbers[0]) + str(numbers[1]))
    #mydisplay.show(str(datetime_obj.hour) + str(datetime_obj.minutes))
    current_state = door_bell.value()
    if last_state == False and current_state == True:

        if(isOpen == False):
            print("open")

            request = requests.get('http://192.168.1.224/open_hatch')
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



    if(secounds60 == 60):
        datetime_obj = datetime_obj + one_minute  # Add one minute
        secounds60 = 1




