from onewire import *
import machine
import time

class FDS1820(object):
    def __init__(self, onewire):
        self.ow = onewire
        self.roms = [rom for rom in self.ow.scan() if rom[0] == 0x10 or rom[0] == 0x28]

    def read_temp(self, rom=None):
        """
        Read and return the temperature of one DS18x20 device.
        Pass the 8-byte bytes object with the ROM of the specific device you want to read.
        If only one DS18x20 device is attached to the bus you may omit the rom parameter.
        """
        rom = rom or self.roms[0]
        ow = self.ow
        ow.reset()
        ow.select_rom(rom)
        ow.write_byte(0x44)  # Convert Temp
        while True:
            if ow.read_bit():
                break
        ow.reset()
        ow.select_rom(rom)
        ow.write_byte(0xbe)  # Read scratch
        data = ow.read_bytes(9)
        return self.convert_temp(rom[0], data)

    def read_temps(self):
        """
        Read and return the temperatures of all attached DS18x20 devices.
        """
        temps = []
        ow=self.ow
        ow.reset()
        for rom in self.roms:
            ow.select_rom(rom)
            ow.write_byte(0x44)
        while True:
            if ow.read_bit():
                break
        ow.reset()
        for rom in self.roms:
            ow.select_rom(rom)
            ow.write_byte(0xbe)  # Read scratch
            data = ow.read_bytes(9)
            temps.append(self.convert_temp(rom[0], data))
        return temps

    def slow_read_temps(self):
        temps=[];
        for rom in self.roms:
            temps.append(self.read_temp(rom))
        return temps;
        
    def convert_temp(self, rom0, data):
        """
        Convert the raw temperature data into degrees celsius and return as a fixed point with 2 decimal places.
        """
        temp_lsb = data[0]
        temp_msb = data[1]
        if rom0 == 0x10:
            if temp_msb != 0:
                # convert negative number
                temp_read = temp_lsb >> 1 | 0x80  # truncate bit 0 by shifting, fill high bit with 1.
                temp_read = -((~temp_read + 1) & 0xff) # now convert from two's complement
            else:
                temp_read = temp_lsb >> 1  # truncate bit 0 by shifting
            count_remain = data[6]
            count_per_c = data[7]
            temp = 100 * temp_read - 25 + (count_per_c - count_remain) // count_per_c
            return temp
        elif rom0 == 0x28:
            return (temp_msb << 8 | temp_lsb) * 100 // 16
        else:
            assert False

def tst():
    dat = machine.Pin('GP30')
    ow = OneWire(dat)
    ds = FDS1820(ow)
    print('devices:', ds.roms)
    start=time.ticks_ms()
    for x in range(0,3):
        print('temperatures:', ds.slow_read_temps())
    print(time.ticks_diff(start,time.ticks_ms()))
    start=time.ticks_ms()
    for x in range(0,3):
        print('temperatures:', ds.read_temps())
    print(time.ticks_diff(start,time.ticks_ms()))
