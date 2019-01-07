#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime, time, os, math,fcntl,struct, configuration.constants as const, handler.Error as Error
from log.WeatherLogger import WeatherLogger
import netifaces, socket, ConfigParser
from configuration.Configuration import Configuration
from handler.DisplayAdapter import DisplayHandler

class SystemState():
    
    _fallbackConn = None
    _currConnection = None
    _defaultAdapter = None
    _adapter = None
    _systemConfig = ConfigParser.RawConfigParser()
    _serverConfig = ConfigParser.RawConfigParser()
    _sensorList = []
    _disp = None
    
    def __init__(self):
        self._wLog = WeatherLogger()
        self._wLog.logDebugMessage("initialize class system state")
        self._configuration = Configuration()
        self._configuration.getConfigurationFiles()
        self._systemConfig = self._configuration.getSystemConfig()
        self._serverConfig = self._configuration.getServerConfig()
        self.initHandler()
        
    def getNetworkState(self):
        return self.get_ip_address()
    
    def initHandler(self):            
        self._disp = DisplayHandler(self._configuration)
        self._disp.setSystemState(self.check_network_connection())
        
    def refreshSystemConfig(self):    
        self.getNetworkAdapter()
        self.setSensorConfiguratuion()        
        self.setDatabaseUpdateIntervall()
        self.initHandler()
        self._adapter = self._systemConfig.get(const._cfg_section_Network,const._cfg_entry_Adapter )
        self._defaultAdapter = self._systemConfig.get(const._cfg_section_Network,self._adapter)        
    
    def getConfiguration(self):
        return self._configuration
        
    def setConfiguration(self):
        self._configuration.getConfigurationFiles()
        self._sensorList = self._configuration.setSensorConfiguratuion()
        self._systemConfig = self._configuration.getSystemConfig()
        self._serverConfig = self._configuration.getServerConfig()
        self.setNetworkConfiguration()
        
    def getNetworkAdapter(self):
        self._adapter = self._systemConfig.get(const._cfg_section_Network,const._cfg_entry_Adapter )
        self._defaultAdapter = self._systemConfig.get(const._cfg_section_Network,self._adapter)    
        
    def setDatabaseUpdateIntervall(self):
        self._updateIntervall = int(self._serverConfig.get(const._cfg_section_database, const._cfg_entry_databaseupdIntervall))        
        
    def setNetworkConfiguration(self):
        self.getNetworkAdapter()
        self._networkConnectionExists = self.check_network_connection()
        if self._networkConnectionExists != True:
           self._wLog.logErrorMessage(const._err_no_connection)
           
    def check_network_connection(self):
        _avl_interfaces = netifaces.interfaces()
        
        for _avlIntf in _avl_interfaces:
            if self._defaultAdapter == _avlIntf:
                self._currConnection = _avlIntf
                addr = netifaces.ifaddresses(self._defaultAdapter)
                return netifaces.AF_INET in addr  
        return False
    
    def get_ip_address(self):
        if self.check_network_connection():
            if self._defaultAdapter !=None:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                return socket.inet_ntoa(fcntl.ioctl(
                    s.fileno(),
                    0x8915,  # SIOCGIFADDR
                    struct.pack('256s', self._defaultAdapter[:15])
                )[20:24])
        else:
            return '0.0.0.0'