import RPi.GPIO as GPIO
from time import sleep
import serial as ser


def soil_moisture_read(ser_con):
    sleeping=False
    # Set Arduino port
    ser_con.flushInput()

    print("wake for data read")
    ser_con.write("W")
    sleep(.5)
    
    resp = ser_con.readline()
    if not resp:

        ser_con.write("W")
        sleep(.5)
        
        resp = ser_con.readline()
        msg = resp.decode('utf-8')
        # Here We ensure that the Ard is woke before we start sending commands.
        woke=False
        while not woke:
            if msg.rstrip() == u"Woke":
                print("success")
                woke=True
            else:
                ser_con.write("W")
                sleep(.5)
                resp = ser_con.readline()
                msg = resp.decode('utf-8')
   # Send the Command to Read The data
    ser_con.write('R')
    sleep(.4)
    resp = ser_con.readline()
    data=resp.decode('utf-8')
    print("Read Data: {}".format(data))
    
    return data

def to_sleep(ser_con):
    ser_con.flushInput()

    ser_con.write("W")
    sleep(.5)
    resp=ser_con.readline()
    
    if not resp:
        print("Currently sleeping")
    else:
        ser_con.write("S")
    

def pump_switch(ser_con):

    ser_con.flushInput()

    print("Wake for pump emission")
    ser_con.write("W")
    sleep(.5)
    
    resp = ser_con.readline()
    msg = resp.decode('utf-8')
    # Here We ensure that the Ard is woke before we start sending commands.
    woke=False
    while not woke:
        if msg.rstrip() == u"Woke":
            print("success")
            woke=True
        else:
            ser_con.write("W")
            sleep(.5)
            resp = ser_con.readline()
            msg = resp.decode('utf-8')
    # Send the command to switch the pump on or off
    ser_con.write("P")



