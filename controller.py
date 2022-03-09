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
y_max = 180
y_min = 50
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
	kit.servo[y_axis].angle = 50
	kit.servo[trigger].angle = trigger_min
	kit.continuous_servo[x_axis].throttle = 0

# Handle Keyup events separately for x axis control
# of continuous servos
def on_key_release(key):
	print(key.name)
	if "left" in key.name or "right" in key.name:
		print("left/right released")
		# Turn off
		kit.continuous_servo[x_axis].throttle = 0

# Define the on release event
keyboard.on_release(on_key_release, suppress=False)

# Main Loop

#reset_defaults()
running = True

print(kit.servo[y_axis].angle)
# Set Y to current position

y_position = kit.servo[y_axis].angle	
	
while running:
	
	# Need to have this for some reason
	time.sleep(0.02)
	
	# Use while statements to prevent key repeat which is 
	# the desired behavior for controlling servos 
	# (we don't want servos to move after key is released)
	while keyboard.is_pressed("up"):
		y_position=y_position+y_increment_unit
		if( y_position > y_max ):
			print("Y is over max")
			y_position=y_position-y_increment_unit
		else:	
			kit.servo[y_axis].angle = y_position
			time.sleep(0.02)
			print( kit.servo[y_axis].angle )

	while keyboard.is_pressed("down"):
		y_position=y_position-y_increment_unit
		if( y_position < y_min ):
			print("Y is over max")
			y_position=y_position+y_increment_unit
		else:	
			kit.servo[y_axis].angle = y_position
			time.sleep(0.02)
			print( kit.servo[y_axis].angle )

	while keyboard.is_pressed("left"):
		#print("LEFT")
		kit.continuous_servo[x_axis].throttle = -1

	while keyboard.is_pressed("right"):
		#print("RIGHT")
		kit.continuous_servo[x_axis].throttle = 1

	while keyboard.is_pressed(" "):
		print("SPACE")
		kit.servo[trigger].angle = 100
		time.sleep(0.3)
		# Set back to zero
		kit.servo[trigger].angle = 0

	while keyboard.is_pressed("q"):
		print("Quitting...")
		kit.servo[y_axis].angle = 120
		#reset_defaults()
		running = False
		break

