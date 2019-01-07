#!/usr/bin/python
# Values for the gy-30 sensor
# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

# declarations

#Werte zum lesen aus den ConfigFiles
_cfg_entry_Adapter_WLAN = 'AdapterWLAN'
_cfg_entry_Adapter_LAN= 'AdapterLAN'
_cfg_unit = 'Unit'
_cfg_network = 'Network'
_cfg_entry_Font_Text = 'Font_Text'

_cfg_section_display = 'DisplayConfig'
_cfg_entry_pin_display = 'RasperryPin'
_cfg_entry_SPI_DEVICE = 'SPI_DEVICE'
_cfg_entry_SPI_PORT = 'SPI_PORT'
_cfg_entry_DC = 'DC'

_cfg_section_system = 'System'
_cfg_entry_loglevel = 'loglevel'
_cfg_entry_debug = 'systemDebug'
_cfg_entry_debug_IP = 'systemDebugIP'

_cfg_entry_Default_font = 'Font_Display'
_cfg_entry_font = 'Font'
_cfg_entry_location = 'Location'
_cfg_entry_Size = 'Size'
_cfg_entry_Adapter = 'Adapter'
_cfg_section_unit = 'Unit'
_cfg_section_Network = 'Network'
_cfg_section_database = 'DatabaseServer'
_cfg_section_lcldatabase = 'LocalDatabase'
_cfg_entry_database_host = 'ServerName'
_cfg_entry_database_user = 'DatabaseUser'
_cfg_entry_database_pwd = 'DatabasePassword'
_cfg_entry_database_table = 'DatabaseTable'
_cfg_entry_database_schema = 'DatabaseSchema'
_cfg_entry_databaseupdIntervall = 'UpdateIntervall'
_cfg_entry_Pressure_Unit = 'Pressure'
_cfg_entry_Temperature_Unit = 'Temperature'
_cfg_entry_Humidity_Unit = 'Humidity'
_cfg_entry_SignalStrength_Unit = 'SignalStrength'
_cfg_entry_Font_Temperature = 'Font_Temperature'
_cfg_entry_Font_Humidity = 'Font_Humidity'
_cfg_entry_Font_Pressure = 'Font_Pressure'
_cfg_entry_Font_Text = 'Font_Text'
_cfg_entry_Font_Network = 'Font_Network'
_cfg_section_TextStation = "Text_Station"
_cfg_entry_NameOfStation = 'NameOfStation'
_cfg_entry_sensor_pin = 'sensor_pin'

#weather parameter
_temperature = 'Temperature'
_humidity = 'Humidity'
_illum = 'Illumination'
_pressure = 'Pressure'
_altitude = 'Altitude'
_windspeed = 'Windspeed'
_anemometer = 'Anemometer'
_pulse = 'Pulse'

#Sensors
_sens_dht22 = 'DHT22'
_sens_bmp085 = 'BMP085'

#location of config files
_cfg_system = 'configuration/system.ini'
_cfg_server = 'configuration/server.ini'
_cfg_locales_de = 'configuration/locales_de.ini'
_cfg_display = 'configuration/display.ini'
_cfg_sensor = 'configuration/sensor.ini'

#Errormessages
_err_no_connection = "no network connection found"
