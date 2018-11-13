#include <avr/sleep.h>

// Pin declarations
int wakePin = 2;
int sleepStatus = 0;
int snsrPwr = 7;
int snsrPin = A0;
int relayPin = 8;
bool PUMP_ENGAGE = false;

// Here we're going to impliment some smoothing to make sure that the readings are accurate
const int numRead = 5;



// Code to be called on wakeup
void wakeup(){
  //Could put some stuff here?
}


//Setup
void setup(){
  pinMode(wakePin,INPUT);
  pinMode(snsrPwr, OUTPUT);
  digitalWrite(snsrPwr, LOW);
  pinMode(relayPin,OUTPUT);
  digitalWrite(relayPin,LOW);
  Serial.begin(9600);
  // attach the interrupt pin and set the condition for wakeup
  attachInterrupt(0, wakeup, LOW);
}
 
//This is the function that controls the sleep and shutdown
void naptime()
{
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();
  attachInterrupt(0,wakeup,LOW);
 //enter sleep
  sleep_mode(); 
  // As a saftey, the first thing to do after exiting sleep mode is
  // disable sleep bit, and detach interrupt pin
  sleep_disable();
  detachInterrupt(0);
}

void snsrRead()
{
 int total = 0;
 int avg = 0;
 digitalWrite(snsrPwr,HIGH);
 delay(100);
 
 for (int i =0 ; i < numRead; i++){
   total = total + analogRead(snsrPin);
   delay(10);
 }
 digitalWrite(snsrPwr, LOW);
 avg = total/numRead;
 
 Serial.println(avg);
}
 
void pump_switch(){
 if(PUMP_ENGAGE==false){
  PUMP_ENGAGE = true;
  Serial.println("Engaging Pump.");
  digitalWrite(relayPin,HIGH);
}
 else{
    PUMP_ENGAGE=false;
    Serial.println("Disengaging Pump.");
    digitalWrite(relayPin,LOW);
}

}
 
void loop(){
  if(Serial.available()){
    int val = Serial.read();
    if (val == 'S'){
	//make sure everything is off for sleep mode
    	digitalWrite(relayPin,LOW);
	digitalWrite(snsrPwr,LOW);
        Serial.println("Entering Sleep Mode");
        delay(1000);
        naptime();

    }
    else if(val == 'W'){
      Serial.println("Woke");
   
    }
    else if(val == 'R'){
      snsrRead();
    }
    else if(val == 'P'){
      pump_switch();
    }
  }
  
  delay(100);
  
  
}
