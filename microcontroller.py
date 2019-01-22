Microcontroller code


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

	cook_time = 0
	start_time = 0

	def __init__(self):
		self.clear()
	
	def set(self, cook_time):
		''' set how long the timer should run for '''
		self.clear()
		self.cook_time = cook_time
	
	def start(self):
		self.start_time = time.time()

	def finished(self):
		''' Is the timer still going? '''
		elapsed_time = time.time() - self.start_time
		# returns true if timer hasn't been started, unless system clock changed
		return self.elapsed_time > self.cook_time
	
	def clear(self):
		self.cook_time = 0
		self.start_time = 0


class CookInstruction(object):
	''' Manage access to cooking instruction, and carry it out '''
	
	cook_time = 0
	cook_temp = 0
	mutexes = None
	timer = None
	confirmed = None
	stop = None

	def __init__(self, cook_time=0, cook_temp=0)
		self.timer = CookTimer()
		self.cook_time = cook_time
		self.cook_temp = cook_temp
		self.stop = thread.Event()
		self.confirmed = thread.Event() # what is the initial state of a threading.Event object?
		self.mutexes = [thread.Lock(), thread.Lock()] # might want to split so no list is created
	
	def write_time(value):
		if value < 0:
			''' Report time error '''
			return
		with mutexes[0]:
			self.cook_time = value
	
	def write_temperature(value):
		if value < 0:
			''' Report temperature error '''
			return
		with mutexes[1]:
			self.cook_temp = value
	
	def read_time():
		with mutexes[0]:
			return self.cook_time
	
	def read_temperature():
		with mutexes[1]:
			return self.cook_temp
	
	def confirm():
		self.confirmed.set()
	
	def halt():
		self.stop.set()
		self.confirmed.clear()
	
	def clear():
		write_time(0)
		write_temperature(0)
		self.confirmed.clear()
		self.stop.clear()
		self.timer.clear()

	def execute():
		# lower platform
		# set stuff about temperature
		self.timer.set(self.read_time)
		self.timer.start()
		while not self.timer.finished:
			# check timer
			# 	if timer has finished, stop cooking
			# check temperature
			# 	alter something
			...
		self.clear()




def listen(instructions):
	''' this thread listens for messages from the app '''
	''' For the time being, let's say this is where it gets messages.
		For testing purposes, I'll substitute with input() '''
	while True:
		time = input('Time (sec): ')
		temperature = input('Temperature (ºF): ')
		slot = int(input('Slot? 0/1'))
		assert slot == 0 or slot == 1, 'Slot doesn\'t exist'
		instructions[slot].write_time(time)
		instructions[slot].write_temperature(temperature)
		if input('Confirm? > '):
			instructions[slot].confirm()


def execute(instruction):
	''' this thread carries out instructions received from the app '''
	while True:
		instruction.confirmed.wait()
		instruction.execute()

if __name__ == '__main__':
	# one instruction structure for each toaster slot
	instructions = [CookInstruction(), CookInstruction()]
	# this thread will listen for messages from the app
	listener = thread.Thread(target=listen, name='listener', args=instructions, daemon=True)
	listener.start()
	execute_0 = thread.Thread(target=execute, name='executor_0', args=instruction[0])
	execute_1 = thread.Thread(target=execute, name='executor_1', args=instruction[1])
	execute_0.start()
	execute_1.start()
	listener.join()
	execute_0.join()
	execute_1.join()





