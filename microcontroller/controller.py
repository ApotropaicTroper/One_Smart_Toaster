import time

from timer import CookTimer
from RPi import GPIO

# total of 40 I/O pins

class ToasterController(object):

	loaded = False
	instructions = None
	timer = None


	# heating_element_channel = 0
	# fan_channel = 1
	# platform_spin_channel = 2
	# platform_direction_channel = 3

		# GPIO.setup(self.heating_element_channel, GPIO.OUT)
		# GPIO.setup(self.fan_channel, GPIO.OUT)
		# GPIO.setup(self.platform_channel, GPIO.OUT)


	# Requires 3 pins
	''' Temperature channels '''
	'''
Pins taken up:
	Buttons on:
	22
	27
	17

	Motor on:
	02
	03
	04

	Temperature on:
	08 (CS0)
	11 (CLK)
	09 (MISO)





	To read temperature, should probably use SPI
		MISO to DO
		CS0 to CS
		SCLK to CLK
https://cdn-learn.adafruit.com/downloads/pdf/max31855-thermocouple-python-library.pdf
https://github.com/doceme/py-spidev

	# output; clock
	# input; data out
	# output; chip select (time to read)
	'''
	temp_CLK_channel = 11
	temp_MISO_channel = 9
	temp_CS0_channel = 8


	def __init__(self, instructions):
		self.instructions = instructions
		self.timer = CookTimer()

		GPIO.setup(self.temp_CLK_channel, GPIO.OUT)
		GPIO.setup(self.temp_MISO_channel, GPIO.IN)
		GPIO.setup(self.temp_CS0_channel, GPIO.OUT)


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
		# Temperature output as 14-bit signed integer counting quarters of °C (i.e. +1 → 0.25°C; +4 → 1°C)
		temp = 0
		GPIO.output(self.temp_CS0_channel, GPIO.HIGH)
		for i in range(14):
			# pulse clock
			GPIO.output(self.temp_CLK_channel, GPIO.HIGH)
			GPIO.output(self.temp_CLK_channel, GPIO.LOW)
			# read data output
			temp = temp << 1
			temp += GPIO.input(self.temp_MISO_channel)
			# time.sleep(0.01)
		# output is signed int
		if temp >= 0b_10_0000_0000_0000:
			temp -= 0b_10_0000_0000_0000
		# not a bit shift; truediv is float division
		temp /= 4
		GPIO.output(self.temp_CS0_channel, GPIO.LOW)
		return temp




'''
temp (°C)	bits				int
+1600.00	01 1001 0000 0000	+6400
+1000.00	00 1111 1010 0000	+4000
 +100.75	00 0001 1001 0011	+ 403		
  +25.00	00 0000 0110 0100	+ 100
    0.00	00 0000 0000 0000	±   0
   -0.25	11 1111 1111 1111	-   1
   -1.00	11 1111 1111 1100	-   4		
 -250.00	11 1100 0001 1000	-1000
'''


