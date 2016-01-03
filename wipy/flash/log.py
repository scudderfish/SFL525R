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
running=True

def safeMkdir(path):
    pass
    
def ba2hex(ba):
    return ''.join('{:02x}'.format(x) for x in ba)

def finish(pin):
    running=False
# clk cmd and dat0 pins must be passed along with
# their respective alternate functions
sd = machine.SD(pins=('GP10', 'GP11', 'GP15'))
os.mount(sd, '/sd')
dataPin=machine.Pin('GP30')
ow = OneWire(dataPin)
ds=FDS18X20.FDS1820(ow)

powerPin=machine.Pin('GP16', mode=Pin.IN, pull=Pin.PULL_DOWN) #High when we should be switched on
livePin=machine.Pin('GP17', mode=Pin.OUT) #Held high whilst we want to run
livePin.value(1)
powerPin.irq(mode=Pin.IRQ_RISING,handler=finish)

path='/sd/data/'+'-'.join(map(str,time.localtime()))+'.csv'
print ('Writing to '+path)
with open(path,'w') as f:
    f.write('Time,')
    f.write(','.join(map(ba2hex,ds.roms)))
    f.write('\n')
    while running:
        temps = ds.read_temps()
        print(temps)
        f.write(str(time.time()))
        f.write(',')
        f.write(','.join(map(str,temps)))
        f.write('\n')
        f.flush()
    f.close()
