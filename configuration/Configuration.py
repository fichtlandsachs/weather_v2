#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, sys, math, configuration.constants as const
import RPi.GPIO as GPIO
import ConfigParser
from sensors.Sensor import Sensor
from sensors.temperature.TempSensor import TempSensor
from sensors.Sensor import AnemometerSensor
from sensors.illumination.IlluminationSensor import IlluminationSensor
from log.WeatherLogger import WeatherLogger

class Configuration():
    _wLog = ""
    _conn = ""
    _updateIntervall = 0
    _sensorList = None
    _systemConfig = None
    _serverConfig = None
    _displayConfig = None
    _textConfig = None
    _sensorConfig = None
            
    def __init__(self):
        self._wLog = WeatherLogger()
        
    def getLogger(self):
        return self._wLog
    
    def getSystemConfig(self):
        return self._systemConfig
    
    def getServerConfig(self):
        return self._serverConfig
    
    def getLocaleConfig(self):
        return self._textConfig
    
    def getDisplayConfig(self):
        return self._displayConfig
    
    def getSensorConfig(self):
        return self._sensorConfig
                
    def getConfigurationFiles(self):
        self._systemConfig = ConfigParser.RawConfigParser()
        self._systemConfig.read(const._cfg_system)                   
        self._wLog.logDebugMessage("read " + const._cfg_system)
        
        self._serverConfig = ConfigParser.RawConfigParser()
        self._serverConfig.read(const._cfg_server)                   
        self._wLog.logDebugMessage("read " + const._cfg_server) 
               
        self._textConfig = ConfigParser.RawConfigParser()
        self._textConfig.read(const._cfg_locales_de)
        self._wLog.logDebugMessage("read "+const._cfg_locales_de)
        
        self._displayConfig = ConfigParser.RawConfigParser()
        self._displayConfig.read(const._cfg_display)
        self._wLog.logDebugMessage("read "+const._cfg_display)   
             
        self._sensorConfig = ConfigParser.RawConfigParser()
        self._sensorConfig.read(const._cfg_sensor)
        self._wLog.logDebugMessage("read " + const._cfg_sensor) 
        
        self._updateIntervall = int(self._serverConfig.get(const._cfg_section_database,const._cfg_entry_databaseupdIntervall))
        
    def setSensorConfiguratuion(self):
        self._sensorList = []
        _sensor = None
        
        for section in self._sensorConfig.sections():
            _sensor = Sensor(self._sensorConfig)
            _sensor.setConfiguration(section)
            
            if _sensor._sensorCategory == const._temperature:
                tempSens = TempSensor(self._sensorConfig)
                tempSens.setConfiguration(section)
                self._sensorList.append(tempSens)
            elif _sensor._sensorCategory == const._anemometer:
                anemoSens = AnemometerSensor(self._sensorConfig)
                anemoSens.setConfiguration(section)
                self._sensorList.append(anemoSens)
            elif _sensor._sensorCategory == const._illum:
                illumSens = IlluminationSensor(self._sensorConfig)
                illumSens.setConfiguration(section)
                self._sensorList.append(illumSens) 
        return self._sensorList