#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.config



class WeatherLogger(object):
    
    global Logger 
    
    def __init__(self):
        logging.config.fileConfig('configuration/log.ini')
        self.Logger = logging.getLogger("weatherData")        
    
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
        # 'application' code
        
        #print(message)
        self.Logger.debug(message)  

    def logCriticalMessage(self, message):    
        # 'application' code
        self.Logger.critical(message)    