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
		self.m = motion.Motion('bots/nao/joints.txt','bots/nao/Forwards.motion')
		self.currentjoint = 0
		self.jointname = self.m.get_joints()[0]

	def think(self):
		if self.init == 0:
			if self.state == 10:
				self.s.send('(scene rsg/agent/nao/nao.rsg)')
				self.init = 1
		elif self.init == 1:
				self.s.send('(init unum '+str(self.id)+')(TeamName '+self.team+'))')
				self.init = 2
		elif self.init == 2:
#			if self.state == 0 and self.idle == False: self.s.send('('+self.jointname+' 0)')
#			if self.state == 11:
#				try:
#					self.currentjoint -= 1
#					self.jointname = self.m.rcssjoints[self.currentjoint][0]
#				except IndexError:
#					self.currentjoint = 0
#					self.jointname = self.m.rcssjoints[0][0]
#				print self.jointname
#			elif self.state == 12:
#				try:
#					self.currentjoint += 1
#					self.jointname = self.m.rcssjoints[self.currentjoint][0]
#				except IndexError:
#					self.currentjoint = 0
#					self.jointname = self.m.rcssjoints[0][0]
#				print self.jointname
#			elif self.state == 1: self.s.send('('+self.jointname+' '+str(0.1+self.speed)+')')
#			elif self.state == 2: self.s.send('('+self.jointname+' '+str(-0.1-self.speed)+')')
#		if self.state in range(1,12):
#			self.idle = False
#		print self.init, self.state
			frame = self.m.next()
			buffer = ''
			for joint in frame:
				buffer += '('+joint+' '+str(frame[joint])+')'
			self.s.send(buffer)
		

	def idle(self):
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

def idle(e):
	if e.dict['joy'] <= len(naos):
		naos[e.dict['joy']].state = 0

def move(e):
	if e.dict['joy'] <= len(naos):
		Nao.move(naos[e.dict['joy']],e)

def action(e):
	if e.dict['joy'] <= len(naos):
		Nao.action(naos[e.dict['joy']],e)
