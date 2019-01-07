import configuration.constants as const, MySQLdb,datetime
import ConfigParser
from log.WeatherLogger import WeatherLogger

import sqlite3 as lite
from types import NoneType
from handler.SystemState import SystemState

class DatabaseHandler():
    
    _Logger = None
    _conn = None
    _vals = []
    _ip = None
    _databaseHost = '127.0.0.1'
    _sysState = None
    _connection = None
    _configuration = None
    _connectionEstablished = False
    _useLoclDatabase = True
    lclConn = None
    
    def __init__(self, systState):
        self._sysState = systState
        self._configuration = systState.getConfiguration()
        self._Logger = self._configuration.getLogger()
        self.lclConn=lite.connect(self._configuration.getServerConfig().get(const._cfg_section_lcldatabase, const._cfg_entry_database_schema))
        
    def setValuesToDB(self, vals, currTime):
        if self._useLoclDatabase == True:
            self.setValuesToLocalDB(vals, currTime)
        else:
            self.setValuesToRemoteDB(vals, currTime)

    def setCurrValsToDB(self, vals, currTime):
        if self._useLoclDatabase == True:
            self.setCurrValuesToLocalDB(vals, currTime)
        else:
            self.setCurrValuesToRemoteDB(vals, currTime)
            
    def getDatabaseConnection(self):
        
        self._ip_defaultAdapter = self._sysState.get_ip_address()
        
        if self._ip_defaultAdapter <> '0.0.0.0':
            self._databaseHost = self._configuration.getServerConfig().get(const._cfg_section_database, const._cfg_entry_database_host)
        else:
            self._databaseHost = '127.0.0.1'

        try:
            if self._ip_defaultAdapter <> '0.0.0.0':
                self._conn=MySQLdb.connect(host=self._databaseHost,user=self._configuration.getServerConfig().get(const._cfg_section_database, const._cfg_entry_database_user),passwd=self._configuration.getServerConfig().get(const._cfg_section_database, const._cfg_entry_database_pwd))  
                self._useLoclDatabase = False
                self.checkTableExists()
            else:
                self._conn=lite.connect(self._configuration.getServerConfig().get(const._cfg_section_lcldatabase, const._cfg_entry_database_schema))
                self._useLoclDatabase = True
                self.checkTableExists()
            return self._conn
        except Exception:
            self._Logger.logErrorMessage('failed to connect to configured database ')
            self._conn=lite.connect(self._configuration.getServerConfig().get(const._cfg_section_lcldatabase, const._cfg_entry_database_schema))
            self._Logger.logErrorMessage('connect to local database ')
            self._databaseHost = '127.0.0.1'
            self._useLoclDatabase = True
            self.checkTableExists()
            return self._conn

    def checkTableExists(self):
        if self._useLoclDatabase != True:
            self.check_remote_tables_exists()
        else:
            self.check_locl_tables_exists()
                        
    def writeValuesToDB(self, sqlStatement, values):    
        if self._conn <> None:
            cursor = self._conn.cursor()
            cursor.execute(sqlStatement, values)
            self._conn.commit() 
                 
    def closeConnection(self):
            self._conn.close()
            
    def existsValsInLocalDB(self):
        if self._useLoclDatabase != True:
            vals = []
            sql_command = 'select * from  v_WeatherData;'
            lclCursor = self.lclConn.cursor()
            lclCursor.execute(sql_command, vals)
            rows = lclCursor.fetchall()
            
            rowsInLclDB = len(rows)
            if rowsInLclDB > 0:
                return True
            else:
                return False
        else:
            return False
        
    def existsValsWeatherCurrInLocalDB(self):
        if self._useLoclDatabase != True:
            vals = []
            sql_command = 'select * from  weatherCond;'
            lclCursor = self.lclConn.cursor()
            lclCursor.execute(sql_command, vals)
            rows = lclCursor.fetchall()
            
            rowsInLclDB = len(rows)
            if rowsInLclDB > 0:
                return True
            else:
                return False
        else:
            return False
                
    def uploadLocalData(self):
        self.uploadAvgWeatherValls()
        self.uploadLocalCurrData()
        
    def uploadAvgWeatherValls(self):
        vals = []
        _wetterDataVals=[]
        if self._useLoclDatabase != True:
            if self.existsValsInLocalDB():
                #lclConn=lite.connect(self._configuration.getServerConfig().get(const._cfg_section_lcldatabase, const._cfg_entry_database_schema))
                sql_command = 'select * from  v_WeatherData;'
                lclCursor = self.lclConn.cursor()
                lclCursor.execute(sql_command, vals)
                weatherRows = lclCursor.fetchall()
                
                for weatherRow in weatherRows:
                    #print weatherRow
                    _wetterDataVals.append({'maxPressure' : weatherRow[14], 'minPressure' : weatherRow[16], 'avgPressure' : weatherRow[15], 'avgPressureCount':weatherRow[17],\
                                            'maxhumi' : weatherRow[2],'minhumi': weatherRow[4], 'avghumi' : weatherRow[3], 'avghumiCount':weatherRow[5], \
                                            'maxtemp' : weatherRow[10], 'mintemp' : weatherRow[12], 'avgtemp' : weatherRow[11], 'avgtempCount' : weatherRow[13],\
                                            'maxwindSpeed' :weatherRow[18], 'minwindSpeed' : weatherRow[20],'avgwindSpeed' :weatherRow[19],'avgwindSpeedCount':weatherRow[21], \
                                            'maxPulse' :weatherRow[22], 'minPulse' :weatherRow[24], 'avgPulse' : weatherRow[23],  'avgPulseCount':weatherRow[25],\
                                            'maxillum' : weatherRow[6], 'minillum' : weatherRow[8], 'avgillum' : weatherRow[7], 'avgillumCount':weatherRow[9]})
                    self.setValuesToDB(_wetterDataVals, weatherRow[0])
                    sql_delete_uploaded = "delete from humidity where datum = "+"'"+weatherRow[0]+"'"
                    lclCursor.execute(sql_delete_uploaded, [])
                    self.lclConn.commit()
                    sql_delete_uploaded = "delete from wind where datum = "+"'"+weatherRow[0]+"'"
                    lclCursor.execute(sql_delete_uploaded, [])
                    self.lclConn.commit()
                    sql_delete_uploaded = "delete from temperature where datum = "+"'"+weatherRow[0]+"'"
                    lclCursor.execute(sql_delete_uploaded, [])
                    self.lclConn.commit()
                    sql_delete_uploaded = "delete from pressure where datum = "+"'"+weatherRow[0]+"'"
                    lclCursor.execute(sql_delete_uploaded, [])
                    self.lclConn.commit()
                    sql_delete_uploaded = "delete from brightness where datum = "+"'"+weatherRow[0]+"'"
                    lclCursor.execute(sql_delete_uploaded, [])                                                                                                
                    _wetterDataVals = [] 
                    self.lclConn.commit()
    
    def uploadLocalCurrData(self):
        vals = []
        _wetterDataVals=[]
        if self._useLoclDatabase != True:
            if self.existsValsWeatherCurrInLocalDB():              
                sql_command = 'select * from  weatherCond;'
                lclCursor = self.lclConn.cursor()
                lclCursor.execute(sql_command, vals)
                weatherRows = lclCursor.fetchall()
                for weatherRow in weatherRows:
                    _wetterDataVals.append({const._pressure: weatherRow[5], const._humidity: weatherRow[4],const._temperature: weatherRow[2], const._illum: weatherRow[7], const._windspeed: weatherRow[6], const._pulse: weatherRow[3]})
                    self.setCurrValuesToRemoteDB(_wetterDataVals, weatherRow[0])
                    sql_delete_uploaded = "delete from weatherCond where datum = "+"'"+weatherRow[0]+"'"
                    lclCursor.execute(sql_delete_uploaded, [])
                    self.lclConn.commit()
                      
    def check_locl_tables_exists(self):
        #sql_command_schema = "create database if not exists wetterData;"
        sql_command_hum = "create table IF NOT EXISTS humidity(datum timestamp primary key, ip varchar(40), max_humidity DECIMAL(5,2), avg_humidity DECIMAL(5,2), min_humidity DECIMAL(5,2), avg_humiCount DECIMAL(4,0));"
        sql_command_illum = "create table IF NOT EXISTS brightness(datum timestamp primary key, ip varchar(40), max_brightness decimal(6,1), avg_brightness decimal(6,1), min_brightness decimal(6,1),avg_brightnessCount DECIMAL(4,0));"
        sql_command_temp = "create table IF NOT EXISTS temperature(datum timestamp primary key, ip varchar(40),max_temp decimal(5,2), avg_temp decimal(5,2), min_temp decimal(5,2), avg_tempCount DECIMALS(4,0));"
        sql_command_pressure = "create table IF NOT EXISTS pressure(datum timestamp primary key, ip varchar(40), max_pressure decimal(6,2), avg_pressure decimal(6,2), min_pressure decimal(6,2),avg_pressureCount DECIMALS(4,0));"
        sql_command_wind = "create table IF NOT EXISTS wind(datum timestamp primary key, ip varchar(40), max_windSpeed decimal(4,1), avg_windSpeed decimal(4,1), min_windSpeed decimal(4,1), max_pulse decimal(4,0), avg_pulse decimal(4,0), min_pulse decimal(4,0), avg_windSpeedCount DECIMALS(4,0), avg_pulseCount DECIMALS(4,0));"
        sql_command_currWeather = "create table IF NOT EXISTS weatherCond (datum timestamp primary key, ip varchar(40), temp decimal(5,2), pulse decimal(4,0), humidity decimal(5,2), pressure decimal(6,2), windSpeed decimal(4,1), brightness decimal(6,1));"
        sql_command_view = "create view if not exists v_WeatherData as " \
        "select humidity.datum, humidity.ip, max_humidity, avg_humidity, min_humidity, avg_humiCount,"\
        "brightness.max_brightness, brightness.avg_brightness,brightness.min_brightness, brightness.avg_brightnessCount,"\
        "temperature.max_temp, temperature.avg_temp, temperature.min_temp, temperature.avg_tempCount, " \
        "pressure.max_pressure, pressure.avg_pressure, pressure.min_pressure, pressure.avg_pressureCount, " \
        "wind.max_windSpeed, wind.avg_windSpeed, wind.min_windSpeed, wind.avg_windSpeedCount, wind.max_pulse, wind.avg_pulse, wind.min_pulse, wind.avg_pulseCount "\
        "from humidity " \
        "inner join brightness on brightness.datum = humidity.datum "\
        "inner join temperature on temperature.datum = humidity.datum "\
        "inner join pressure on pressure.datum = humidity.datum "\
        "inner join wind on wind.datum = humidity.datum;"
        values = []
        #self.writeValuesToDB(sql_command_schema, values)
        self.writeValuesToDB(sql_command_hum, values)
        self.writeValuesToDB(sql_command_illum, values)
        self.writeValuesToDB(sql_command_temp, values)
        self.writeValuesToDB(sql_command_pressure, values)                        
        self.writeValuesToDB(sql_command_wind, values)
        self.writeValuesToDB(sql_command_currWeather, values)
        self.writeValuesToDB(sql_command_view, values)
                
    def check_remote_tables_exists(self):
        sql_command_schema = "create database if not exists wetterData;"
        sql_command_hum = "create table IF NOT EXISTS wetterData.humidity(datum timestamp primary key, ip varchar(40), max_humidity DECIMAL(5,2), avg_humidity DECIMAL(8,2), min_humidity DECIMAL(5,2), avg_humiCount DECIMAL(4,0));"
        sql_command_illum = "create table IF NOT EXISTS wetterData.brightness(datum timestamp primary key, ip varchar(40), max_brightness decimal(6,1), avg_brightness decimal(8,1), min_brightness decimal(6,1),avg_brightnessCount DECIMAL(4,0));"
        sql_command_temp = "create table IF NOT EXISTS wetterData.temperature(datum timestamp primary key, ip varchar(40), max_temp decimal(5,2), avg_temp decimal(8,2), min_temp decimal(5,2), avg_tempCount DECIMAL(4,0));"
        sql_command_pressure = "create table IF NOT EXISTS wetterData.pressure(datum timestamp primary key, ip varchar(40), max_pressure decimal(6,2), avg_pressure decimal(8,2), min_pressure decimal(6,2),avg_pressureCount DECIMAL(4,0));"
        sql_command_wind = "create table IF NOT EXISTS wetterData.wind(datum timestamp primary key, ip varchar(40), max_windSpeed decimal(4,1), avg_windSpeed decimal(8,1), min_windSpeed decimal(4,1), max_pulse decimal(4,0), avg_pulse decimal(8,0), min_pulse decimal(4,0), avg_windSpeedCount DECIMAL(4,0), avg_pulseCount DECIMAL(4,0));"
        sql_command_currWeather = "create table IF NOT EXISTS wetterData.weatherCond (datum timestamp primary key, ip varchar(40), temp decimal(5,2), pulse decimal(4,0), humidity decimal(5,2), pressure decimal(6,2), windSpeed decimal(4,1), brightness decimal(6,1));"
        values = []
        self.writeValuesToDB(sql_command_schema, values)
        self.writeValuesToDB(sql_command_hum, values)
        self.writeValuesToDB(sql_command_illum, values)
        self.writeValuesToDB(sql_command_temp, values)
        self.writeValuesToDB(sql_command_pressure, values)                        
        self.writeValuesToDB(sql_command_wind, values)    
        self.writeValuesToDB(sql_command_currWeather, values)

    def setCurrValuesToRemoteDB(self, vals, currTime):
        _vals = None
        sql_command = "REPLACE into wetterData.weatherCond values(%s,%s,%s,%s,%s,%s,%s,%s);"
        _vals = (currTime, self._sysState.get_ip_address(),round(vals[0].get('Temperature'),2),round(vals[0].get('Pulse'),2),round(vals[0].get('Humidity'),2), vals[0].get('Pressure',2), round(vals[0].get('Windspeed',2)),vals[0].get('Illumination',2))
        self.writeValuesToDB(sql_command, _vals)
                                
    def setCurrValuesToLocalDB(self, vals, currTime):
        sql_command = "INSERT into weatherCond (datum, ip, temp , pulse, humidity, pressure, windSpeed, brightness ) values"
        vals = (currTime, self._sysState.get_ip_address(),round(vals[0].get('Temperature'),2),round(vals[0].get('Pulse'),2),round(vals[0].get('Humidity'),2), vals[0].get('Pressure',2), round(vals[0].get('Windspeed',2)),vals[0].get('Illumination',2))
        sql_command = sql_command + str(vals) +";"
        values=[]
        self.writeValuesToDB(sql_command, values)
        
    def setValuesToRemoteDB(self, vals, currTime):
        _vals = None        
        sql_command = "REPLACE into wetterData.humidity values(%s,%s,%s,%s,%s,%s);"        
        _vals = (currTime, self._sysState.get_ip_address(),round(vals[0].get('maxhumi'),2),round(vals[0].get('avghumi'),2),round(vals[0].get('minhumi'),2), round(vals[0].get('avghumiCount',0)))
        self.writeValuesToDB(sql_command, _vals)

        sql_command = "REPLACE into wetterData.temperature values(%s,%s,%s,%s,%s,%s);"        
        _vals = (currTime, self._sysState.get_ip_address(),round(vals[0].get('maxtemp'),2),round(vals[0].get('avgtemp'),2),round(vals[0].get('mintemp'),2), round(vals[0].get('avgtempCount',0)))
        self.writeValuesToDB(sql_command, _vals)

        sql_command = "REPLACE into wetterData.brightness values(%s,%s,%s,%s,%s,%s);"        
        _vals = (currTime, self._sysState.get_ip_address(),round(vals[0].get('maxillum'),2),round(vals[0].get('avgillum'),2),round(vals[0].get('minillum'),2), round(vals[0].get('avgillumCount',0)))
        self.writeValuesToDB(sql_command, _vals)

        sql_command = "REPLACE into wetterData.pressure values(%s,%s,%s,%s,%s,%s);"        
        _vals = (currTime, self._sysState.get_ip_address(), round(vals[0].get('maxPressure'),2),round(vals[0].get('avgPressure'),2),round(vals[0].get('minPressure'),2), round(vals[0].get('avgPressureCount',0)))
        self.writeValuesToDB(sql_command, _vals)

        sql_command = "REPLACE into wetterData.wind values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        _vals = (currTime, self._sysState.get_ip_address(),round(vals[0].get('maxwindSpeed'),2), round(vals[0].get('minwindSpeed'),2),round(vals[0].get('avgwindSpeed'),2),round(vals[0].get('avgwindSpeedCount'),0), round(vals[0].get('maxPulse'),0), round(vals[0].get('avgPulse'),0) , round(vals[0].get('minPulse'),0) , round(vals[0].get('avgPulseCount'),0))
        self.writeValuesToDB(sql_command, _vals)

                
    def setValuesToLocalDB(self, vals, currTime):
        values=[]
        
        sql_command = "INSERT into humidity ('datum', 'ip', 'max_humidity','avg_humidity','min_humidity','avg_humiCount') values"        
        _vals = (currTime, self._sysState.get_ip_address(),round(vals[0].get('maxhumi'),2),round(vals[0].get('avghumi'),2),round(vals[0].get('minhumi'),2), round(vals[0].get('avghumiCount',0)))
        sql_command = sql_command + str(_vals) +";"
        self.writeValuesToDB(sql_command, values)

        sql_command = "INSERT into temperature ('datum', 'ip', 'max_temp','avg_temp','min_temp','avg_tempCount') values"
        _vals = (currTime, self._sysState.get_ip_address(),round(vals[0].get('maxtemp'),2),round(vals[0].get('avgtemp'),2),round(vals[0].get('mintemp'),2), round(vals[0].get('avgtempCount',0)))
        sql_command = sql_command + str(_vals) +";"
        self.writeValuesToDB(sql_command, values)

        sql_command = "INSERT into brightness ('datum', 'ip', 'max_brightness','avg_brightness','min_brightness','avg_brightnessCount') values"
        _vals = (currTime, self._sysState.get_ip_address(),round(vals[0].get('maxillum'),2),round(vals[0].get('avgillum'),2),round(vals[0].get('minillum'),2), round(vals[0].get('avgillumCount',0)))
        sql_command = sql_command + str(_vals) +";"
        self.writeValuesToDB(sql_command, values)

        sql_command = "INSERT into pressure ('datum', 'ip', 'max_pressure','avg_pressure','min_pressure','avg_pressureCount') values"
        _vals = (currTime, self._sysState.get_ip_address(), round(vals[0].get('maxPressure'),2),round(vals[0].get('avgPressure'),2),round(vals[0].get('minPressure'),2), round(vals[0].get('avgPressureCount',0)))
        sql_command = sql_command + str(_vals) +";"
        self.writeValuesToDB(sql_command, values)
        
        sql_command = "INSERT into wind ('datum', 'ip', 'max_windSpeed','avg_windSpeed','min_windSpeed','avg_windSpeedCount', 'max_pulse', 'avg_pulse', 'min_pulse', 'avg_pulseCount') values"
        _vals = (currTime, self._sysState.get_ip_address(),round(vals[0].get('maxwindSpeed'),2), round(vals[0].get('minwindSpeed'),2),round(vals[0].get('avgwindSpeed'),2),round(vals[0].get('avgwindSpeedCount'),0), round(vals[0].get('maxPulse'),0), round(vals[0].get('avgPulse'),0) , round(vals[0].get('minPulse'),0) , round(vals[0].get('avgPulseCount'),0))
        sql_command = sql_command + str(_vals) +";"
        self.writeValuesToDB(sql_command, values)                                 