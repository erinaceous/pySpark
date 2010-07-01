#!/usr/bin/python -OO
JOYSTICK = 0 #which joystick (in /dev/event/jsX) to use

import pygame

class JoystickListener:
	def __init__(self,joystick=0):
		self.joy = pygame.joystick.Joystick(joystick)
		self.id = joystick
		self.joy.init()
		self.map = maps[self.joy.get_name()]
		self.state = 0

	def axis(self,e):
		self.state = 0
		map = self.map['axis']
		for i in map.keys():
			if e.dict['axis'] == map[i][0]:
				if round(e.dict['value']) == map[i][1]:
					self.state = i

	def button(self,e):
		self.state = 0
		map = self.map['buttons']
		for i in map.keys():
			if e.dict['button'] == map[i]:
				self.state = i

def axis(e):
	if e.dict['joy'] == joy.id:
		joy.axis(e)

def button(e):
	if e.dict['joy'] == joy.id:
		joy.button(e)

def idle(e):
	if e.dict['joy'] == joy.id:
		joy.state = 0

events = {
	#what events should be listened to,
	#and the functions they bind to
	pygame.JOYAXISMOTION: axis,
	pygame.JOYBUTTONDOWN: button,
	pygame.JOYBUTTONUP: idle
}

maps = {
	#JoyAxisMotion: tuple(axis,min-value,max-value)
	#	^ which joystick axis (and what values)
	#	correspond to which motions.
	#
	#Button: int(button)
	#	^ what button corresponds to what action.

	"Xbox 360 Wireless Receiver":{
		"axis": {
			1: (1,-1), #1: forward
			2: (1,1), #2: backward
			3: (0,-1), #3: sidestep left
			4: (0,1), #4: sidestep right
			5: (3,-1), #5: turn left
			6: (3,1) #6: turn right
		},
		"buttons": {
			7: 4, #9: kick
			8: 5 #10: stand up.
		}
	}
}

descriptions = {
	0: 'Idle',
	1: 'Forward',
	2: 'Backward',
	3: 'Sidestep Left',
	4: 'Sidestep Right',
	5: 'Turn Left',
	6: 'Turn Right',
	7: 'Kick',
	8: 'Stand Up (if fallen over)'
}

pygame.init()
pygame.joystick.init()

joy = JoystickListener(JOYSTICK)

while 1:
	for e in pygame.event.get():
		if e.type in events:
			events[e.type](e)

	#REPLACE THE FOLLOWING WITH YOUR NAOQI STUFF.
	if joy.state != 0:
		print descriptions[joy.state]

	#what 'state' corresponds to what joystick axis/button
	#is in maps{}
