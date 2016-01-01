# main.py -- put your code here!
from machine import SD
from machine import Pin
from onewire import *
import os
import uDS3231
import FDS18X20
import time

# Set the time according to the real RTC
uDS3231.DS3231().loadTime()

def safeMkdir(path):
    pass
    
def ba2hex(ba):
    return ''.join('{:02x}'.format(x) for x in ba)

# clk cmd and dat0 pins must be passed along with
# their respective alternate functions
sd = machine.SD(pins=('GP10', 'GP11', 'GP15'))
os.mount(sd, '/sd')
dataPin=machine.Pin('GP30')
ow = OneWire(dataPin)
ds=FDS18X20.FDS1820(ow)

path='/sd/data/'+'-'.join(map(str,time.localtime()))+'.csv'

print ('Writing to '+path)
with open(path,'w') as f:
    f.write('Time,')
    f.write(','.join(map(ba2hex,ds.roms)))
    f.write('\n')
    for x in range(1,1000):
        temps = ds.read_temps()
        print(temps)
        f.write(str(time.time()))
        f.write(',')
        f.write(','.join(map(str,temps)))
        f.write('\n')
        
