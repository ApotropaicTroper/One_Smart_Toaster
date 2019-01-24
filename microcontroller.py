'''
parts to control:
	cooling fan
	heating element
	timer
	slot mechanism
Use case:
- User inserts food, then sends instruction
					OR
  User sends instruction, then inserts food
- Toaster lowers food into position
- Toaster cooks food using provided instructions
- Toaster raises food out of position
One thread for each slot. Two slots, so two threads
A separate thread should listen for instructions from user. Write to data structure which the main code reads from? Its writing takes priority over main program's reading
Instruction validity check:
	Is indicated timer value positive?
	  N: report entry error
	Is indicated temperature value greater than some threshold?
	  N: report low temperature
Cook food:
	loop until timer is no longer positive:
		if abort,
			set timer to 0
			disable heating mechanism
			exit loop
		read temperature
		if temperature is too low,
			increase power to heating element
		if temperature is too high,
			decrease power to heating element
When instructions/confirmation received:
	Are instructions valid?
	 N: report
	 Y: Note that valid instructions received
When food inserted:
	Note that food inserted
If food inserted and valid instructions received,
	lower slot mechanism
		wait for mechanism to complete
	set heating element
	enable cooling fan
	set timer
	cook food
	set timer to 0
	disable heating element
	disable cooling fan
	raise slot mechanism
		wait for mechanism to complete
'''




# for elapsed wall-clock time: time.time()
#   returns time in seconds (as float) since Unix epoch, based on system clock
import time
import threading as thread

class CookTimer(object):
	''' countdown timer '''

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
		return self.remaining_time >= 0

	def set(self, cook_time):
		''' Set how long the timer should run for '''
		self.clear()
		self.cook_time = cook_time
	
	def start(self):
		self.start_time = time.time()
		self.running = True
	
	def clear(self):
		self.cook_time = 0
		self.start_time = 0
		self.running = False


class CookInstructions(object):
	''' Manage access to cooking instructions '''
	
	_cook_time, _cook_temp = 0,0
	time_mutex, temp_mutex = None,None
	confirmed, stop = None, None

	def __init__(self, cook_time=0, cook_temp=0):
		self.mutex_time = thread.Lock()
		self.mutex_temp = thread.Lock()

		self.cook_time = cook_time
		self.cook_temp = cook_temp
		self.stop = thread.Event()
		self.confirmed = thread.Event() # what is the initial state of a threading.Event object?

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
	
	def halt(self):
		self.stop.set()
		self.confirmed.clear()
	
	def clear(self):
		self.cook_time = 0
		self.cook_temperature = 0
		self.confirmed.clear()
		self.stop.clear()


class ToasterController(object):

	loaded = False
	instructions = None
	timer = None

	def __init__(self, instructions):
		self.timer = CookTimer()
		self.instructions = instructions

	def start(self):
		self.lower_platform()
		self.set_heating_element()
		self.timer.set(instructions.cook_time)
		self.timer.start()

	def execute(self):
		'''
		Have the instructions been confirmed?
		If so,:
			lower platform
			set temperature
			set timer
			loop:
				run until timer finishes or abort signal receives
				has timer finished?
				has abort signal been received?
			clear temperature
			clear timer
			raise platform

		'''		
		self.instructions.confirmed.wait()
		while True:
			...
		...



	def lower_platform(self):
		...
	def raise_platform(self):
		...
	def set_heating_element(self):
		...
	def get_heating_element(self):
		...


def listen(instructions):
	''' this thread listens for messages from the app '''
	''' For the time being, let's say this is where it gets messages.
		For testing purposes, I'll substitute with input() '''
	while True:
		...
		# time = int(input('Time (sec)\n> '))
		# temperature = int(input('Temperature (°F)\n> '))
		# instructions.write_time(time)
		# instructions.write_temperature(temperature)
		# if input('Confirm? > '):
		# 	instructions.confirm()

def execute(instructions):
	''' this thread carries out instructions received from the app '''
	while True:
		...
		# instructions.confirmed.wait()
		# instructions.execute()

if __name__ == '__main__':
	# one instruction structure for each toaster slot
	instructions = CookInstructions()
	controller = ToasterController(instructions)
	# this thread will listen for messages from the app
	listener = thread.Thread(target=listen, name='listener', args=(instructions,), daemon=True)
	listener.start()
	execute = thread.Thread(target=execute, name='executor', args=(instructions,))
	execute.start()
	listener.join()
	execute.join()
