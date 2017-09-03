import RPi.GPIO as GPIO
import time
import random

# Turn on debug prints
DEBUG = 0

# Define the GPIO pins
BUZZER = 37
RED = 7
BLUE = 11
YELLOW = 13
GREEN = 15
NOCOLOR = 0
REDBUTTON = 29
BLUEBUTTON = 31
YELLOWBUTTON = 33
GREENBUTTON = 35

# Arrays for buttons and LEDs
ledpins = [RED, BLUE, YELLOW, GREEN]
buttonpins = [REDBUTTON, BLUEBUTTON, YELLOWBUTTON, GREENBUTTON]

# pattern is the array that makes the pattern
pattern = []

def setup():
	GPIO.setmode(GPIO.BOARD)

	# Setup led pins
	for pin in ledpins:
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.LOW)

	# Setup button pins
	for pin in buttonpins:
		GPIO.setup(pin, GPIO.IN)

	# Setup buzzer
	GPIO.setup(BUZZER, GPIO.OUT)
	GPIO.output(BUZZER, GPIO.LOW)


def printColorName(color):
	if (color == RED):
		print("RED")
	elif (color == BLUE):
		print("BLUE")
	elif (color == YELLOW):
		print("YELLOW") 
	elif (color == GREEN):	
		print("GREEN")


def scanbutton():
	buttonpressed = False
	timeout = 2.5
	timechecks = 1000
	timetowait = timeout / timechecks 

	while(buttonpressed == False):
		# Accumulate small waits to do a timeout if player waits too long
		time.sleep(timetowait)
		timechecks -= 1
		if (timechecks == 0):
			return NOCOLOR
		# Translate button pressed into the corresponding color
		redbutton = GPIO.input(REDBUTTON)
		if (redbutton == GPIO.HIGH):
			return RED
		bluebutton = GPIO.input(BLUEBUTTON)
		if (bluebutton == GPIO.HIGH):
			return BLUE
		yellowbutton = GPIO.input(YELLOWBUTTON)
		if (yellowbutton == GPIO.HIGH):
			return YELLOW
		greenbutton = GPIO.input(GREENBUTTON)
		if (greenbutton == GPIO.HIGH):
			return GREEN		
		

def showsuccess(color):
	if (DEBUG == 1):
		printColorName(color)
	GPIO.output(color, GPIO.HIGH)
	frequency = 0
	# Each color has a frequency
	if (color == RED):
		frequency = 1200.0
	elif (color == BLUE):
		frequency = 1100.0
	elif (color == YELLOW):
		frequency = 1000.0
	elif (color == GREEN):	
		frequency = 900.0
	playbuzz(frequency, 0.30)
	GPIO.output(color, GPIO.LOW)


def showfail(color):
	print("")
	print("Fail!")
	GPIO.output(color, GPIO.HIGH)
	playbuzz(100.0, 1.0)
	GPIO.output(color, GPIO.LOW)
	print("Your score was: " + str(len(pattern) - 1))
	print("")


def playbuzz(frequency, duration):
	# Convert frequency to period
	period = (1.0 / frequency)
	timecount = 0.0
	while (timecount < duration):
		GPIO.output(BUZZER, GPIO.HIGH)
		time.sleep(period / 2.0)
		GPIO.output(BUZZER, GPIO.LOW)
		time.sleep(period / 2.0)
		timecount += period
	

def loop():
	print("")
	while True:
		# 1. Make pattern 
		newint = random.randint(0,3)
		newpincolor = ledpins[newint]
		pattern.append(newpincolor)

		# 2. Display pattern
		if (DEBUG == 1):
			print(" Pattern")
			print("---------")
		for color in pattern:
			showsuccess(color)
			time.sleep(0.15)
		if (DEBUG == 1):
			print("")

		# 3. Get user input
		if (DEBUG == 1):
			print(" Player")
			print("--------")
		for color in pattern:
			buttonpressed = scanbutton()
			if (color == buttonpressed):
				showsuccess(color)
			else:
				showfail(color) #fix here to show the color that the user missed
				return

		if (DEBUG == 1):
			print("")
		time.sleep(0.5)
			

def destroy():
	GPIO.cleanup()


if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
		destroy()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, destroy() will be called before exiting
		destroy()



