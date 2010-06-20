import socket,threading
from binascii import a2b_uu,unhexlify
from time import sleep

class defaults:
	host = ''
	port = 3100
	initStr = '(scene rsg/agent/nao/nao.rsg)(init (unum 0)(TeamName NaoRobot))'

class rcReceiver(threading.Thread):
	def __init__(self,host=defaults.host,port=defaults.port,window=1024):
		threading.Thread.__init__(self)
		self.sock = rcSocket(host,port)
		self.window = window
		self.buffer = ''
		self.running = True

	def getSocket(self):
		return self.sock

	def stop(self):
		self.running = False
		self.sock.close()

	def recv(self):
		buffer = ''
		while len(buffer) < self.window:
			chunk = self.sock.sock.recv(self.window-len(buffer))
			if chunk == '': break
			buffer += chunk
		return buffer

	def run(self):
		while self.running == True:
			self.buffer = self.recv()
			sleep(0)

class rcSocket:
	def __init__(self,host=defaults.host,port=defaults.port):
		self.addr = (host,port)
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.connect(self.addr)

	def close(self):
		self.sock.shutdown(1)
		self.sock.close()

	def send(self,string):
		length = str(hex(len(string)))[2:]
		length = '0'*(8-len(length))+length
		length = unhexlify(length)
		self.sock.send(length+string)
