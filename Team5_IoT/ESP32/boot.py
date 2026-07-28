try:
    import usocket as socket
except:
    import socket

import network
import dht
from machine import Pin
from time import sleep
import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'Khongbiet'
password = 'akisuru40027052'

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(ssid, password)

while sta.isconnected() == False:
    pass

print('Ket noi mang Wifi thanh cong!')
print(sta.ifconfig())

sensor = dht.DHT11(Pin(14))
