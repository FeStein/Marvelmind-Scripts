"""
File: nmea_serial_parse.py
Author: Felix Steinmetz
Email: fsteinme@rhrk.uni-kl.de / felix.steinmetz@gmx.de
Github: https://github.com/FeStein
Description: Parses nnmea prtocol in serial. Will be used to determine tranfer
rate of marvelmind beacon. For description of python nmea parser see the
corrsespoding github repo github.com/Knio/pynmea2
"""

import io
import collections
import serial #https://pyserial.readthedocs.io/en/latest/pyserial_api.html#classes

from datetime import datetime, date

import pynmea2

################################################################################
    #Parameter
################################################################################

# corresponds to the d serial port on my mac
serial_port = '/dev/cu.usbserial-A50285BI'

#defined by musbelmusb
baudr = 115200

################################################################################
    #Parsing
################################################################################

ser = serial.Serial(serial_port, baudrate=baudr, timeout=5.0)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

#readChar = ser.read(1)
#while (readChar != None) and (readChar != ''):
#    bufferSerialDeque = collections.deque(maxlen=255)
#    readChar = ser.read(1)
#    bufferList = list(self._bufferSerialDeque)
#    strbuf = (b''.join(bufferList)) 

msg_list = []

i = 1
while True and i <= 1200:
    try:
        line = sio.readline()
        msg =pynmea2.parse(line)
        i+=1
        msg_list.append(msg)
        #print(i,'|',msg)
        if i%50 == 0: print(i)
    except serial.SerialException as e:
        print('Device error: {}'.format(e))
        break
    except pynmea2.ParseError as e:
        line = sio.readline()
        print(repr(line))
        print('Parse error: {}'.format(e))
        continue

msg_list = msg_list[300:]


start_time = msg_list[0].timestamp
end_time = msg_list[-1].timestamp

diff = datetime.combine(date.today(),end_time) - datetime.combine(date.today(),start_time)

number_of_protocols = len(msg_list)

rate = number_of_protocols/diff.total_seconds()

print('Transfer rate per second {}'.format(rate))
