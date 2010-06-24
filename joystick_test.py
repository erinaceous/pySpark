#!/usr/bin/python -OO
import pygame
from pygame.locals import *
pygame.init()
pygame.joystick.init()

joysticks = []
clock = pygame.time.Clock()
running = True

for i in range(pygame.joystick.get_count()):
	joysticks.append(pygame.joystick.Joystick(i))
	joysticks[i].init()
	print 'Enabled',joysticks[i].get_name()

while running:
	try:
		for e in pygame.event.get():
			print e.dict
	except KeyboardInterrupt:
		del running
		quit()
	clock.tick(60)
