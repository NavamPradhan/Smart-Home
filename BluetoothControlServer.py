import os
import requests
from bluetooth import *
import RPi.GPIO as GPIO

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12,GPIO.OUT)
#GPIO.output(12,GPIO.LOW)
GPIO.setup(16,GPIO.OUT)
#GPIO.output(16,GPIO.LOW)
GPIO.setup(20,GPIO.OUT)
#GPIO.output(20,GPIO.LOW)
bulb1 = 0
bulb2 = 0
motor = 0

advertise_service( server_sock, "BTS",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
                    )
                   
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        print("received [%s]" % data.decode("utf-8"))
        if data == "1":
	    print ("Bulb 1 ON")
            GPIO.output(12,GPIO.HIGH)
	    bulb1 = data

        if data == "0":
            print ("Bulb 1 OFF")
	    GPIO.output(12,GPIO.LOW)
	    bulb1 = data
	    
        if data == "2":
	    print ("Bulb 2 ON")
            GPIO.output(16,GPIO.HIGH)
	    bulb2 = data

        if data == "3":
	    print ("Bulb 2 OFF")
            GPIO.output(16,GPIO.LOW)
	    bulb2 = data

	if data == "8":
	    print ("Motor ON")
	    GPIO.output(20,GPIO.HIGH)
	    motor = data

	if data == "9":
	    print ("Motor OFF")
	    GPIO.output(20,GPIO.LOW)
	    motor = data

except IOError:
    pass

print("Disconnected")

print("Updating bulb status to cloud")

Request1 = 'https://api.thingspeak.com/update?api_key=R7DX6SEZF0A6P5DG&field1='
Request1 += str(bulb1)

Request2 = 'https://api.thingspeak.com/update?api_key=R7DX6SEZF0A6P5DG&field2='
Request2 += str(bulb2)

Request3 = 'https://api.thingspeak.com/update?api_key=R7DX6SEZF0A6P5DG&field6='
Request3 += str(motor)

request = requests.get(Request1)
request = requests.get(Request2) 
request = requests.get(Request3)

print("Updated")


client_sock.close()
server_sock.close()
print("All Closed")




