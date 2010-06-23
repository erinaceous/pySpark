#!/usr/bin/python -OO

#import psyco
#psyco.full()

host = ''
port = 3100

import pygame,net
from pygame.locals import *
execfile('bot.py')
execfile('maps.py')

pygame.display.init()
pygame.joystick.init()

time = pygame.time.Clock()
running = 1
naos = []

sockets = [] #RCSS controls agents on a per-socket basis, so let's create a pool of them.

try:
	for i in range(pygame.joystick.get_count()):
		sockets.append(net.rcSocket(host,port))
		naos.append(Nao(pygame.joystick.Joystick(i),i+1,'blue',sockets[i]))
		print 'Enabled Joystick',naos[i].joystick.get_name(),'For Nao',i+1
except pygame.error:
	print 'No Joysticks found.',pygame.get_error()
	quit()

recv = net.rcDiscarder(sockets) #rcReceiver reads data from a LIST of sockets.
recv.start() #it's also a thread, so start it. This is just to keep RCSS
#accepting our own commands. We don't do anything with the data.

while running:
	try:
		for e in pygame.event.get():
			if e.type in events:
				events[e.type](e)
				#events{} is defined in
				#joystick_maps.py; the
				#functions to run are the
				#vars and the keys are
				#the pygame events

		map(Nao.think,naos)

	except KeyboardInterrupt:
		recv.stop()
		del running
		quit()

	time.tick(10) #run the main loop no more than
	#10 frames per second - saves a bunch of CPU
	#time, and RCSS starts to block commands sent
	#if they're sent too fast (it seems).
