#!/usr/bin/python

# Pi Nerf Turret Controller

import board
import busio
import adafruit_pca9685
import time
import keyboard
from adafruit_servokit import ServoKit

# Define object for servo control
kit = ServoKit(channels=16)

# Pins of each servo
x_axis = 13
y_axis = 12
trigger = 14

# Position Variables
y_position = 100
trigger_position = 0

# Limits
y_max = 160
y_min = 100
trigger_min = 0
y_increment_unit = 2 # this determines speed of y axis movement

# Utility Functions
def activate_trigger( number ):
	time.sleep(1)
	kit.servo[number].angle = 100
	time.sleep(0.3)
	# Set back to zero
	kit.servo[number].angle = 0

def reset_defaults():
	# Reset everything to known good values
	kit.servo[y_axis].angle = y_min + 30
	kit.servo[trigger].angle = trigger_min
	kit.continuous_servo[x_axis].throttle = 0

# Handle Keyup events separately for x axis control
# of continuous servos
def on_key_release(key):
	if key.name == "up" || key.name == "down":
		print("up/down released")
		# Turn off
		kit.continuous_servo[x_axis].throttle = 0

# Define the on release event
keyboard.on_release(on_key_release, suppress=False)

# Main Loop
try:
	reset_defaults()
	running = True

	while running:

		# Use while statements to prevent key repeat which is 
		# the desired behavior for controlling servos 
		# (we don't want servos to move after key is released)
		while keyboard.is_pressed("up"):
			print("UP")
			if( y_position < y_max ):
				y_position=y_position+y_increment_unit
				kit.servo[y_axis].angle = y_position
			else:	
				print( "Y axis out of range" )
				y_position = y_max

		while keyboard.is_pressed("down"):
			print("DOWN")
			if( y_position > y_min ):
				y_position=y_position-y_increment_unit
				kit.servo[y_axis].angle = y_position
			else:
				print( "Y axis out of range" )
				y_position = y_min	

		while keyboard.is_pressed("left"):
			print("LEFT")
			kit.continuous_servo[x_axis].throttle = -1

		while keyboard.is_pressed("right"):
			print("RIGHT")
			kit.continuous_servo[x_axis].throttle = 1

	    while keyboard.is_pressed(" "):
			print("SPACE")
			time.sleep(1)
			kit.servo[number].angle = 100
			time.sleep(0.3)
			# Set back to zero
			kit.servo[number].angle = 0

		while keyboard.is_pressed("q"):
			print("Quitting...")
			reset_defaults()
			running = False
			break

		#print( kit.continuous_servo[x_axis].throttle )

