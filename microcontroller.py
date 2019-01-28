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
		return self.remaining_time >= 0 # returns true if remaining time is exactly 0

	def to_string(self):
		''' return how much time is left as a tuple of minutes and seconds '''
		if not self.running:
			return (0,0)
		return divmod(self.remaining_time, 60)

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
	mutex_time, mutex_temp = None,None
	confirmed, stopped = None, None

	def __init__(self, cook_time=0, cook_temp=0):
		self.mutex_time = thread.Lock()
		self.mutex_temp = thread.Lock()

		self.cook_time = cook_time
		self.cook_temp = cook_temp
		self.stoppped = thread.Event()
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
	
	def stop(self):
		self.stopped.set()
		self.confirmed.clear()
	
	def clear(self):
		self.cook_time = 0
		self.cook_temp = 0
		self.confirmed.clear()
		self.stopped.clear()


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


def listen(instructions):
	''' this thread listens for messages from the app '''
	while True:
		'''
		Upon receiving confirmation, call instructions.confirm()
		Upon receiving stop order, call instructions.stop()
		'''
		...

''' For future reference, using end='\r' allows printing over same line '''
if __name__ == '__main__':
	# one instruction structure for each toaster slot
	instructions = CookInstructions()
	controller = ToasterController(instructions)
	# this thread will listen for messages from the app
	listener = thread.Thread(target=listen, name='listener', args=(instructions,), daemon=True)
	listener.start()
	execute = thread.Thread(target=controller.execute, name='executor')
	execute.start()
	listener.join()
	execute.join()
