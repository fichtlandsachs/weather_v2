#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sensors.Sensor import Sensor
from sensor_gy30 import sensor_gy_30
import configuration.constants as const

class IlluminationSensor(Sensor):
    
    _sensor_resulution = ""
    
    def __init__(self, configuration):
        Sensor.__init__(self, configuration)

    def setConfiguration(self,section):
        Sensor.setConfiguration(self, section)
        self._sensor_resulution = self._config.get(section,"sensor_resulution")
    
    def getValue(self):
        sensIllum = sensor_gy_30(self._sensor_resulution)
        if self._sensor_resulution == 'CONTINUOUS_LOW_RES_MODE':
            return sensIllum.readLight(const.CONTINUOUS_LOW_RES_MODE)
        elif self._sensor_resulution == 'CONTINUOUS_HIGH_RES_MODE_1':
            return sensIllum.readLight(const.CONTINUOUS_HIGH_RES_MODE_1)
        elif self._sensor_resulution == 'CONTINUOUS_HIGH_RES_MODE_2':
            return sensIllum.readLight(const.CONTINUOUS_HIGH_RES_MODE_2)
        elif self._sensor_resulution == 'ONE_TIME_HIGH_RES_MODE_1':
            return sensIllum.readLight(const.ONE_TIME_HIGH_RES_MODE_1)
        elif self._sensor_resulution == 'ONE_TIME_HIGH_RES_MODE_2':
            return sensIllum.readLight(const.ONE_TIME_HIGH_RES_MODE_2)           
        elif self._sensor_resulution == 'ONE_TIME_LOW_RES_MODE':
            return sensIllum.readLight(const.ONE_TIME_LOW_RES_MODE)
        else:
            return None                     