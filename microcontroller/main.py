import time
import socket
import threading as thread
import threading
import os
import requests
import board
import busio
import digitalio
import adafruit_max31855

import RPi.GPIO as GPIO
from gpiozero import Motor, Button

from time import sleep

from socket import error as SocketError
from controller import ToasterController
from instruction import CookInstructions
from timer import CookTimer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
host = ''  # Get local machine name
port = 12345  # Reserve a port for your service.
loop = True
global motor1
motor1 = Motor(forward = 2, backward = 4)
button = Button(17)
button2 = Button(22)
main_exit = False
global offline_mode
offline_mode = True
global failsafe
failsafe = False

instructions = CookInstructions()
controller = ToasterController(instructions)

def cancel():
    '''
    if offline_mode == False and failsafe == True:
        data = 'Cooking Cancelled'
        send(data)
    '''
    controller.cancel = True

def cancel_button():
    
    while True:
        if main_exit == True:
            break
        button.wait_for_release()
        cancel()
        
def lower_button():
    
    while True:
        if main_exit == True:
            break
        button2.wait_for_release()
        controller.lower_platform_offline(motor1)
        controller.end_offline(motor1)

socketThread2 = threading.Thread(target = cancel_button)
socketThread2.daemon = True
socketThread2.start()
socketThread3 = threading.Thread(target = lower_button)
socketThread3.daemon = True
socketThread3.start()

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
    offline_mode = False
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
            print(all_data)
            
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
                global failsafe
                failsafe = False
            elif all_data[0] == 'Confirm':
                global failsafe
                failsafe = True
                instructions.confirm()
                print("Confirmed")
            elif all_data[0] == 'Default':
                set_default(int(all_data[1]), int(all_data[2]))
            elif all_data[0] == 'Disconnect':
                '''c.close()'''
            else:
                print("Data not understood")            
        except socket.timeout:
            print("Server Timed out...closing socket")
            c.close()
            loop == False
            main_exit = True
            global offline_mode
            offline_mode = True
            global motor1
            motor1.stop()
            break
        except ConnectionResetError as e:
            print("Error: Connection was lost to client")
            c.close()
            loop == False
            main_exit = True
            global offline_mode
            offline_mode = True
            global motor1
            motor1.stop()
            break
  
def send(data):
    if offline_mode == False:
        c.send(data.encode('utf-8'))
    
def set_default(time, temp):
    instructions.defaults(time, temp)
    text_file = open("default.txt", mode = 'w')
    text_file.write(str(time))
    text_file.write("\n")
    text_file.write(str(temp))
    text_file.close()
    

def execute(controller, instructions, motor1):

    instructions.confirmed.wait()  # have the instructions been confirmed? wait until this is true
    controller.start(c, motor1)    
    controller.end(c, motor1)

#''' For future reference, using end='\r' allows printing over same line '''
if __name__ == '__main__':
    # one instruction structure for each toaster slot
    GPIO.setmode(GPIO.BCM)
    GPIO.getmode()

    instructions = CookInstructions()
    controller = ToasterController(instructions)
    socketThread = threading.Thread(target = always_listen)
    socketThread.daemon = True
    socketThread.start()   

    try:
        while loop:
            print("Time: ", instructions.cook_time)
            if main_exit == True:
                break
            print("Toaster is ready!")
            execute(controller, instructions, motor1)
    finally:        
        print("ending program")
        GPIO.cleanup()
        motor1.stop()

