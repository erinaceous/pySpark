events = {
	#what events should be listened to,
	#and the functions they bind to (in bot.py)
	pygame.JOYAXISMOTION: bot.move,
	pygame.JOYBUTTONDOWN: bot.action,
	pygame.JOYBUTTONUP: bot.idle
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
			1: (1,-0.1,-2), #1: forward
			2: (1,0.1,2), #2: backward
			3: (0,-0.1,-2), #3: sidestep left
			4: (0,0.1,2), #4: sidestep right
			5: (3,-0.1,-2), #5: turn left
			6: (3,0.1,2), #6: turn right
		},
		"buttons": {
			7: 0, #7: kick
			8: 1 #8: stop all motions
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
	8: 'Stop All Motion'
}
