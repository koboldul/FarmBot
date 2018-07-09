import RPi.GPIO as GPIO
import time
import sys
import datetime

from time import sleep

from notifier import Notifier

#init stuff

GPIO.setmode(GPIO.BCM)
mailer = Notifier()

pump = 22
valve = 4
sprinklers = 17

rainDetectedAt = None

pumpTime = 24000
valveTime = 5000
hasIrrigation = False
def start_device(pin):
	global pump
	global valve
	global sprinklers
	p = pin
	if pin == 'v':
		p = valve
	if pin == 'p':
		p = pump
	if pin == 'k':
		p = sprinklers
	print('Starting device ' + str(p))
	global mailer	
	mailer.log('Start device {0}'.format(pin))
	
	try:
		GPIO.setup(p,GPIO.OUT)
		GPIO.output(p, GPIO.LOW)
	except Exception as e:
		print (e)

	return

def checkIrrigation(pin):
	global valve
	try:
		return pin == 'v' or int(pin) == valve
	except:
		return False

def stop_device(pin):
	global mailer
	GPIO.output(pin, GPIO.HIGH)

def stop_all():
	GPIO.setup(pump, GPIO.OUT)
	GPIO.setup(valve, GPIO.OUT)
	GPIO.setup(sprinklers, GPIO.OUT)	
	GPIO.cleanup()

if sys.argv[1] == 's':
	stop_all()
	print ('stopped all')
	
else:
	try:
		for i in range(1,len(sys.argv)):
			print ('Starting', str(sys.argv[i]))
			start_device(sys.argv[i])
			if checkIrrigation(sys.argv[i]):
				hasIrrigation = True
				print ('Has irrigation')
			print ('Started', str(sys.argv[i]))
		if hasIrrigation == True:
			time.sleep(valveTime)
			print ('Done with the irrigation')
			GPIO.setup(valve, GPIO.HIGH)
	except Exception as e:
		print (e)
		print ('cleaning on error')
		GPIO.cleanup()
