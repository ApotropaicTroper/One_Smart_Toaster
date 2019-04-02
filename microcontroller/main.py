import socket
import threading as thread
import threading
from RPi import GPIO

from controller import ToasterController
from instruction import CookInstructions
from timer import CookTimer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
host = ''  # Get local machine name
port = 12345  # Reserve a port for your service.
temp_data = 0
time_data = 0
all_data = 0

print(host)
s.bind((host, port))  # Bind to the port

try:
    s.listen(1)  # Now wait for client connection.
except timeout:
    print("Server Timed out...closing socket")
    s.close()

try:
    c, addr = s.accept()  # Establish connection with client.
    print("Server Was Setup!")
    print('Got connection from', addr)
    output = 'Thank you for connecting'
    c.sendall(output.encode('utf-8'))
except socket.error:
    print("An error has occurred... closing connection to client")
    print("...Closing socket")
    c.close()
# finally:
# c.shutdown(socket.SHUT_RDWR)

def always_listen():
    
    while True:
        try:           
            data = c.recv(12345).decode()  # data is accepted in a byte stream
            all_data = data.split(' ', 2)  # split the data coming in into an array (0 is cook time, 1 is cook temp)
            
            if all_data[0] == 'Time':
                if CookTimer.running == True:
                    print("here")
                    controller.reset()
                    execute()
                instructions.cook_time = int(all_data[1])
                print("Time Set")
            elif all_data[0] == 'Temp':
                instructions.cook_temp = int(all_data[1])
                print("Temp Set")
            elif all_data[0] == 'Stop':
                cancel()
            elif all_data[0] == 'Confirm':
                instructions.confirm()
                print("Confirmed")
            elif all_data[0] == 'Default':
                set_default(int(all_data[1]), int(all_data[2]))
            else:
                print("Data not understood")               
            
        except timeout:
            print("Server Timed out...closing socket")
            s.close()
            
def cancel():
    send("Cooking Cancelled")
    controller.cancel = True
            
def send(data):
    c.send(data.encode('utf-8'))
    
def set_default(time, temp):
    instructions.defaults(time, temp)

def execute(controller, instructions):

    instructions.confirmed.wait()  # have the instructions been confirmed? wait until this is true
    controller.start()
    controller.wait_time(c, instructions)
    controller.end()

#''' For future reference, using end='\r' allows printing over same line '''
if __name__ == '__main__':
    # one instruction structure for each toaster slot
    GPIO.setmode(GPIO.BCM)
    GPIO.getmode()

    socketThread = threading.Thread(target = always_listen)
    socketThread.daemon = True
    socketThread.start()    
    instructions = CookInstructions()
    controller = ToasterController(instructions)

    try:
        while True:
            print("Toaster is ready!")
            execute(controller, instructions)
    finally:
        GPIO.cleanup()


# this thread will listen for messages from the app (also send messages back?)
# listener = thread.Thread(target=listen, name='listener', args=(instructions,), daemon=True)
# listener.start()
# this thread will control the toaster hardware
# execute = thread.Thread(target=execute, name='executor', args=(controller, instructions))
# execute.start()
# listener.join()
# execute.join()

