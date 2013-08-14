#!/usr/bin/python
# -*- coding: latin-1 -*-
# File			: godown.py 
# description	: do some work while system shutdown
#				  called by down_to_iot_units (in folder init.d) while system shutdown procedure 
# autor			: c2013, Markus Gasser

import sys
import mydb
import mailer
import mysystem
import datetime
import time
import socket


# get ip-address, wlan or lan depends on current usage
try:
	myip = str(mysystem.get_ip_address('wlan0'))
except:
	myip = str(mysystem.get_ip_address('eth0'))

# get actual date and time 
localtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# get unitname from inifile
myunitname = mysystem.inifile_read("UNIT", "unit_name")

# get location from inifile
mylocation = mysystem.inifile_read("UNIT", "unit_location")

# mySN is used as sn, moniker for unique identifier of a unit
mySN = mysystem.getserial()

mymessage = """
			<b>Raspberry Pi wird heruntergefahren</b><br><br>
			<table border="0">
				<tr>
					<td>Zeit</td>
					<td>: """ + localtime + """</td>
				</tr>	
				<tr>
					<td>Unit</td>
					<td>: """ + myunitname + """</td>
				</tr>
				<tr>
					<td>Unit Standort</td>
					<td>: """ + mylocation + """</td>
				</tr>				
				<tr>
					<td>SN</td>
					<td>: """ + mySN + """</td>
				</tr>				
				<tr>
					<td>IP</td>
					<td>: """ + myip + """</td>
				</tr>
			</table>
			"""
	
mydb.update_this_unit("03","DOWN")
mysystem.inifile_write("UNIT", "unit_name", myunitname)
mysystem.inifile_write("IP", "ip_address", myip)
mailer.send_mail(myunitname + " Shutdown",mymessage)