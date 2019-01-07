#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, sys, math, configuration.constants as const
import RPi.GPIO as GPIO
import ConfigParser, warnings
from time import sleep
from sensors.Sensor import Sensor
from sensors.temperature.TempSensor import TempSensor
from sensors.Sensor import AnemometerSensor
from sensors.wind.Anemometer import windSensor
from sensors.illumination.IlluminationSensor import IlluminationSensor
from log.WeatherLogger import WeatherLogger
from handler.SystemState import SystemState
from handler.DatabaseHandler import DatabaseHandler

class CurrentWeatherCond():

    _wetterDataVals = []
    _temp_DHT22 = 0
    _temp_BMP085 = 0
    _humi_DHT22 = 0
    _humi_BMP085 = 0
    _altitude = 0
    _pressure = 0
    _illum =0
    _pulse = 0
    _windSpeed = 0
    _maxPressure = 0.0
    _minPressure = 0.0
    _avgPressure = 0.0
    _avgPressureCount = 0
    _maxhumi = 0.0
    _minhumi = 0.0
    _avghumi = 0.0
    _avghumiCount =0
    _maxtemp = 0.0
    _mintemp = 0.0
    _avgtemp = 0.0
    _avgtempCount =0
    _maxwindSpeed = 0.0
    _minwindSpeed = 0.0
    _avgwindSpeed = 0.0
    _avgwindSpeedCount = 0
    _maxpulse = 0.0
    _minpulse = 0.0
    _avgpulse = 0.0
    _avgpulseCount = 0
    _maxillum = 0.0
    _minillum = 0.0
    _avgillum = 0.0
    _avgillumCount = 0
    _wetterDataVals = []
    _currWetterDataVals= []
    
    def __init__(self, SystemState):
        self._wLog = WeatherLogger()
        self._systemState = SystemState
        self._wetterDataVals = []
        self._wetterDataVals.append({'maxPressure' : 0.0, 'minPressure' : 0.0, 'avgPressure' : 0.0, 'avgPressureCount':0,b'maxhumi' : 0.0,b'minhumi': 0.0, 'avghumi' : 0.0, 'avghumiCount':0,b'maxtemp' : 0.0, 'mintemp' : 0.0, 'avgtemp' : 0.0, 'avgtempCount' : 0,'maxwindSpeed' :0.0, 'minwindSpeed' : 0.0,'avgwindSpeed' :0.0,'avgwindSpeedCount':0, 'maxpulse' :0.0, 'minpulse' :0.0, 'avgpulse' : 0.0, 'avgpulseCount':0 ,'maxillum' : 0.0, 'minillum' : 0.0, 'avgillum' : 0.0, 'avgillumCount':0})
        
    def getCurrentVals(self, configuration):
        
        for sensor in configuration._sensorList:
            if sensor._sensorCategory == const._temperature:
                if sensor._sensorType == const._sens_dht22:
                    self._temp_DHT22, self._humi_DHT22, self._pressure, self._altitude = sensor.getValue()
                elif sensor._sensorType ==const._sens_bmp085:
                    self._temp_BMP085, self._humi_BMP085, self._pressure, self._altitude = sensor.getValue()
            elif sensor._sensorCategory == const._illum:
                self._illum = sensor.getValue()
            elif sensor._sensorCategory == const._anemometer:
                self._windSpeed, self._pulse = windSensor(sensor).determineWindSpeed()
                
        self._currWetterDataVals= []
        self._currWetterDataVals.append({const._pressure: self._pressure, const._humidity: self._humi_DHT22,const._temperature: self._temp_BMP085, const._illum: self._illum, const._windspeed: self._windSpeed, const._pulse: self._pulse, const._altitude : self._altitude})
        self.setMinMaxVals()
        
    def setMinMaxVals(self):
        size = len(self._wetterDataVals)
        if self._maxPressure < self._pressure or self._maxPressure == 0:
            self._maxPressure = self._pressure
        if self._minPressure > self._pressure or self._minPressure == 0:
            self._minPressure = self._pressure
        #if (self._maxPressure > self._pressure and self._minPressure < self._pressure) or self._avgPressure == 0:
        self._avgPressure = self._avgPressure + self._pressure
        self._avgPressureCount = self._avgPressureCount+ 1
        
        if self._maxhumi < self._humi_DHT22 or self._maxhumi == 0:
            self._maxhumi = self._humi_DHT22
        if self._minhumi > self._humi_DHT22 or self._minhumi == 0:
            self._minhumi = self._humi_DHT22
        #if (self._maxhumi > self._humi_DHT22 and self._minhumi < self._humi_DHT22) or self._avghumi == 0:
        self._avghumi = self._avghumi + self._humi_DHT22
        self._avghumiCount = self._avghumiCount+ 1
            
        if self._maxtemp < self._temp_BMP085 or self._maxtemp == 0:
            self._maxtemp = self._temp_BMP085
        if self._mintemp > self._temp_BMP085 or self._mintemp == 0:
            self._mintemp = self._temp_BMP085
        #if (self._maxtemp > self._temp_BMP085 and self._mintemp < self._temp_BMP085) or self._avgtemp == 0:
        self._avgtemp = self._avgtemp + self._temp_BMP085
        self._avgtempCount = self._avgtempCount+ 1  
                  
        if self._maxillum < self._illum or self._maxillum == 0:
            self._maxillum = self._illum
        if self._minillum > self._illum or self._minillum == 0:
            self._minillum = self._illum
        #if (self._maxillum > self._illum and self._minillum < self._illum) or self._avgillum == 0:
        self._avgillum = self._avgillum + self._illum
        self._avgillumCount = self._avgillumCount+ 1
            
        if self._maxwindSpeed < self._windSpeed or self._maxwindSpeed == 0:
            self._maxwindSpeed = self._windSpeed
        if self._minwindSpeed > self._windSpeed or self._minwindSpeed == 0:
            self._minwindSpeed = self._windSpeed
        #if (self._maxwindSpeed > self._windSpeed and self._minwindSpeed < self._windSpeed) or self._avgwindSpeed == 0:
        self._avgwindSpeed = self._avgwindSpeed + self._windSpeed
        self._avgwindSpeedCount = self._avgwindSpeedCount+ 1

        if self._maxpulse < self._pulse or self._maxpulse == 0:
            self._maxpulse = self._pulse
        if self._minpulse > self._pulse or self._minpulse == 0:
            self._minpulse = self._pulse
        #if (self._maxpulse > self._pulse and self._minpulse < self._pulse) or self._avgpulse == 0:
        self._avgpulse = self._avgpulse + self._pulse
        self._avgpulseCount = self._avgpulseCount+ 1
        if size > 0:
            size = size -1
            self._wetterDataVals[size] = ({'maxPressure' : self._maxPressure, 'minPressure' : self._minPressure, 'avgPressure' : self._avgPressure, 'avgPressureCount':self._avgPressureCount,'maxhumi' : self._maxhumi, 'minhumi': self._minhumi, 'avghumi' : self._avghumi, 'avghumiCount':self._avghumiCount,'maxtemp' : self._maxtemp, 'mintemp' : self._mintemp, 'avgtemp' : self._avgtemp, 'avgtempCount' : self._avgtempCount,'maxwindSpeed' :self._maxwindSpeed, 'minwindSpeed' : self._minwindSpeed,'avgwindSpeed' :self._avgwindSpeed,'avgwindSpeedCount':self._avgwindSpeedCount, 'maxPulse' :self._maxpulse, 'minPulse' :self._minpulse, 'avgPulse' : self._avgpulse, 'avgPulseCount':self._avgpulseCount ,'maxillum' : self._maxillum, 'minillum' : self._minillum, 'avgillum' : self._avgillum, 'avgillumCount':self._avgillumCount})
        else:
            self._wetterDataVals.append({'maxPressure' : self._maxPressure, 'minPressure' : self._minPressure, 'avgPressure' : self._avgPressure, 'avgPressureCount':self._avgPressureCount,'maxhumi' : self._maxhumi,'minhumi': self._minhumi, 'avghumi' : self._avghumi, 'avghumiCount':self._avghumiCount, 'maxtemp' : self._maxtemp, 'mintemp' : self._mintemp, 'avgtemp' : self._avgtemp, 'avgtempCount' : self._avgtempCount,'maxwindSpeed' :self._maxwindSpeed, 'minwindSpeed' : self._minwindSpeed,'avgwindSpeed' :self._avgwindSpeed,'avgwindSpeedCount':self._avgwindSpeedCount, 'maxPulse' :self._maxpulse, 'minPulse' :self._minpulse, 'avgPulse' : self._avgpulse,  'avgPulseCount':self._avgpulseCount ,'maxillum' : self._maxillum, 'minillum' : self._minillum, 'avgillum' : self._avgillum, 'avgillumCount':self._avgillumCount})
            
    def clearLastVals(self):
        self._maxPressure = 0.0
        self._minPressure = 0.0
        self._avgPressure = 0.0
        self._avgPressureCount = 0
        self._maxhumi = 0.0
        self._minhumi = 0.0
        self._avghumi = 0.0
        self._avghumiCount =0
        self._maxtemp = 0.0
        self._mintemp = 0.0
        self._avgtemp = 0.0
        self._avgtempCount =0
        self._maxwindSpeed = 0.0
        self._minwindSpeed = 0.0
        self._avgwindSpeed = 0.0
        self._avgwindSpeedCount = 0
        self._maxpulse = 0.0
        self._minpulse = 0.0
        self._avgpulse = 0.0
        self._avgpulseCount = 0
        self._maxillum = 0.0
        self._minillum = 0.0
        self._avgillum = 0.0
        self._avgillumCount = 0
        self._humi_DHT22 = 0
        self._humi_BMP085 = 0
        self._temp_BMP085 = 0
        self._temp_DHT22 = 0
        self._pressure = 0
        self._altitude = 0
        self._illum = 0
        self._windSpeed = 0
        self._currWetterDataVals = []
        self._wetterDataVals = []

if __name__ == '__main__':

    if not sys.warnoptions:
        warnings.simplefilter("ignore")    
    i = 0
       
    systemState = SystemState()
    systemState.setConfiguration()
    
    configuration = systemState.getConfiguration()
    
    if configuration._systemConfig.get(const._cfg_section_system, const._cfg_entry_debug)=='True':
        _remote_IP = configuration._systemConfig.get(const._cfg_section_system, const._cfg_entry_debug_IP)
        import pydevd
        pydevd.settrace(_remote_IP, stdoutToServer=True, stderrToServer=True)
        configuration._updateIntervall = 30

    database = DatabaseHandler(systemState)
    print("System initialized")
    
    currWeather = CurrentWeatherCond(systemState)
    
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=5)
    while 1!=0:
        
        try:
            i = 0
            if endTime < datetime.datetime.now():
                database.getDatabaseConnection()
                currTime = datetime.datetime.now().isoformat()
                database.setValuesToDB(currWeather._wetterDataVals, currTime)
                database.uploadLocalData()
                database.setCurrValsToDB(currWeather._currWetterDataVals, currTime)
                endTime = datetime.datetime.now() + datetime.timedelta(seconds=configuration._updateIntervall)
                database.closeConnection()
                currWeather.clearLastVals()
                systemState.refreshSystemConfig()
                currWeather.getCurrentVals(configuration)                
            else:
                currWeather.getCurrentVals(configuration)
                              
            systemState._disp.setCurrentData(currWeather._currWetterDataVals)
            while i < 2:
                systemState._disp.displayData()
                sleep(5)
                i = i +1  
        except KeyboardInterrupt:
            print("program closed after keyboard interrupt")
            exit()