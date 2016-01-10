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
