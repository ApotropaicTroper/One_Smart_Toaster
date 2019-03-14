
from timer import CookTimer
from RPi import GPIO

# total of 40 I/O pins

class ToasterController(object):

	loaded = False
	instructions = None
	timer = None


	heating_element_channel = 0
	fan_channel = 1
	platform_channel = 2

	# Requires 3 pins
	''' Temperature channels '''
	'''
	To read temperature, should probably use SPI
		MISO to DO
		CS0 to CS
		SCLK to CLK
https://cdn-learn.adafruit.com/downloads/pdf/max31855-thermocouple-python-library.pdf


	temp_CLK_channel = 28 	# output; clock
	temp_DO_channel = 29	# input; data out
	temp_CS_channel = 30	# output; chip select (time to read)
	'''

	def __init__(self, instructions):
		self.instructions = instructions
		self.timer = CookTimer()

		GPIO.setup(self.heating_element_channel, GPIO.OUT)
		GPIO.setup(self.fan_channel, GPIO.OUT)
		GPIO.setup(self.platform_channel, GPIO.OUT)

		GPIO.setup(self.temp_CLK_channel, GPIO.OUT)
		GPIO.setup(self.temp_DO_channel, GPIO.IN)
		GPIO.setup(self.temp_CS_channel, GPIO.OUT)



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
		GPIO.output(self.temp_CS_channel, GPIO.HIGH)





		GPIO.output(self.temp_CS_channel, GPIO.LOW)
		...
