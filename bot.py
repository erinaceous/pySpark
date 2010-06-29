import net,motion
from time import clock as ctime

class Nao:
	def __init__(self,joystick,id=0,team='blue',socket=None):
		if socket != None:
			self.s = socket
		
		joystick.init()
		self.curtime,self.pastime,self.interval = ctime(),ctime(),40
		self.joystick = joystick
		self.map = maps[joystick.get_name()]
		self.state = 0
		self.init = 0
		self.idle = False
		self.moving = False
		self.speed = 0
		self.id = id
		self.team = team
		self.m = {
			1: motion.RCSSMotion('bots/nao/Forwards.rcss')
#			1: motion.WebotsMotion('bots/nao/joints.txt','bots/nao/Forwards.motion'),
#			2: motion.WebotsMotion('bots/nao/joints.txt','bots/nao/Backwards.motion'),
#			3: motion.WebotsMotion('bots/nao/joints.txt','bots/nao/SideStepLeft.motion'),
#			4: motion.WebotsMotion('bots/nao/joints.txt','bots/nao/SideStepRight.motion'),
#			5: motion.WebotsMotion('bots/nao/joints.txt','bots/nao/TurnLeft40.motion'),
#			6: motion.WebotsMotion('bots/nao/joints.txt','bots/nao/TurnRight40.motion'),
#			9: motion.WebotsMotion('bots/nao/joints.txt','bots/nao/Shoot.motion'),
#			11: motion.WebotsMotion('bots/nao/joints.txt','bots/nao/HeadShake.motion')
		}
		self.joints = motion.WebotsMotion('bots/nao/joints.txt','bots/nao/Idle.motion').get_frame(0)
		#get the names of all the joints so we can reset all their velocities when needs be.
		#need to use a .motion file that defines Nao's 22-ish joints. Forwards.motion doesn't.

	def __del__(self):
		print 'Deleting Bot, ID:',self.id
		self.s.send('(kill (unum '+str(self.id)+'))')
		self.s.close()

	def quit(self):
		self.__del__()

	def reset_joints(self):
		buffer = ''
		if self.moving == True:
			frame = self.m[1].reset_motion()
			if (self.curtime-self.pastime)*1000 > self.interval:
				self.moving = False
				self.pastime = ctime()
		else:
			# Set all velocities to zero
			frame = self.m[1].reset_motion()
		for joint in frame:
			buffer += '('+joint+' 0)'
		return buffer

	def set_joints(self,frame):
		buffer = ''
		frametime = 40-time.get_rawtime()

		for joint in frame:
#			if frametime != 0: frame[joint] = frame[joint]/frametime #stop ZeroDivisionError
			buffer += '('+joint+' '+str(round(frame[joint],4))+')'
		return buffer

	def think(self):
		self.curtime = ctime()
		if self.init == 0:
			if self.state == 10:
				self.s.send('(scene rsg/agent/nao/nao.rsg)')
				self.init = 1
		elif self.init == 1:
				buffer = ''
				buffer += '(init unum '+str(self.id)+')(TeamName '+self.team+'))'
				buffer += self.reset_joints()
				self.s.send(buffer)
				self.init = 2
				print 'Nao',self.id,'fully initialized'
		elif self.init == 2:
			if self.state in self.m.keys():
				self.s.send(self.set_joints(self.m[self.state].next(times=4)))
				self.idle = False
				self.moving = True
			elif self.state == 0:
				if self.idle == False:
					self.s.send(self.reset_joints())
#					for m in self.m:
#						self.m[m].index = 0 #reset all animations to their first frame.
					self.idle = True
			elif self.state == 10:
				self.s.send(self.reset_joints()+'(beam 0 0 0)')
				self.state = 0
				self.idle = True
			global stats
			statename = descriptions[self.state]
#			stats += "\033[1;31;40m"+statename+' '*(10-len(statename))+"\033[0m\t"
		
	def idle(self,e):
		if e.dict['button'] in self.map['buttons'] and self.idle == False:
			self.state = 0
			self.idle = True

	def action(self,e):
		map = self.map['buttons']
		for i in map.keys():
			if e.dict['button'] == map[i]:
				self.state = i

	def move(self,e):
		map = self.map['axis']
		self.state = 0
		for i in map.keys():
			if e.dict['axis'] == map[i][0]:
				if round(e.dict['value']) == map[i][1]:
					self.state = i
					self.speed = round(abs(e.dict['value']),2)

def idle(e,mainloop=None):
	if e.dict['joy'] <= len(naos):
		Nao.idle(naos[e.dict['joy']],e) 

def move(e,mainloop=None):
	if e.dict['joy'] <= len(naos):
		Nao.move(naos[e.dict['joy']],e)

def action(e,mainloop=None):
	if e.dict['joy'] <= len(naos):
		Nao.action(naos[e.dict['joy']],e)

def endloop(e,mainloop=None):
	print 'pressed'
	if pygame.key.get_pressed() == pygame.K_Q:
		mainloop.quit()
