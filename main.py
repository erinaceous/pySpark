#!/usr/bin/python -OO

#import psyco
#psyco.full()

host = ''
port = 3100
fps = 25 #how many times the main loop runs a second (or tries to).

import pygame,net,sys
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
		joy = pygame.joystick.Joystick(i)
		if joy.get_name() in maps:
			sockets.append(net.rcSocket(host,port))
			naos.append(Nao(joy,i+1,'blue',sockets[i]))
			print 'Enabled Joystick',joy.get_name(),'For Nao',i+1
		else:
			print 'Joystick',joy.get_name(),'has no map'
except pygame.error:
	print 'No Joysticks found.',pygame.get_error()
	quit()

recv = net.rcDiscarder(sockets) #rcReceiver reads data from a LIST of sockets.
recv.start() #it's also a thread, so start it. This is just to keep RCSS
#accepting our own commands. We don't do anything with the data.

def main():
	global running
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

		stats = '\033[30;43m Bots: '+str(len(naos))+"\tFPS: "+str(time.get_fps())+" \033[0m\t"
		sys.stdout.write("\r{0}".format(stats))
		sys.stdout.flush()
		time.tick(fps) #run the main loop no more than
		#X frames per second - saves a bunch of CPU
		#time, and RCSS starts to block commands sent
		#if they're sent too fast (it seems).

if __name__=='__main__': main()
