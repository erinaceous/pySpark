#!/usr/bin/python -OO
# Parser class - read SimSpark .motion files into a format that RCSS can understand.
# Takes .motion files and 'joint.txt's, which define the maximum/minimum amount each
# of a robot's limbs can move in Webots & RCSS, and the names of the joints in both.

class Motion:
	def __init__(self,limits=None,motion=None):
		self.rcssjoints = {}
		if limits:
			self.set_limits(limits)
		if motion:
			self.set_motions(motion)
		self.index = -1

	def set_limits(self,file):
		tmpfile = open(file)
		limits = {}
		for line in tmpfile:
			if line[0] == chr(35): continue #if line starts with a hash, it's a comment.
			tmp = line.split("\t\t")
			tmp[0] = tmp[0].split(',')
			limits[tmp[0][0]] = (round(float(tmp[0][1]),2),round(float(tmp[0][2][0:-1]),2))
			if tmp[1] not in ['',"\n"]:
				tmp[1] = tmp[1].split(",")
				if tmp[1][2][-1] == "\n": tmp[1][2] = tmp[1][2][:-1]
				self.rcssjoints[tmp[0][0]] = tmp[1]
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

	def get_frame(self,frame=0):
		tmp = {}
		for i,key in enumerate(self.motions):
			try:
				joint = self.motions[key][frame]
				if joint[-1] == "\n": joint = joint[:-1]
				tmp[self.rcssjoints[key][0]] = float(joint*)
			except IndexError:
				return {}
		return tmp

	def next(self):
		if self.index < self.get_length():
			self.index += 1
		else:
			self.index = 0
		return self.get_frame(self.index)

	def prev(self):
		if self.index > 0:
			self.index -= 1
		else:
			self.index = 0
		return self.get_frame(self.index)

	def get_length(self):
		return len(self.motions[self.motions.keys()[0]])

if __name__=='__main__':
	nao = Motion('bots/nao/joints.txt','bots/nao/Forwards.motion')
#	nao.set_limit('LAnkleRoll',(0,-13.37))
	for i in range(100):
		frame = nao.next()
		print frame
