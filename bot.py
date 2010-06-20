class Nao:
	def __init__(self,joystick,id,socket=None):
		self.r = socket
		if self.r != None:
			self.s = self.r.getSocket()
			self.s.send(net.defaults.initStr)
		
		joystick.init()
		self.joystick = joystick
		self.map = maps[joystick.get_name()]
		self.state = 0
		self.id = id
		self.pos = [0,0,0]

	def think(self):
		buffer = '(unum '+str(self.id)+')'
		if self.r != None:
			if self.state == 1:
				self.pos[1] += 0.1
			elif self.state == 2:
				self.pos[1] -= 0.1
			elif self.state == 3:
				self.pos[0] += 0.1
			elif self.state == 4:
				self.pos[0] -= 0.1
			elif self.state == 5:
				self.pos[2] += 0.1
			elif self.state == 6:
				self.pos[2] -= 0.1
			buffer += '(beam '+str(self.pos[0])+' '+str(self.pos[1])+' '+str(self.pos[2])+')'
			self.s.send(buffer)

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

def idle(e):
	if e.dict['joy'] <= len(naos):
		Nao.idle(naos[e.dict['joy']],e)

def move(e):
	if e.dict['joy'] <= len(naos):
		Nao.move(naos[e.dict['joy']],e)

def action(e):
	if e.dict['joy'] <= len(naos):
		Nao.action(naos[e.dict['joy']],e)
