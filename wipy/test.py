#!/usr/bin/env python
import pexpect,sys

def ctrl_d(a):
    a.sendcontrol('d')
    a.expect('>>>')

def cmd(a,str):
    line=str+'\r'
    a.sendline(line)
    a.expect('>>>')
    
def setup():
    pexpect.run('sitecopy -u wipy')
    a=pexpect.spawn('telnet 192.168.1.1')
    a.logfile=sys.stdout
    a.expect('Login as:')
    a.sendline('micro')
    a.expect('assword:')
    a.sendline('python')
    a.expect('>>>')
    ctrl_d(a)
    return a

def teardown(a):
    pass
        
def test_ulcd(a):
    ctrl_d(a)
    cmd(a,'import ulcd')
    cmd(a,'ulcd.lcd().test()')

def test_command(a):
    ctrl_d(a)
    cmd(a,'import command.sensors')
    cmd(a,'command.sensors.test()')
    cmd(a,'command.sensors.testServer()')
    pass
        
def run_tests(a):
    test_ulcd(a)
    test_command(a)
    
if __name__=="__main__":
    a=setup()
    run_tests(a)
    teardown(a)
    
