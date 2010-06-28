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
			2: motion.Motion('bots/nao/joints.txt','bots/nao/Forwards.motion')
		}
		self.currentjoint = 0
		self.jointname = self.m[1].get_joints()[0]
	
	def reset_joints(self):
		buffer = ''
		frame = self.m[1].get_frame(0)
		for joint in frame:
			buffer += '('+joint+' 0)'
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
			if self.state == 1:
				frame = self.m[1].next()
				buffer = ''
				for joint in frame:
					buffer += '('+joint+' '+str(round(frame[joint]/(40-time.get_fps()),3))+')'
				self.s.send(buffer)
			elif self.state == 0:
				if self.idle == False:
					self.s.send(self.reset_joints())
					self.idle = True
			elif self.state == 10:
				self.s.send(self.reset_joints()+'(beam 0 0 0)')
		
	def idle(self,e):
		if e.dict['button'] in self.map['buttons']:
#			self.state = 0
			pass

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
		Nao.idle(naos[e.dict['joy']],e) 

def move(e):
	if e.dict['joy'] <= len(naos):
		Nao.move(naos[e.dict['joy']],e)

def action(e):
	if e.dict['joy'] <= len(naos):
		Nao.action(naos[e.dict['joy']],e)
