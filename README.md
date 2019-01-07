# weather_v2 - the project is still in development

The project is an python raspi implemntation to collect several weather information. These informations are written in a remote database. In case the remote database is not available all data is stored in a local sqlite database. If the remote database is available again all local data are transferred to the remote database.
The weather station is equiped with the following sensor
1. DHT22
2. BMP085
3. GY-30
4. MCP3008 8-Channel 10-Bit ADC
5. 128 x 64 Pixel 0,96 Zoll OLED I2C Display
6. Eltako Windsensor - reedcontact sensor

There are several configuration options using the configuration files in the configuration folder.

The display.ini defines the options for displaying the values on the local OLED display.

The server.ini is intended to define values for the remote database.

The system.ini is intended defines the network connection to be used(wlan0 or eth0). In case of a wlan connection the signal strengh is diplayed on the local OLED display.

The log.ini defines the logger module.

The locales.ini is intended to defines the names for the values on the OLED display
