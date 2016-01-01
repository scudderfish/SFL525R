import FDS18X20
from machine import Pin
from onewire import *
import socket 

class Server(object):
    def __init__(self,port=51938):
        dat = Pin('GP30')
        ow=OneWire(dat)
        self.sensors = FDS18X20.FDS1820(ow)

    def __del__(self):
        self.s.close()
    
    def run(self):
        pass
        
    def process(self,conn):
        x=conn.read(1)
        print(x)
        self.command(x)
        
    def command(self,cmdStr):
        method_name = 'cmd_' + cmdStr
        method = getattr(self, method_name, lambda: "nothing")
        return method()

    def cmd_S(self):
        return self.sensors.roms
        
    def cmd_T(self):
        return self.sensors.read_temps()
        
    def cmd_X(self):
        self.running=False
        self.s.close()
        
def test():
    print('Server Test')
    a=Server()
    print(a.command('S'))
    print(a.command('T'))
    print('Done')
    pass
    
def testServer():
    a=Server()
    print("Running")
    a.run()
    print("Finished")
    