#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configuration.constants as const
from PIL import Image, ImageDraw, ImageFont
import Adafruit_GPIO.SPI as SPI
import lib.Adafruit_SSD1306 as Adafruit_SSD1306
#from lib.handler.SensorHandler import SensorHandler
from lib.wifi.iwlibs import Wireless
import ConfigParser
from lib.logger.WeatherLogger import WeatherLogger
from lib.error.Error import Error

class DisplayChange(object):
    """
    First class which ask who is listening to it
    """
    global dispHandler

    def __init__(self, event_dispatcher):

        # Save a reference to the event dispatch
        self.event_dispatcher = event_dispatcher

        # Listen for the RESPOND event type
        self.event_dispatcher.add_event_listener(
            ButtonDispChangeEvent.NEW_PAGE, self.on_page_change_event
        )
        self.dispHandler = DisplayHandler()

    def on_page_change_event(self, event):
        self.dispHandler.displayData()


class DisplayHandler():
    global config
    global textConfig
    global wLog

    _weatherData = {}
    _disp = Adafruit_SSD1306.SSD1306_128_64(24)
    _font2 = None
    _font = None
    _wlog = None
    
    #_serverConfig = ConfigParser.RawConfigParser()
        
    def __init__(self, configuration):
        self._wlog = configuration.getLogger()
        self._systemConfig = configuration.getSystemConfig()
        self._displayConfig = configuration.getDisplayConfig()
        self._textConfig = configuration.getLocaleConfig()
        sensorPin = self._systemConfig.get(const._cfg_section_display,const._cfg_entry_pin_display)
        self._wlog.logDebugMessage("Display SensorPin was set to: "+sensorPin)
        # Raspberry Pi pin configuration:
        RST = int(sensorPin)
        # Note the following are only used with SPI:
        DC = self._systemConfig.get(const._cfg_section_display,const._cfg_entry_DC)
        self._wlog.logDebugMessage("Display SPI DC was set to: "+DC)
        SPI_PORT = self._systemConfig.get(const._cfg_section_display, const._cfg_entry_SPI_PORT)
        self._wlog.logDebugMessage("Display SPI_PORT was set to: "+SPI_PORT)
        SPI_DEVICE = self._systemConfig.get(const._cfg_section_display,const._cfg_entry_SPI_DEVICE)
        self._wlog.logDebugMessage("Display SPI_DEVICE was set to: "+SPI_DEVICE)
        
        self._defaultAdapter = self._systemConfig.get(const._cfg_section_Network,const._cfg_entry_Adapter)
        self.wifi = Wireless(self._systemConfig.get(const._cfg_section_Network,self._defaultAdapter))
        self._wlog.logDebugMessage("Networkadapter was set to:"+str(self.wifi))

        self.page = 0
        self.line1Counter = 0
        self._wlog.logDebugMessage("Initialize Display on pin: "+str(RST))
        self._disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
        #  Initialize library.
        self._disp.begin()
        # Clear display.
        self._disp.clear()
        self._disp.display()
        self._wlog.logDebugMessage("Initialize Display done")
    
    def setSystemState(self, ip):
        self._ip = ip
    
    def readTextConfigutation(self, text, section, item):
        self._wlog.logDebugMessage("Read font")
        # Load font configuration.
        return ImageFont.truetype(self.getFontLocation(text), int(self._displayConfig.get(section,item)))

    def getFontLocation(self, font):
        #load font configuration
        fontHeaderType = self._displayConfig.get(font,const._cfg_entry_font)
        self.fontLocation =''
        fontHeaderLocation =''
        if fontHeaderType == const._cfg_entry_Default_font:
            self.fontHeaderLocation = self._displayConfig.get(const._cfg_entry_Default_font,const._cfg_entry_location)
        else:
            self.fontHeaderLocation = self._displayConfig.get(font,const._cfg_entry_location)

        self._wlog.logDebugMessage("return Font location: "+str(self.fontHeaderLocation)+' for key: '+font)
        return self.fontHeaderLocation

    def getFontSize(self, font):
        #load font configuration
        self.fontHeaderSize = self._displayConfig.get(font,const._cfg_entry_Size)
        if self.fontHeaderSize == const._cfg_entry_Default_font:
            self.fontHeaderSize = self._displayConfig.get(const._cfg_entry_Default_font,const._cfg_entry_Size)
        else:
            self.fontHeaderSize = self._displayConfig.get(font,const._cfg_entry_Size)
        self._wlog.logDebugMessage("return Font Size: "+str(self.fontHeaderSize)+' for key: '+font)
        return self.fontHeaderSize

    def setCurrentData(self, weatherData):
        self._weatherData = weatherData

    def displayData(self):
        self._wlog.logDebugMessage("displayData prosessed")
        self.preparePage()
        self.displayPage()
        self._disp.image(self.image)
        self._disp.display()

    def preparePage(self):
        self._wlog.logDebugMessage("preparePage prosessed")
        self.image = Image.new('1', (self._disp.width, self._disp.height))
        self.draw = ImageDraw.Draw(self.image)
        self._disp.clear()

    def displayPage(self):
        self._wlog.logDebugMessage("displayPage prosessed")
        self.page = self.page + 1
        self.writeNextPage()

    def writeNextPage(self):
        self._wlog.logDebugMessage("writeNextPage prosessed")
        section = 'page_' + str(self.page)
        self._wlog.logDebugMessage("section "+ section+" prosessed") 
        self.line1Counter = 0
        try:
            if self._displayConfig.has_section(section):
                font = self.readTextConfigutation(const._cfg_entry_Font_Text,section, 'header_size')
                self.preparePage()
                self.writeHeader(font)
                self.drawNetworkStatus(font)
                self.page_options = self._displayConfig.options(section)
                sensors = self._displayConfig.get(section, 'line1')
                vals = sensors.split(',')
                headerSize = self._displayConfig.get(section, 'line1_Size')
                sensors2 = self._displayConfig.get(section, 'line2')
                lineSize = self._displayConfig.get(section, 'line2_Size')
                vals2 =  sensors2.split(',')
            else:
                self.page = 1
                section = 'page_' + str(self.page)
                font = self.readTextConfigutation(const._cfg_entry_Font_Text,section, 'header_size')
                self.preparePage()
                self.writeHeader(font)
                self.drawNetworkStatus(font)
                self.page_options = self._displayConfig.options(section)
                sensors = self._displayConfig.get(section, 'line1')
                headerSize = self._displayConfig.get(section, 'line1_Size')
                vals = sensors.split(',')

                sensors2 = self._displayConfig.get(section, 'line2')
                lineSize = self._displayConfig.get(section, 'line2_Size')
                vals2 =  sensors2.split(',')
        except Error as e:
            self._wlog.logDebugMessage('sections is no page setup section: '+ section)
            self.page = 1
            section = 'page_' + str(self.page)
            font = self.readTextConfigutation(const._cfg_entry_Font_Text,section, 'header_size')
            self.writeHeader(font)
            self.drawNetworkStatus(font)
            self.page_options = self._displayConfig.options(section)
            headerSize = self._displayConfig.get(section, 'header_size')
            sensors = self._displayConfig.get(section, 'line1')
            vals = sensors.split(',')
            sensors2 = self._displayConfig.get(section, 'line2')
            lineSize = self._displayConfig.get(section, 'line2_Size')
            vals2 =  sensors2.split(',')
        #print(self._weatherData)

        if len(self._weatherData) > 0:
            for option in vals:
                val = self._weatherData[0].get(option.strip())
                self._font = self.readTextConfigutation(const._cfg_entry_Font_Text,section, 'line1_Size')
                self.unit = self._textConfig.get(const._cfg_section_unit, option.lstrip() )
                if val == None:
                    val = 0
                self.writeLine1(val, self.unit, self._font)

            for option2 in vals2:
                val2 = self._weatherData[0].get(option2.strip())
                self._font2 = self.readTextConfigutation(const._cfg_entry_Font_Text,section, 'line2_Size')
                self.unit2 = self._textConfig.get(const._cfg_section_unit, option2.lstrip() )
                if val == None:
                    val = 0
                self.writeText1Line2(val2, self.unit2, self._font2)

    def writeHeader(self, font):
        self._wlog.logDebugMessage("write Header")
        self.draw.text((0, 0), self._textConfig.get(const._cfg_section_TextStation,const._cfg_entry_NameOfStation), font=font, fill=(128))

    def writeLine1(self, value, unit, font):
        self.line1Counter = self.line1Counter + 1
        xPosition = 0
        if self.line1Counter == 0:
            xPosition = 0
        elif self.line1Counter == 1:
            xPosition = 80
        self.draw.text((xPosition, 15), str(round(float(value),1))+' '+str(unit), font=font, fill=(128))

    def initCounter(self):
        self.line1Counter = 0

    def writeText1Line2(self, value, unit, size):

        if value == None:
            value = 0
        self.draw.text((0, 30), str(round(value,1))+' '+str(unit), font=size, fill=(128))

    def drawNetworkStatus(self, font):
        
        if self.wifi.getStatistics() <> None and self._defaultAdapter == const._cfg_entry_Adapter_WLAN:
            if self.wifi.getStatistics()[1].getSignallevel() <= 8:
                self.draw.text((95,0), str(self.wifi.getStatistics()[1].getSignallevel())+self._textConfig.get(const._cfg_section_unit,const._cfg_entry_SignalStrength_Unit), font=font, fill=(128))

            elif self.wifi.getStatistics()[1].getSignallevel() <= 10 and self.wifi.getStatistics()[1].getSignallevel() > 20:
                self.draw.line((110,8,110,10), 5)
            elif self.wifi.getStatistics()[1].getSignallevel() <= 20 and self.wifi.getStatistics()[1].getSignallevel() > 30:
                self.draw.line((112,6,112,10), 5)
                self.draw.line((110,8,110,10), 5)

            elif self.wifi.getStatistics()[1].getSignallevel() <= 50 and self.wifi.getStatistics()[1].getSignallevel() > 30:
                self.draw.line((114,4,114,10), 5)
                self.draw.line((112,6,112,10), 5)
                self.draw.line((110,8,110,10), 5)

            elif self.wifi.getStatistics()[1].getSignallevel() <= 70 and self.wifi.getStatistics()[1].getSignallevel() > 50:
                self.draw.line((116,2,116,10), 5)
                self.draw.line((114,4,114,10), 5)
                self.draw.line((112,6,112,10), 5)
                self.draw.line((110,8,110,10), 5)

            elif self.wifi.getStatistics()[1].getSignallevel() > 70:
                self.draw.line((118,0,118,10), 5)
                self.draw.line((116,2,116,10), 5)
                self.draw.line((114,4,114,10), 5)
                self.draw.line((112,6,112,10), 5)
                self.draw.line((110,8,110,10), 5)
            else:
                self.draw.text((70,0), str(self.wifi.getStatistics()[1].getSignallevel()) + '%', font=self._font2, fill=(128))
        elif self._ip and self._defaultAdapter == _cfg_entry_Adapter_LAN:
            self.draw.text((100,0), str( 'Net'), font=self._font, fill=(128))
        else:
            self.draw.text((100,0), str( 'lcl'), font=self._font, fill=(128))
