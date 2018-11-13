import RPi.GPIO as GPIO
from time import sleep
import Flora.lib.the_bog as bog
''' This is the script that cares for the bog. It reads data from the arduino, and manages the pump system based on this

It is designed to be called on a chron schedule, The arduno is placed into sleep mode after each read.'''

relay_pin = 18
pump_timer = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin,GPIO.OUT)
# This flag is set to false when moisture is low
SOIL_MOISTURE_FLAG = True
try:
    # Start by reading data from the arduino
    data = bog.soil_moisture_read()
    
    if data < 800:
        SOIL_MOISTURE_FLAG = False
        # Activate pump
        print("Low Soil Moisture, Activating pump")
        GPIO.output(relay_pin,GPIO.HIGH)
        sleep(pump_timer)
        while not SOIL_MOISTURE_FLAG:
            data = bog.soil_moisture_read()
            if data > 800:
                GPIO.output(relay_pin,GPIO.LOW)
                SOIL_MOISTURE_FLAG = True
        
    else:
        pass
        # There should be some timestamp functionality here but for now
        # we'll just pass
        
    GPIO.cleanup()
except KeyboardInterrupt:
    GPIO.cleanup()
