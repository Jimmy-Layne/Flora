from time import sleep
import datetime as dt
import lib.the_bog as bog
import serial as ser
''' This is the script that cares for the bog. It reads data from the arduino, and manages the pump system based on this

It is designed to be called on a chron schedule, The arduno is placed into sleep mode after each read.'''

# This flag is set to false when moisture is low
SOIL_MOISTURE_FLAG = True
pump_timer = 5.0

port = "/dev/ttyACM0"
ser_con = ser.Serial(port,9600,timeout=1)
ser_con.flushInput()

# Start by reading data from the arduino
data = int(bog.soil_moisture_read(ser_con))
sleep(1)


if data > 500:
    SOIL_MOISTURE_FLAG = False
    # Activate pump
    print("Low Soil Moisture, Activating pump")
    bog.pump_switch(ser_con)
    sleep(pump_timer)
    while not SOIL_MOISTURE_FLAG:
        
        print('checking pump continuance')
        data = int(bog.soil_moisture_read(ser_con))
        if data >500:
            print("Moisture is still low, continuing pump cycle")
            sleep(pump_timer)
            continue
        else:
            # Call The pump activation function again to dactivate
            bog.pump_switch(ser_con)
            SOIL_MOISTURE_FLAG = True
else:
    pass
    # There should be some timestamp functionality here but for now
    # we'll just pass

bog.to_sleep(ser_con)
