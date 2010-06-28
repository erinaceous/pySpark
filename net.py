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
		self.running = True

	def stop(self):
		self.running = False
		self.sock.close()

	def recv(self,sock):
		buffer = ''
		while len(buffer) < self.window:
			chunk = sock.sock.recv(self.window-len(buffer))
			if chunk == '': break
			buffer += chunk
		return buffer

	def run(self):
		while self.running == True:
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

class rcDiscarder(rcReceiver):
	def run(self):
		while self.running == True:
			for sock in self.sockets:
				try: sock.sock.recv(8192)
				except socket.error: continue
			sleep(0)

class rcSocket:
	def __init__(self,host=defaults.host,port=defaults.port,window=4096):
		self.window = window
		self.buffer = ''
		self.addr = (host,port)
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.setblocking(0)
		try:
			self.sock.connect(self.addr)
		except socket.error:
			self.sock.connect(self.addr)

	def close(self):
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()

	def send(self,string):
		length = str(hex(len(string)))[2:]
		length = '0'*(8-len(length))+length
		length = unhexlify(length)
		self.sock.send(length+string)
		print string

	def recv(self):
                buffer = ''
                while len(buffer) < self.window:
                        chunk = self.sock.recv(self.window-len(buffer))
                        if chunk == '': break
                        buffer += chunk
                return buffer
