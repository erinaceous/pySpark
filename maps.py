events = {
	#what events should be listened to,
	#and the functions they bind to (in bot.py)
	pygame.JOYAXISMOTION: move,
	pygame.JOYBUTTONDOWN: action,
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
			5: (3,-1), #5: turn head left
			6: (3,1), #6: turn head right
			7: (4,-1), #7: left arm up
			8: (4,1), #8: left arm down
			9: (5,1) #9: kick
		},
		"buttons": {
			10: 1, #10: init
			11: 2 #11: shake head.
		}
	},
	"Logitech Logitech Attack 3":{
		"axis": {
			1: (1,-1),
			2: (1,1)
		},
		"buttons": {
			10: 0,
			#the next two are custom: cycle
			#through joint names on the bot
			11: 3, #go back a joint
			12: 4 #go forward a joint
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
	7: 'Left Arm Up',
	8: 'Left Arm Down',
	9: 'Kick',
	10: 'Create Bot (only done once)',
	11: 'User Assigned Function'
}

teams = {
	'blue':{
		1:[1,1,0],
		2:[2,2,0],
		3:[3,3,0],
		4:[-1,1,0]
	},
	'red':{
		1:[-1,-1,0],
		2:[-2,-2,0],
		3:[-3,-3,0],
		4:[1,-1,0]
	}
}
