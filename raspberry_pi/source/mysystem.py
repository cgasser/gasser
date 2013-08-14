#!/usr/bin/python
# -*- coding: latin-1 -*-
# File			: mysystem.py 
# description	: module to Raspberry Pi system things
# autor			: c2013, Markus Gasser

import socket
import fcntl
import struct
import ConfigParser
import string

#------------------------------------------------------------------
# def getserial
#	description	: get serial-number of this Raspberry Pi module(Unit)
#
#	input		: nothing
#
#	output		: serial-number, String 
#
#	use	/ call	: mysystem.getserial()
#	created		: 2013-08-05, Markus Gasser
#	modified	: 2013-08-05, Markus Gasser
#------------------------------------------------------------------
def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"

  return cpuserial
  

#------------------------------------------------------------------
# def get_ip_address
#	description	: get serial-number of this Raspberry Pi module(Unit)
#
#	input		: ifname, String
#				  'lo' 		= Local adress (172.0.0.0)
#				  'eth0' 	= LAN address(xxx.xxx.xxx.xxx)
#				  'wlan0' 	= WLAN address (xxx.xxx.xx.xxx)
#
#	output		: IP-address, String 
#
#	use	/ call	: mysystem.get_ip_address(['lo']¦['eth0']¦['wlan0']))
#	created		: 2013-08-07, Markus Gasser
#	modified	: 2013-08-07, Markus Gasser
#------------------------------------------------------------------
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

#------------------------------------------------------------------
# def inifile_read
#	description	: read ini-file data /home/pi/Development/iot_unit.ini
#
#	input		: aSection, String
#				  aAttribute, String
#
#	output		: data of attribute 
#
#	use	/ call	: mysystem.inifile_read("Section","Attribut")
#	created		: 2013-08-09, Markus Gasser
#	modified	: 2013-08-09, Markus Gasser
#
#Inifile:
#--------
#[Section1]
#Attribute1 = Data1
#Attribute2 = Data2
#
#[aSection2]
#Attribute3 = Data3
#Attribute4 = Data4
#
#------------------------------------------------------------------	
def inifile_read(aSection, aAttribute):	
	config = ConfigParser.ConfigParser()
	config.read("/home/pi/Development/iot_unit.ini")
	return config.get(aSection, aAttribute)


#example for reading hole inifile
# dump entire config file
#for section in config.sections():
#    print section
#    for option in config.options(section):
#        print " ", option, "=", config.get(section, option)
	
#------------------------------------------------------------------
# def inifile_write
#	description	: write inifile data to /home/pi/Development/iot_unit.ini
#
#	input		: aSection, String
#				  aAttribute, String
#				  aData, String
#
#	output		: none 
#
#	use	/ call	: mysystem.inifile_read("Section","Attribute","Data")
#	created		: 2013-08-09, Markus Gasser
#	modified	: 2013-08-09, Markus Gasser
#------------------------------------------------------------------	
def inifile_write(aSection, aAttribute, aData):
	config = ConfigParser.ConfigParser()
	config.read("/home/pi/Development/iot_unit.ini")
	cfgfile = open("/home/pi/Development/iot_unit.ini",'w')
	config.set(aSection, aAttribute, aData)
	config.write(cfgfile)



