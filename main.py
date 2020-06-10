import os
import requests
import json
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12,GPIO.OUT)
GPIO.output(12,GPIO.LOW)
GPIO.setup(16,GPIO.OUT)
GPIO.output(16,GPIO.LOW)
GPIO.setup(20,GPIO.OUT)
GPIO.output(20,GPIO.LOW)

req = None

JsonResult = None

req3 = requests.get("https://api.thingspeak.com/channels/543455/fields/1/last.json?api_key=KRQ7MZOD1RLEL142")
JsonResult3 = json.loads((req3.text))
temp = JsonResult3['field1']

try:
	while True:
		req = None

		JsonResult = None

		print("Request Sent")
		req1 = requests.get("https://api.thingspeak.com/channels/541492/fields/1/last.json?api_key=UNC1US4WU3ANWDRJ")
		req2 = requests.get("https://api.thingspeak.com/channels/541492/fields/2/last.json?api_key=UNC1US4WU3ANWDRJ")
		req3 = requests.get("https://api.thingspeak.com/channels/543455/fields/1/last.json?api_key=KRQ7MZOD1RLEL142")
		req4 = requests.get("https://api.thingspeak.com/channels/542686/fields/1/last.json?api_key=9PGLV1DS9E9CT7AN")
		req5 = requests.get("https://api.thingspeak.com/channels/541492/fields/6/last.json?api_key=UNC1US4WU3ANWDRJ")

		JsonResult1 = json.loads((req1.text))
		JsonResult2 = json.loads((req2.text))
		JsonResult3 = json.loads((req3.text))
		JsonResult4 = json.loads((req4.text))
		JsonResult5 = json.loads((req5.text))

		bulb1 = JsonResult1['field1']
		bulb2 = JsonResult2['field2']
		camera = JsonResult3['field1']
		bluetooth = JsonResult4['field1']
		motor = JsonResult5['field6']

		print bulb1
		print bulb2
		print camera
		print bluetooth
		print motor

		if bluetooth == "4":
			os.system('sudo python BluetoothControlServer.py')
			
		if camera != temp:
			os.system('python camera.py')
			temp = camera

		if bulb1 == "1":
            		print ("Bulb 1 ON")
            		GPIO.output(12,GPIO.HIGH)

	        if bulb1 == "0":
        		print ("Bulb 1 OFF")
            		GPIO.output(12,GPIO.LOW)

        	if bulb2 == "2":
            		print ("Bulb 2 ON")
			GPIO.output(16,GPIO.HIGH)

		if bulb2 == "3":
            		print ("Bulb 2 OFF")
            		GPIO.output(16,GPIO.LOW)

		if motor == "8":
			print ("Motor ON")
			GPIO.output(20,GPIO.HIGH)

		if motor == "9":
			print ("Motor OFF")
			GPIO.output(20,GPIO.LOW)


except KeyboardInterrupt:
	GPIO.cleanup()
	print ("Interrupted!!")


