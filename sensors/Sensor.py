#!/usr/bin/env python
# -*- coding: utf-8 -*-
from log.WeatherLogger import WeatherLogger
import ConfigParser
from handler.Error import Error

class Sensor():
    _sensorType = ""
    _config = ConfigParser.RawConfigParser()
    _sections= []
    _sensorCategory = ""  
    _sensor_pin = 0
    _sensor_Address = "" 
    _disp = ""
    
    def __init__(self, configuration):
        self.wLog = WeatherLogger()
        self._config = configuration
        
    def setConfiguration(self, section):
        
        config_len = len(self._config.items(section))
        
        if config_len > 0:
            self._sensorCategory = self._config.get(section,"sensor_category")
            self._sensorType = self._config.get(section,"sensor_type")
            self._sensor_pin = self._config.get(section,"sensor_pin")
            self._sensor_Address = self._config.get(section, "sensor_address")
            
    def getValue(self):
         return None  

        
class AnemometerSensor(Sensor):
    
    _rotator_radius = 0
    
    def __init__(self, configuration):
        Sensor.__init__(self, configuration)

    def setConfiguration(self, section):
        Sensor.setConfiguration(self, section)
        self._rotator_radius = self._config.get(section,"rotator_radius")
        
       

       