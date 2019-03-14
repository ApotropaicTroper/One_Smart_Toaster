import socket
import threading as thread
from RPi import GPIO

from controller import ToasterController
from instruction import CookInstructions
#from Server2 import ServerSetup

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
host = '' # Get local machine name
port = 12345  # Reserve a port for your service.
all_data = 0;
print(host)
s.bind((host, port))  # Bind to the port

try:
	s.listen(1)  # Now wait for client connection.
except timeout: 
	print("Server Timed out...closing socket")
	s.close()
	
while True:
	try:
		c, addr = s.accept()  # Establish connection with client.
		print("Server Was Setup!")
		print('Got connection from', addr)
		output = 'Thank you for connecting'
		c.sendall(output.encode('utf-8'))
		data = c.recv(12345).decode()	 #data is accepted in a byte stream
		all_data = data.split(' ', 1)   #split the data coming in into an array (0 is cook time, 1 is cook temp)
		break;
	except socket.error:
		print("An error has occurred... closing connection to client")
		print("...Closing socket")
		c.close()
	#finally:
	#c.shutdown(socket.SHUT_RDWR)
		

#def recieve_data(instructions):
#   try:
#	 #Recieve the cook time and temp as an array so it can be transferred as one parameter then split it up  
#	 print('Cook Time:', all_data [0])
#	 print('Cook Temp:', all_data [1])
#	 time_num = int(all_data [0])
#	 #instructions = listen(instructions)
#	 temp_num = int(all_data [1])
#   except socket.error:
#	 print("An error has occured...")
def listen(instructions):
	'''this thread listens for messages from the app'''
	try:
		#Recieve the cook time and temp as an array so it can be transferred as one parameter then split it up  
		print('Cook Time:', int(all_data[0]))
		print('Cook Temp:', int(all_data[1]))
		
		#time_num = int(all_data [0])
		#instructions = listen(instructions)
		#temp_num = int(all_data [1])
	except socket.error:
		print("An error has occured...")
#   while True:
#	 input('>')
#	 '''Upon recieving confirmation, call instructions.confirm()
#	   Upon recieving stop order, call instructions.stop()
#	 '''

def execute(controller, instructions):
	GPIO.setmode(GPIO.BOARD)


	try:
		''' Loop until shut off '''
		while True:
			instructions.confirmed.wait() # have the instructions been confirmed? wait until this is true
			controller.start()
			instructions.stopped.wait(timeout=instructions.cook_time) # wait until user signals to stop, up to the length of the timer
			controller.end()

	finally:
		GPIO.cleanup()


''' For future reference, using end='\r' allows printing over same line '''
if __name__ == '__main__':
# one instruction structure for each toaster slot
	GPIO.setmode(GPIO.BOARD)
	GPIO.getmode()
	# instructions = CookInstructions()
	# controller = ToasterController(instructions)
# this thread will listen for messages from the app (also send messages back?)
	# listener = thread.Thread(target=listen, name='listener', args=(instructions,), daemon=True)
	# listener.start()
# this thread will control the toaster hardware
	# execute = thread.Thread(target=execute, name='executor', args=(controller, instructions))
	# execute.start()
	# listener.join()
	# execute.join()

