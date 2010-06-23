#!/usr/bin/python -OO

import net
from pygame import time
#psyco.full()

#r = net.rcReceiver('192.168.212.201')
s = [net.rcSocket()]
r = net.rcReceiver(s)
c = time.Clock()

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
		s[0].send(raw_input("1>\t"))
#		s[0].recv()
#		s[1].send(raw_input("2>\t"))
#		s[1].recv()
		c.tick(1)
	except KeyboardInterrupt:
		r.stop()
		running = False
		quit()
	c.tick(1)
