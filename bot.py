import net

class Nao:
	def __init__(self,joystick,id=0,team='blue',socket=None):
		self.buffer = ''
		if socket != None:
			self.s = socket
		
		joystick.init()
		self.joystick = joystick
		self.map = maps[joystick.get_name()]
		self.state = 0
		self.init = 0
		self.speed = 0
		self.id = id
		self.team = team
		self.pos = teams[team][id]

	def think(self):
		self.buffer = ''
		if self.init == 1:
			print self.id,self.state,descriptions[self.state]
		if self.s != None:
			if self.state == 10:
				if self.init == 0:
					self.buffer = '(scene rsg/agent/nao/nao.rsg)'
					self.init = 1
				elif self.init == 1:
					self.buffer = '(init unum '+str(self.id)+')(TeamName '+self.team+'))'
					self.init = 2
			if self.init == 2:
				if self.state == 0:
					self.buffer += '(he1 0)(lae1 0)'
				else:
					if self.state == 1:
						self.pos[1] += 0.1
					elif self.state == 2:
						self.pos[1] -= 0.1
					elif self.state == 3:
						self.pos[0] += 0.1
					elif self.state == 4:
						self.pos[0] -= 0.1
					elif self.state == 5:
	#					self.pos[2] += 0.1
						self.buffer += '(he1 '+str(0.1+self.speed)+')'
					elif self.state == 6:
	#					self.pos[2] -= 0.1
						self.buffer += '(he1 '+str(-0.1-self.speed)+')'
					elif self.state == 7:
						self.buffer += '(lae1 '+str(0.1+self.speed)+')'
					elif self.state == 8:
						self.buffer += '(lae1 '+str(-0.1-self.speed)+')'
					if self.state in range(0,4):
						self.buffer += '(beam '+str(self.pos[0]*self.speed)+' '+str(self.pos[1]*self.speed)+' '+str(self.pos[2]*self.speed)+')'
			self.s.send(self.buffer)

	def state(self):
		if self.state != 0:
			print self.id,descriptions[self.state]

	def idle(self,e):
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
					self.speed = abs(e.dict['value'])

def idle(e):
	if e.dict['joy'] <= len(naos):
		Nao.idle(naos[e.dict['joy']],e)

def move(e):
	if e.dict['joy'] <= len(naos):
		Nao.move(naos[e.dict['joy']],e)

def action(e):
	if e.dict['joy'] <= len(naos):
		Nao.action(naos[e.dict['joy']],e)
