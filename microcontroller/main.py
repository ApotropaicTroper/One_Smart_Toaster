
import socket as sock
import threading as thread

from controller import ToasterController
from instruction import CookInstructions


def listen(instructions):
	''' this thread listens for messages from the app '''
	while True:
		input('> ')
		'''
		Upon receiving confirmation, call instructions.confirm()
		Upon receiving stop order, call instructions.stop()
		'''
		...

def execute(controller, instructions):
	''' Loop until shut off '''
	while True:
		instructions.confirmed.wait() # have the instructions been confirmed? wait until this is true
		controller.start()
		instructions.stopped.wait(timeout=instructions.cook_time) # wait until user signals to stop, up to the length of the timer
		controller.end()


''' For future reference, using end='\r' allows printing over same line '''
if __name__ == '__main__':
	# one instruction structure for each toaster slot
	instructions = CookInstructions()
	controller = ToasterController(instructions)
	# this thread will listen for messages from the app
	listener = thread.Thread(target=listen, name='listener', args=(instructions,), daemon=True)
	listener.start()
	execute = thread.Thread(target=execute, name='executor', args=(controller, instructions))
	execute.start()
	listener.join()
	execute.join()
