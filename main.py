#!/usr/bin/python -OO

#import psyco
#psyco.full()

host = '192.168.60.7'
port = 3100
fps = 40 #how many times the main loop runs a second (or tries to).
#50hz or 50fps; 20ms (same as RCSS)

import pygame,net,sys,threading
from pygame.locals import *
execfile('bot.py')
execfile('maps.py')

pygame.init()

time = pygame.time.Clock()
running = 1
stats = ''
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

class mainloop(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def quit(self):
		for nao in naos:
			del nao
		global running
		del running

	def run(self): self.main()

	def main(self):
		global running
		global stats
		while running:
			active = 0
			for bot in naos:
				if bot.init == 2: active += 1

			stats = '\033[30;43m Bots: '+str(active)+"\tFPS: "+str(round(time.get_fps(),3))+" \033[0m\t"

			try:
				for e in pygame.event.get():
					if e.type in events:
						events[e.type](e,self)
						#events{} is defined in
						#joystick_maps.py; the
						#functions to run are the
						#vars and the keys are
						#the pygame events
	
				map(Nao.think,naos)
	
			except KeyboardInterrupt:
				self.quit()

			sys.stdout.write("\r{0}".format(' '*80))
			sys.stdout.write("\r{0}".format(stats))
			sys.stdout.flush()
			
#			pygame.time.delay(20) #wait 20ms; keep in sync
			#with RCSS loop.

			time.tick_busy_loop(fps) #run the main loop no more than
			#X frames per second - saves a bunch of CPU
			#time, and RCSS starts to block commands sent
			#if they're sent too fast (it seems).

if __name__=='__main__': mainloop().start()
