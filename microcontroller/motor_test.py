
'''
	Motor on:
	02	SDA
	03	SCL
	04	IN/TRIG

MODE register (0x01):
	STANDBY: 		0x01[6]
		0: ready
		1: standby
	PWM:			0x01[2:0]
		3: PWM/Analog input
	N_PWM_ANALOG	0x1D[1]:
		0: PWM
		1: Analog

initialize by setting PWM mode
set standby
send PWM info
clr standby
	platform lifts
set standby
	platform stops


SPI with spidev
I²C with smbus


'''
import time

from RPi import GPIO





def adafruit():
	import board
	import busio
	import adafruit_drv2605

	i2c = busio.I2C(board.SCL, board.SDA)
	drv = adafruit_drv2605.DRV2605(i2c)
	for i in range(123):
		drv.sequence[i] = adafruit_drv2605.Effect(i)
		drv.play()
		time.sleep(0.5)
		drv.stop()






if __name__ == '__main__':

	adafruit()




	# SDA = 2
	# SCL = 3
	# IN_TRIG = 4





	# GPIO.setup(SDA, GPIO.OUT)
	# GPIO.setup(SCL, GPIO.OUT)

	# GPIO.setup(IN_TRIG, GPIO.OUT)
	# for i in range(4):
	# 	GPIO.output(SDA, GPIO.HIGH)
	# 	time.sleep(1)
	# 	GPIO.output(2, GPIO.LOW)

	# 	GPIO.output(3, GPIO.HIGH)
	# 	time.sleep(1)
	# 	GPIO.output(3, GPIO.LOW)

	# 	GPIO.output(4, GPIO.HIGH)
	# 	time.sleep(1)
	# 	GPIO.output(4, GPIO.LOW)



