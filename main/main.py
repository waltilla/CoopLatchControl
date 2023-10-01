import socket
import network
import tm1637
from machine import Pin
from utime import sleep
import PicoMotorDriver


# 7 Segment Display Config
mydisplay = tm1637.TM1637(clk=Pin(27), dio=Pin(26))
mydisplay.brightness(0)

# WLAN Config
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("StarDestroyer","aaasssddd")

sleep(10)

sta_if = network.WLAN(network.STA_IF)
ip = sta_if.ifconfig()[0]
print(ip)

# Motor driver config
board = PicoMotorDriver.KitronikPicoMotor()

# Print IP on display Pico W
for i in range(1):
    mydisplay.show("strt")
    sleep(1)
    for x in ip.split("."):
        mydisplay.number(int(x))
        print("ye")
        sleep(1)

mydisplay.number(int(4441))

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()


s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(addr)

s.listen(1)


# Show IP on Display
print(addr)

closed = True

while True:

    for i in range(1):
        mydisplay.show("strt")
        sleep(1)
        for x in ip.split("."):
            mydisplay.number(int(x))
            print(x)
            print("ye")
            sleep(1)

    mydisplay.show("wait")
    # Return message
    returnMessage = ""
    # show scrolling text
    # update display
    cl, addr = s.accept()
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if "open_hatch" in line:

            if closed == True:
                print("open hatch cause closed")
                print("code for open hatch")
                returnMessage = "open_hatch"
                for x in range(110):
                    board.step("f", 8)

                closed = False
            else:
                print("already open")
                returnMessage = "open_hatch_allready_opened"


        if "close_hatch" in line:

            if closed == False:
                print("closing hatch")
                print("code for closing hatch")
                returnMessage = "close_hatch"
                for x in range(110):
                    board.step("r", 8)

                closed = True
            else:
                print("already closed")
                returnMessage = "close_hatch_Already_closed"


        if not line or line == b'\r\n':
            break

    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
    cl.send(returnMessage)
    cl.close()

