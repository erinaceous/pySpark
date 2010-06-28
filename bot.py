import net,motion

class Nao:
	def __init__(self,joystick,id=0,team='blue',socket=None):
		if socket != None:
			self.s = socket
		
		joystick.init()
		self.joystick = joystick
		self.map = maps[joystick.get_name()]
		self.state = 0
		self.init = 0
		self.idle = False
		self.speed = 0
		self.id = id
		self.team = team
		self.pos = teams[team][id]
		self.m = {
			1: motion.Motion('bots/nao/joints.txt','bots/nao/Forwards.motion'),
			2: motion.Motion('bots/nao/joints.txt','bots/nao/Backwards.motion'),
			3: motion.Motion('bots/nao/joints.txt','bots/nao/SideStepLeft.motion'),
			4: motion.Motion('bots/nao/joints.txt','bots/nao/SideStepRight.motion'),
			5: motion.Motion('bots/nao/joints.txt','bots/nao/TurnLeft40.motion'),
			6: motion.Motion('bots/nao/joints.txt','bots/nao/TurnRight40.motion'),
			9: motion.Motion('bots/nao/joints.txt','bots/nao/Shoot.motion')
		}
		self.joints = motion.Motion('bots/nao/joints.txt','bots/nao/Idle.motion').get_frame(0)

	def __destroy__(self):
		print 'Deleting Bot, ID:',self.id
		self.sock.close()

	def reset_joints(self):
		# Set all velocities to zero
		buffer = ''
		frame = self.joints
		for joint in frame:
			buffer += '('+joint+' 0)'
		return buffer

	def set_joints(self,frame):
		buffer = ''
		frametime = 40-time.get_rawtime()

		for joint in frame:
			if frametime != 0: frame[joint] = frame[joint]/frametime #stop ZeroDivisionError
			buffer += '('+joint+' '+str(round(frame[joint],4))+')'
		return buffer

	def think(self):
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
		elif self.init == 2:
			if self.state in self.m.keys():
				self.s.send(self.set_joints(self.m[self.state].next(2)))
				self.idle = False
			elif self.state == 0:
				if self.idle == False:
					self.s.send(self.reset_joints())
					self.idle = True
			elif self.state == 10:
				self.s.send(self.reset_joints()+'(beam 0 0 0)')
				self.state = 0
				self.idle = True
			global stats
			statename = descriptions[self.state]
			stats += "\033[1;31;40m"+statename+' '*(10-len(statename))+"\033[0m\t"
		
	def idle(self,e):
		if e.dict['button'] in self.map['buttons']:
			self.state = 0

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
