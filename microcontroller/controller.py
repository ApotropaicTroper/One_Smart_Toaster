
from timer import CookTimer

class ToasterController(object):

	loaded = False
	instructions = None
	timer = None

	def __init__(self, instructions):
		self.instructions = instructions
		self.timer = CookTimer()

	def start(self):
		''' Begin cooking '''
		self.lower_platform()
		self.set_heating_element()
		self.timer.set(self.instructions.cook_time)
		self.timer.start()

	def end(self):
		''' Cooking has finished '''
		self.set_heating_element()
		self.timer.clear()
		self.instructions.clear()
		self.raise_platform()

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
