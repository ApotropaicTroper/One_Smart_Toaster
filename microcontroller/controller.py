import time
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
from timer import CookTimer
from RPi import GPIO
from instruction import CookInstructions
import board
import busio
import adafruit_drv2605

# total of 40 I/O pins

class ToasterController(object):

    GPIO.setmode(GPIO.BCM)
    loaded = False
    instructions = None
    timer = None
    cancel = False


    #heating_element_channel = 0
    #fan_channel = 1
    motor_channel = 3
    #platform_spin_channel = 2
    #platform_direction_channel = 3

    #GPIO.setup(heating_element_channel, GPIO.OUT)
    #GPIO.setup(fan_channel, GPIO.OUT)
    #GPIO.setup(platform_spin_channel, GPIO.OUT)
    GPIO.setup(motor_channel, GPIO.OUT)


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
    button_1_channel = 22
    button_2_channel = 27
    button_3_channel = 17


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
        
    def wait_time(self, c, instructions):
        '''Send data to app'''
        for x in range (int(self.timer.remaining_time), -1, -1)
            if self.cancel == True:
                break
            print(self.timer.remaining_time)
            time_split = str(int(self.timer.remaining_time)) + " "
            c.send(time_split.encode('utf-8'))
            instructions.stopped.wait(timeout=1)
        if self.cancel == False:
            c.send(('Done!').encode('utf-8'))

    def reset(self):
        '''reset timer mid cook'''
        self.cancel = False
        self.timer.clear()

    def end(self):
        ''' Cooking has finished '''
        self.cancel = False
        self.set_heating_element()
        self.timer.clear()
        self.instructions.clear()
        self.raise_platform()

    def lower_platform(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        drv = adafruit_drv2605.DRV2605(i2c)
        i = 119
        drv.sequence[0] = adafruit_drv2605.Effect(i)
        drv.play()
        time.sleep(0.5)
        drv.stop()



        self.loaded = True
        # GPIO.output(self.motor_channel, GPIO.HIGH)
        # time.sleep(0.5)
        # GPIO.output(self.motor_channel, GPIO.LOW)
        print("Platform is lowered")

    def raise_platform(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        drv = adafruit_drv2605.DRV2605(i2c)
        i = 119
        drv.sequence[0] = adafruit_drv2605.Effect(i)
        drv.play()
        time.sleep(0.5)
        drv.stop()



        self.loaded = False
        # GPIO.output(self.motor_channel, GPIO.HIGH)
        # time.sleep(0.5)
        # GPIO.output(self.motor_channel, GPIO.LOW)
        print("Platform is raised")

    def set_heating_element(self):
        ...
    def get_temperature(self):
        ...
        # Temperature output as 14-bit signed integer counting quarters of °C (i.e. +1 ? 0.25°C; +4 ? 1°C)
        temp = 0
        GPIO.output(self.temp_CS0_channel, GPIO.HIGH)
        for i in range(14):
            # pulse clock
            GPIO.output(self.temp_CLK_channel, GPIO.HIGH)
            GPIO.output(self.temp_CLK_channel, GPIO.LOW)
            # read data output
            temp = temp << 1
            temp += GPIO.input(self.temp_MISO_channel)
            time.sleep(0.01)
        # output is signed int
        if temp >= 0b10000000000000:
            temp -= 0b10000000000000
        # not a bit shift; truediv is float division
        temp /= 4
        GPIO.output(self.temp_CS0_channel, GPIO.LOW)
        return temp




'''
temp (°C)   bits                int
+1600.00    01 1001 0000 0000   +6400
+1000.00    00 1111 1010 0000   +4000
 +100.75    00 0001 1001 0011   + 403       
  +25.00    00 0000 0110 0100   + 100
    0.00    00 0000 0000 0000   ±   0
   -0.25    11 1111 1111 1111   -   1
   -1.00    11 1111 1111 1100   -   4       
 -250.00    11 1100 0001 1000   -1000
'''

