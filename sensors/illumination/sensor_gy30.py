#!/usr/bin/python
import smbus
import datetime, time, os, math
import RPi.GPIO as GPIO
import configuration.constants as const

# Define some constants from the datasheet
 
DEVICE     = 0x23 # Default device I2C address
 
POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value
 

 
#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

class sensor_gy_30():
	
	_resolution_mode = ""
	
	def __init__(self, resol):
		data = ""
		_resolution_mode = resol
			
	def convertToNumber(self, data):
	  # Simple function to convert 2 bytes of data
	  # into a decimal number
	  return ((data[1] + (256 * data[0])) / 1.2)
	 
	def readLight(self, addr=DEVICE):
	  data = bus.read_i2c_block_data(DEVICE,const.ONE_TIME_HIGH_RES_MODE_2)
	  return self.convertToNumber(data)