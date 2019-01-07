#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, configuration.constants as const
import logging.config
import ConfigParser


class WeatherLogger(object):
    
    global Logger 
    
    def __init__(self):
        logging.config.fileConfig('configuration/log.ini')
        self.Logger = logging.getLogger("weatherData")
        self.systemConfig = ConfigParser.RawConfigParser()
        self.systemConfig.read(const._cfg_system)    
         
        if self.systemConfig.get(const._cfg_section_system, const._cfg_entry_loglevel) == 'INFO':
            self.Logger.setLogLevel(logging.INFO)
        elif self.systemConfig.get(const._cfg_section_system, const._cfg_entry_loglevel) == 'DEBUG':
            self.Logger.setLogLevel(logging.DEBUG)
        elif self.systemConfig.get(const._cfg_section_system, const._cfg_entry_loglevel) == 'ERROR':
            self.Logger.setLogLevel(logging.ERROR)

    
    def logErrorMessage(self, message):    
        # 'application' code
        self.Logger.error(message)

    def logWarningMessage(self, message):    
        # 'application' code
        self.Logger.warn(message)
        
    def logInfoMessage(self, message):    
        # 'application' code
        self.Logger.info(message)
        
    def logDebugMessage(self, message):    
        self.Logger.debug(message)  

    def logCriticalMessage(self, message):    
        # 'application' code
        self.Logger.critical(message)
        
    def setLogLevel(self, level):
        self.Logger.setLevel(level)   