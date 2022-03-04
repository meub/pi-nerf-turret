#Pi Nerf Turret Controller

#!/usr/bin/python
import curses
import board
import busio
import adafruit_pca9685
import time

from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

def activate_servo( number, angle, duration):
	kit.servo[number].angle = angle
	time.sleep(duration)
	#kit.servo[number].angle = 0

def activate_c_servo( number, direction, duration):
	kit.continuous_servo[number].throttle = direction
	time.sleep(duration)
	kit.continuous_servo[number].throttle = 0

def activate_trigger( number ):
	time.sleep(1)
	kit.servo[number].angle = 100
	time.sleep(0.3)
	kit.servo[number].angle = 0


# Ports
x_axis = 13
y_axis = 12
trigger = 14

# Position Variables
x_position = 0
y_position = 100
trigger_position = 0

# Limits
y_max = 160
y_min = 100
trigger_min = 0

# get the curses screen window
screen = curses.initscr()
 
# turn off input echoing
curses.noecho()
 
# respond to keys immediately (don't wait for enter)
curses.cbreak()
 
# map arrow keys to special values
screen.keypad(True)
 
try:
	# Reset everything to known good values
	kit.servo[y_axis].angle = y_min + 30
	kit.servo[trigger].angle = trigger_min
	kit.continuous_servo[x_axis].throttle = 0

	while True:
		char = screen.getch()
		if char == ord('q'):
			kit.servo[y_axis].angle = y_min + 30
			kit.servo[trigger].angle = trigger_min
			kit.continuous_servo[x_axis].throttle = 0
			break

		if char == curses.KEY_UP:
			screen.addstr(0, 0, 'up   ')
			if( y_position < y_max ):
				y_position=y_position+2
				kit.servo[y_axis].angle = y_position
			else:	
				print( "Y axis out of range" )
				y_position = y_max
		   
		if char == curses.KEY_DOWN:
			screen.addstr(0, 0, 'down ')
			if( y_position > y_min ):
				y_position=y_position-2
				kit.servo[y_axis].angle = y_position
			else:
				print( "Y axis out of range" )
				y_position = y_min		

		if char == curses.KEY_RIGHT:
			screen.addstr(0, 0, 'right ')
			kit.continuous_servo[x_axis].throttle = 1
			time.sleep(0.1)
			kit.continuous_servo[x_axis].throttle = 0

		if char == curses.KEY_LEFT:
			screen.addstr(0, 0, 'left ')
			kit.continuous_servo[x_axis].throttle = -1
			time.sleep(0.2)
			kit.continuous_servo[x_axis].throttle = 0

		if char == ord(' '):
			screen.addstr(0, 0, 'fire ')
			print ("Firing")
			kit.servo[trigger].angle = 100
			time.sleep(0.3)
			kit.servo[trigger].angle = 0
			
		print( y_position )

finally:
    # shut down cleanly
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()

































