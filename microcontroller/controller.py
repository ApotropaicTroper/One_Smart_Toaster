import time
from time import sleep
import socket
import board
import busio
import digitalio
import adafruit_max31855
import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855
from gpiozero import Motor, Button

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
from timer import CookTimer
from instruction import CookInstructions

class ToasterController(object):

    loaded = False
    instructions = None
    timer = None
    cancel = False
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = digitalio.DigitalInOut(board.D5) 
    max31855 = adafruit_max31855.MAX31855(spi, cs)
    main_time = 12
    cancel_time = 1
    #motor1 = Motor(forward = 2, backward = 4)
    
    CLK = 11
    CS  = 8
    DO  = 9
    sensor = MAX31855.MAX31855(CLK, CS, DO)
    
    btn = Button(27)
    button_1_channel = 22
    button_2_channel = 27
    button_3_channel = 17

    def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0
    
    def __init__(self, instructions):
        self.instructions = instructions
        self.timer = CookTimer()

    def start(self, c, motor1):
        ''' Begin cooking '''       
        self.timer.set(self.instructions.cook_time)
        self.lower_platform(c, motor1)
        
    def lower_platform(self, c, motor1):
        try:
            self.loaded = True                
            for x in range (0, self.main_time, 1):
                motor1.backward()
                if self.cancel == True:
                    break
                note = 'Lowering food...'
                c.send(note.encode('utf-8'))            
                print('Main: ', self.main_time)
                print('Cancel: ',self.cancel_time)
                self.cancel_time = self.cancel_time + 1
                time.sleep(1)
            if self.cancel == False:
                note = 'Food Lowered' + ' '
                c.sendall(note.encode('utf-8'))
                print("Platform is lowered")
                motor1.stop()
                self.timer.start()
                self.wait_time(c, self.instructions)
        except OSError:
            print("Error...")
            motor1.stop()
            
    def lower_platform_offline(self, motor1):
        try:
            self.loaded = True                
            for x in range (0, self.main_time, 1):
                motor1.backward()
                if self.cancel == True:
                    break       
                print('Main: ', self.main_time)
                print('Cancel: ',self.cancel_time)
                self.cancel_time = self.cancel_time + 1
                time.sleep(1)
            if self.cancel == False:
                print("Platform is lowered")
                motor1.stop()
                self.timer.start()
                self.wait_time_offline(self.instructions)
        except OSError:
            print("Error...")
            motor1.stop()
        
    def wait_time(self, c, instructions):
        '''Send data to app'''
        if int(self.timer.remaining_time)  <= 0:
            self.timer.cook_time = instructions.cook_time
        try:
            for x in range (int(self.timer.remaining_time), -1, -1):
                if self.cancel == True:
                    break
                print(self.timer.remaining_time)
                time_split = str(round(self.timer.remaining_time))
                tempC = self.sensor.readTempC()
                tempF = str(tempC * 9 / 5 + 32)
                print('Temperature: {} C {} F '.format(tempC, tempF))
                total_data = time_split + ' ' + tempF + ' ' + 'Code'
                c.send(total_data.encode('utf-8'))
                instructions.stopped.wait(timeout=1)
        except OSError:
            print("Error...")
        
    def wait_time_offline(self, instructions):
        '''Send data to app'''
        if int(self.timer.remaining_time)  <= 0:
            self.timer.cook_time = instructions.cook_time
        try:
            for x in range (int(self.timer.remaining_time), -1, -1):
                if self.cancel == True:
                    break
                print(self.timer.remaining_time)
                instructions.stopped.wait(timeout=1)
        except OSError:
            print("Error...")
            motor1.stop()

    def raise_platform(self, c, motor1):
        try:
            self.loaded = False
            raise_time = -1
            self.cancel_time = self.cancel_time - 1
            print('Main: ', self.main_time)
            print('Cancel: ',self.cancel_time)
            if self.main_time != self.cancel_time:
                raise_time = raise_time + self.cancel_time + 1
            else:
                raise_time = self.main_time
            for x in range (0, raise_time, 1):
                motor1.forward()
                note = 'Raising food...'
                c.send(note.encode('utf-8'))
                time.sleep(1)
            note = 'Raised'
            c.send(note.encode('utf-8'))
            print("Platform is raised")
            motor1.stop()
        except OSError:
            print("Error...")
            motor1.stop()

    def raise_platform_offline(self, motor1):
        try:
            self.loaded = False
            raise_time = -1
            print('Main: ', self.main_time)
            
            if self.main_time != self.cancel_time:
                raise_time = raise_time + self.cancel_time
            else:
                raise_time = self.main_time
            print('Raise: ',raise_time)
            for x in range (0, raise_time, 1):
                motor1.forward()
                time.sleep(1)
            print("Platform is raised")
            motor1.stop()
        except OSError:
            print("Error...")
            motor1.stop()

    def reset(self):
        '''reset timer mid cook'''
        self.cancel = False
        self.timer.clear()

    def end(self, c, motor1):
        ''' Cooking has finished '''
        self.cancel = False        
        self.timer.clear()
        self.instructions.clear()
        self.raise_platform(c, motor1)
        self.cancel_time = 0
        
    def end_offline(self, motor1):
        ''' Cooking has finished '''
        self.cancel = False        
        self.timer.clear()
        self.instructions.clear()
        self.raise_platform_offline(motor1)
        self.cancel_time = 0  
