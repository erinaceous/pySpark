#!/usr/bin/python -OO

import psyco
psyco.full()

import pygame,net,bot
from pygame.locals import *
execfile('input_maps.py')

r = net.rcReceiver()
s = r.getSocket() #return the actual socket used
#as an object, so we can send() things on it

r.start() #rcReceiver is actually a class of thread.
#When running it just recv()'s from the open socket,
#so RCSS keeps accepting commands from the client.
#all recv()'d data can be retrieved from the var
#r.buffer, but we have no reason to retreive the
#data in this case.

pygame.display.init()
pygame.joystick.init()

time = pygame.time.Clock()
running = 1
naos = []

try:
	for i in range(pygame.joystick.get_count()):
		naos.append(bot.Nao(pygame.joystick.Joystick(i),i,r))
		print 'Enabled Joystick',naos[i].joystick.get_name(),'For Nao',i
except pygame.error:
	print 'No Joysticks found.',pygame.get_error()
	quit()

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

		map(bot.Nao.think,naos)

	except KeyboardInterrupt:
		r.stop() #the net thread doesn't seem to
		#end properly, why is this?
		del running
		quit()

	time.tick(20) #run the main loop no more than
	#20 frames per second - saves a bunch of CPU
	#time, and RCSS starts to block commands sent
	#if they're sent too fast (it seems).
