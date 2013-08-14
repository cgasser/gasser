#!/usr/bin/python
# -*- coding: latin-1 -*-
# File			: goup.py 
# description	: do some work while system startup
#				  called by /ect/rc.local while system boot 
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

# get hostname from inifile
myunitname = mysystem.inifile_read("UNIT", "unit_name")

# get location from inifile
mylocation = mysystem.inifile_read("UNIT", "unit_location")

# mySN is used as sn, moniker for unique identifier of a unit
mySN = mysystem.getserial()



mymessage = """
			<b>Raspberry Pi wird gestartet</b><br><br>
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
mydb.update_this_unit("03","STARTUP")			
mailer.send_mail(myunitname + " Startup",mymessage)