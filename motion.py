#!/usr/bin/python -OO
# Parser class - read SimSpark .motion files into a format that RCSS can understand.
# Takes .motion files and 'joint.txt's, which define the maximum/minimum amount each
# of a robot's limbs can move in Webots & RCSS, and the names of the joints in both.

import math,time

def sign(number):
	if number < 0: return -1
	elif number == 0: return 0
	elif number > 0: return 1

class WebotsMotion:
	def __init__(self,limits=None,motion=None,times=1,timestep=40,speed=1):
		self.precomputed = []
		self.rcssjoints = {}
		self.length = 0
		self.index = 0
		self.speed = speed
		self.times = times
		self.timestep = timestep
		if limits:
			self.set_limits(limits)
		if motion:
			self.set_motions(motion)
		for i in range(self.length):
			self.precomputed.append(self.get_frame(i,times,timestep))

	def set_limits(self,file):
		tmpfile = open(file)
		limits = {}
		for line in tmpfile:
			if line[0] == chr(35): continue #if line starts with a hash, it's a comment.
			if line[-1] == "\n": line = line[:-1] #remove newline chars

			tmp = line.split("\t")
			for i,part in enumerate(tmp):
				if part == '': del tmp[i]

			tmp[0] = tmp[0].split(',')
			limits[tmp[0][0]] = (float(tmp[0][1]),float(tmp[0][2]))
			if tmp[1] not in ['',"\n"]:
				tmp[1] = tmp[1].split(",")
				self.rcssjoints[tmp[0][0]] = [tmp[1][0],abs(int(tmp[1][1])-int(tmp[1][2]))]
		self.limits = limits

	def set_limit(self,joint,tuple):
		try: self.limits[joint]
		except KeyError:
			print 'No such joint'
			return
		else:
			self.limits[joint] = tuple

	def set_motions(self,file):
		tmpfile = open(file)
		motions = {}
		for line in tmpfile:
			tmp = line.split(',')
			if line[0] == chr(35): #lines starting with hashes define joints used in motion.
				for element in tmp:
					if element in self.limits:
						motions[element] = []
			else:
				self.length += 1
				keys = motions.keys()
				for i,element in enumerate(tmp):
					if i>=2: #first two variables seem to be junk
						motions[keys[i-3]].append(tmp[i])
		self.motions = motions

	def get_joints(self,type='rcss'):
		joints = []
		for i,key in enumerate(self.limits):
			if type == 'webots': joints[:] = key
			elif type == 'rcss': return self.rcssjoints[key][0]
		return joints

#	def get_frame(self,frame=0,times=1,timestep=40):
#		tmp = {}
#		for key in self.motions:
#			joint = self.motions[key][frame]
#			if frame > 0:
#				lastframe = math.degrees(float(self.motions[key][frame-1]))
#				velocity = ((math.degrees(float(joint))-lastframe)/timestep)*self.rcssjoints[key][1]
#			else:
#				velocity = math.degrees(float(joint))*self.rcssjoints[key][1]
#			tmp[self.rcssjoints[key][0]] = velocity/times
#		return tmp

	def get_frame(self,frame=0,times=None,timestep=None,speed=None):
		if times == None: times = self.times
		if timestep == None: timestep = self.timestep
		if speed == None: speed = self.speed

		timestep = float(timestep)/1000 #timestep is in seconds not ms

		tmp = {}
		for key in self.motions:
			pos = float(self.motions[key][frame])
			maxaccel = 0
			if frame < self.length-1: nextpos = float(self.motions[key][frame+1])
			else: nextpos = 0
			velocity = self.speed*(nextpos-pos)
			if abs(velocity) > self.limits[key][1]:
				velocity = sign(velocity) * self.limits[key][1]
			if maxaccel != -1:
				acceleration = (velocity-pos)/timestep
			if abs(acceleration) > maxaccel:
				acceleration = sign(acceleration)*maxaccel
			velocity = (pos+acceleration*timestep)/times
			tmp[self.rcssjoints[key][0]] = velocity
		return tmp

	def next(self,times=1,frame=None):
		if frame != None:
			index = frame
		else:
			index = self.index

		if index < self.get_length():
			index += 1/times
		else:
			index = 0

		if frame == None: self.index = index
		return self.get_frame(int(index),times,timestep=self.timestep)
#		return self.precomputed[self.index]

	def prev(self,times=1):
		if self.index == 0:
			self.index = self.get_length()
			return self.get_frame(0)
		if self.index > 0:
			self.index -= 1/times
		else:
			self.index = self.get_length()
		return self.get_frame(self.index,times,timestep=self.timestep)
#		return self.precomputed[self.index]

	def get_length(self):
		return self.length-1

class RCSSMotion:
	def __init__(self,motion=None,speed=1,interval=40):
		self.interval = interval
		self.curtime = time.clock()
		self.pastime = time.clock()
		self.joints = []
		self.internal = {}
		self.index = -1
		self.speed = speed
		self.length = 0

		if motion != None:
			self.motion = self.set_motion(motion)

	def set_motion(self,file):
		file = open(file)
		motion = {}		

		for line in file:
			if line[-1] == "\n": line = line[:-1]

			if line[0] == chr(35): #ignore comments
				continue
			elif line[0] == '@':
				self.joints = line[1:].split(',')
				for joint in self.joints:
					motion[joint] = []
					self.internal[joint] = 0
			else:
				self.length += 1
				tmp = line.split(',')
				for i,joint in enumerate(self.joints):
					motion[joint].append(tmp[i])
		return motion

	def reset_motion(self):
		tmp = {}
		for joint in self.motion.keys():
			tmp[joint] = -self.internal[joint]
		return tmp

	def get_frame(self,frame=0):
		tmp = {}
		for joint in self.motion.keys():
			tmp[joint] = float(self.motion[joint][frame])
			self.internal[joint] += float(self.motion[joint][frame])
		return tmp

	def next(self,times=1,frame=None):
		if frame != None:
			return self.get_frame(self,frame)
		else:
			tmp = self.get_frame(int(self.index))
			if (self.curtime-self.pastime)*1000 > self.interval:
				if self.index < self.length-1:
					self.index += (float(1)/times)
				else:
					self.index = 0
				self.pastime = time.clock()
		print self.pastime,self.curtime,self.curtime-self.pastime,(self.curtime-self.pastime)*1000
		self.curtime = time.clock()
		return tmp

if __name__=='__main__':
	nao = RCSSMotion('bots/nao/Forwards.rcss')
	for i in range(30):
		print nao.next(3)

#	for i in range(100):
#		frame = nao.next()
#		print frame

#	nao = WebotsMotion('bots/nao/joints.txt','bots/nao/Forwards.motion')
#	nao.set_limit('LAnkleRoll',(0,-13.37))
#	for i in range(100):
#		frame = nao.next()
#		print frame
