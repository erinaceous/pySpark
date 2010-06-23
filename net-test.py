#!/usr/bin/python -OO

import net
from pygame import time
#psyco.full()

#r = net.rcReceiver('192.168.212.201')
r = net.rcReceiver()
c = time.Clock()
s = r.getSocket()

r.start()
#s.send(net.defaults.initStr+'(he1 -1 0)')

he1 = -2

running = True
#while running == True:
#	print r.buffer
#	try:
#		if he1 < 0:
#			he1 = 2
#		else:
#			he1 = -2
#		s.send('(he1 '+str(he1)+' 0)')
#	except KeyboardInterrupt:
#		r.stop()
#		r.join()
#		running = False
#	c.tick(1)

while running == True:
	try:
		s.send(raw_input(">\t"))
		c.tick(1)
	except KeyboardInterrupt:
		r.stop()
		running = False
		quit()
	c.tick(1)
