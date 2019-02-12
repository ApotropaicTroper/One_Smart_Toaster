
from CookTimer import CookTimer



class ToasterController(object):

	loaded = False
	instructions = None
	timer = None

	def __init__(self, instructions):
		self.instructions = instructions
		self.timer = CookTimer()

	def start(self):
		self.lower_platform()
		self.set_heating_element()
		self.timer.set(self.instructions.cook_time)
		self.timer.start()

	def end(self):
		self.set_heating_element()
		self.timer.clear()
		self.instructions.clear()
		self.raise_platform()

	def execute(self):
		''' Loop until shut off '''
		while True:
			self.instructions.confirmed.wait() # have the instructions been confirmed? wait until this is true
			self.start()
			self.instructions.stopped.wait(timeout=self.timer.cook_time) # wait until user signals to stop, up to the length of the timer
			self.end()

	def lower_platform(self):
		self.loaded = True
		...
	def raise_platform(self):
		self.loaded = False
		...
	def set_heating_element(self):
		...
	def get_temperature(self):
		...
