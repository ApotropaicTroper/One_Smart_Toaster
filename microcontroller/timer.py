
import threading as thread
import time

class CookTimer(object):
	''' Countdown timer '''

	cook_time = 0
	start_time = 0
	running = False

	def __init__(self):
		self.clear()

	@property
	def remaining_time(self):
		''' If the timer is counting down, how much time is left? '''
		if not self.running:
			return 0
		return self.cook_time - self.elapsed_time
	@property
	def elapsed_time(self):
		''' If the timer is counting down, how long has it been running? '''
		if not self.running:
			return 0
		return time.time() - self.start_time
	@property
	def finished(self):
		''' Has the timer reached 0? '''
		if not self.running:
			return True
		return self.remaining_time >= 0 # returns true if remaining time is exactly 0

	def minutes_seconds(self):
		''' return how much time is left as a tuple of minutes and seconds '''
		if not self.running:
			return None
		return divmod(self.remaining_time, 60)

	def set(self, cook_time):
		''' Set how long the timer should run for '''
		self.clear()
		self.cook_time = cook_time
	
	def start(self):
		''' Start the timer '''
		self.start_time = time.time()
		self.running = True
	
	def clear(self):
		''' Stop the timer and reset all settings '''
		self.cook_time = 0
		self.start_time = 0
		self.running = False
