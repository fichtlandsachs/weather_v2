#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sensors.Sensor import Sensor
import Adafruit_DHT
import lib.Adafruit_BMP.BMP085 as BMP085


class TempSensor(Sensor):
    _sensor_function_temp = 0
    _sensor_function_humidity = 0
    _sensor_function_pressure = 0
    _sensor_function_altitude = 0
        
    def __init__(self, configuration):
        Sensor.__init__(self, configuration)

    def setConfiguration(self, section):
        Sensor.setConfiguration(self, section)
        
        self._sensor_function_temp = self._config.get(section,"sensor_function_temp")
        self._sensor_function_humidity = self._config.get(section,"sensor_function_humidity")
        self._sensor_function_pressure = self._config.get(section,"sensor_function_pressure")
        self._sensor_function_altitude = self._config.get(section,"sensor_function_altitude")
    
    def getValue(self):
        return self.getTemperature(), self.getHumidity(), self.getPressure(), self.getAltitude()
    
    def getTemperature(self):
        if self._sensorType == "DHT22" and self._sensor_function_temp == "1":
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, self._sensor_pin)
            #print humidity
            return temperature
        elif self._sensorType == "BMP085" and self._sensor_function_temp == "1":
            self.bmp = BMP085.BMP085()
            return self.bmp.read_temperature()
    
    def getHumidity(self):
        if self._sensorType == "DHT22" and self._sensor_function_humidity == "1":
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, self._sensor_pin)
            return humidity
        else:
            return 0
    
    def getPressure(self):
        if self._sensorType == "BMP085" and self._sensor_function_pressure == "1":
            seaLevelPressure = 1013.25
            self.bmp = BMP085.BMP085()
            return self.bmp.read_sealevel_pressure(300.8) / 100
        else:
            return 0
    
    def getAltitude(self):        
        if self._sensorType == "BMP085" and self._sensor_function_altitude == "1":
            self.bmp = BMP085.BMP085()
            return self.bmp.read_altitude()
        else:
            return 0
            
        