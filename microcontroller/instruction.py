
import threading as thread

class CookInstructions(object):
	''' Manage access to cooking parameters '''
	
	_cook_time, _cook_temp = 0,0
	mutex_time, mutex_temp = None,None
	confirmed, stopped = None, None

	def __init__(self, cook_time=0, cook_temp=0):
		self.mutex_time = thread.Lock()
		self.mutex_temp = thread.Lock()

		self.cook_time = cook_time
		self.cook_temp = cook_temp
		# initial state  not set, as expected
		self.stoppped = thread.Event()
		self.confirmed = thread.Event()

	@property
	def cook_time(self):
		''' Read access for cooking time '''
		with self.mutex_time:
			return self._cook_time
	@cook_time.setter
	def cook_time(self, value):
		''' Write access for cooking time '''
		if value < 0:
			''' Report time error '''
			...
			return
		with self.mutex_time:
			self._cook_time = value

	@property
	def cook_temp(self):
		''' Read access for cooking temperature '''
		with self.mutex_temp:
			return self._cook_temp
	@cook_temp.setter
	def cook_temp(self,value):
		''' Write access for cooking temperature '''
		if value < 0:
			''' Report temperature error '''
			...
			return
		with self.mutex_temp:
			self._cook_temp = value
	
	def confirm(self):
		self.confirmed.set()
	
	def stop(self):
		self.stopped.set()
		self.confirmed.clear()
	
	def clear(self):
		self.cook_time = 0
		self.cook_temp = 0
		self.confirmed.clear()
		self.stopped.clear()
