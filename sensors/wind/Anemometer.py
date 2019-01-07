#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, sys, math, configuration.constants as const
import RPi.GPIO as GPIO
import ConfigParser
from sensors.Sensor import Sensor
from sensors.temperature.TempSensor import TempSensor
from sensors.Sensor import AnemometerSensor
from sensors.illumination.IlluminationSensor import IlluminationSensor
from handler.DisplayAdapter import DisplayHandler
from log.WeatherLogger import WeatherLogger
from handler.DatabaseHandler import DatabaseHandler
from handler.SystemState import SystemState

from time import sleep
import warnings

_windSensor = None
_anemoSens = None
_lastTime = 0

class windSensor():
    global number
    _wlog           = None
    _endTime        = None
    _recordTime     = None
    _opensens       = None
    _closedsens     = None
    _lastSens       = None
    _lastWind       = None
    _pulse          = None
    _meterspersec   = None
    _kmh            = None
    _mph            = None
    _beaufort       = None
    _windPin        = None
  
    def __init__(self, anemoSens):
        self._wLog = WeatherLogger()
        self._sensorConfig = anemoSens
        self._windPin = int(anemoSens._sensor_pin)
        self.initVars()
        
    def initVars(self):
        self._recordTime = 0
        self._closedsens = 0
        self._opensens = 1
        self._lastSens = 1
        self._lastWind = 0
        self._pulse = 0
        self._meterspersec = 0.0
        self._kmh=0.0
        self._mph=0.0
        self._beaufort=0.0
        self._stop = False
         
    def determineWindSpeed(self):
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._windPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.initVars()

        self._endTime = datetime.datetime.now() + datetime.timedelta(seconds=10)
        self._recordTime = self._endTime + datetime.timedelta(seconds=5)
        while datetime.datetime.now() <= self._endTime:
        
                while GPIO.input(self._windPin) == self._opensens and self._lastSens != self._opensens:
                    self._lastSens = GPIO.input(self._windPin)
                    self._pulse += 1
                while GPIO.input(self._windPin) == self._closedsens and self._lastSens != self._closedsens:
                    self._lastSens = GPIO.input(self._windPin)
        
        self._meterspersec=2*math.pi*0.065*self._pulse
        self._lastWind = self._meterspersec
        return round(self._meterspersec,3),  self._pulse
