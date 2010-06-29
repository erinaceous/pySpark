import socket,select,threading
from binascii import unhexlify
from time import sleep

class defaults:
	host = ''
	port = 3100
	initStr = '(scene rsg/agent/nao/nao.rsg)(init (unum 0)(TeamName NaoRobot))'

class rcReceiver(threading.Thread):
	def __init__(self,sockets,window=4096):
		threading.Thread.__init__(self)
		self.sockets = sockets
		self.window = window
		self.buffer = ''

	def recv(self,sock):
		buffer = ''
		while len(buffer) < self.window:
			if sock.sock.type == 'tcp': chunk = sock.sock.recv(self.window-len(buffer))
			else: chunk = sock.sock.recvfrom(self.window-len(buffer))
			if chunk == '': break
			buffer += chunk
		return buffer

	def run(self):
		while len(self.sockets) > 0:
#			buffer = ''
#			for sock in self.sockets:
#				try: sock.buffer += sock.recv()
#				except socket.error: pass
#				sleep(0)
			input,output,exception = select.select(self.sockets,[],[])
			for sock in input:
				try: sock.buffer += sock.recv()
				except socket.error: continue
			sleep(0)
		print 'Socket list depleted; ending rcReceiver thread'

class rcDiscarder(rcReceiver):
	def run(self):
		while len(self.sockets) > 0:
			for sock in self.sockets:
				try:
					if sock.sock.type == 'tcp': sock.sock.recv(8192)
					else: sock.sock.recvfrom(8192)
				except socket.error: continue
			sleep(0)
		print 'Socket List depleted; ending rcDiscarder thread'

class rcSocket:
	def __init__(self,host=defaults.host,port=defaults.port,window=4096,type='tcp'):
		self.window = window
		self.buffer = ''
		self.addr = (host,port)
		self.type = type
		if self.type == 'tcp':
			self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.sock.setblocking(0)
			try:
				self.sock.connect(self.addr)
			except socket.error:
				sleep(0.5)
				self.sock.connect(self.addr)
		else:
			self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

	def close(self):
		if self.type == 'tcp':
			self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()

	def send(self,string):
		length = str(hex(len(string)))[2:]
		length = '0'*(8-len(length))+length
		length = unhexlify(length)
		try:
			if self.type == 'tcp':
				self.sock.send(length+string)
			else:
				self.sock.sendto(length+string, self.addr)
		except socket.error: pass
		print string

	def recv(self):
                buffer = ''
                while len(buffer) < self.window:
                        chunk = self.sock.recv(self.window-len(buffer))
                        if chunk == '': break
                        buffer += chunk
                return buffer
