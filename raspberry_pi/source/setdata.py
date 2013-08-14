#!/usr/bin/python
# -*- coding: latin-1 -*-
# File			: setdata.py 
# description	: 
# autor			: c2013, Markus Gasser

import mysystem

def print_options():

	print "UNIT"
	print "-----------------------------------------------------------------"
	print "0 = Name        : " + mysystem.inifile_read('UNIT','unit_name')
	print "1 = Standort    : " + mysystem.inifile_read('UNIT','unit_location')
	print "2 = FQDN        : " + mysystem.inifile_read('UNIT','unit_fqdn')
	print "3 = Typ         : " + mysystem.inifile_read('UNIT','unit_type')
	print "4 = Typ-Namen   : " + mysystem.inifile_read('UNIT','unit_type_names')
	print ""

	print "IP"
	print "-----------------------------------------------------------------" 
	print "0 = IP-Adresse  : " + mysystem.inifile_read("IP","ip_address")
	print "0 = Subnet-Maske: " + mysystem.inifile_read("IP","ip_subnet")
	print "0 = Gateway     : " + mysystem.inifile_read("IP","ip_gateway")
	print("")
	
	print "OS"
	print "-----------------------------------------------------------------" 
	print "0 = Name        : " + mysystem.inifile_read("OS","os_name")
	print "0 = Version     : " + mysystem.inifile_read("OS","os_version")
	print ""

eingabe = ""
again = True
while again:
	print("")
	print_options()
	eingabe = raw_input("Nummer (q=exit) : ") 
	if eingabe=="1":
		newdata = raw_input("Neuer Standort ist: ")
		mysystem.inifile_write('UNIT','unit_location',newdata)
	elif eingabe=="2": 
		newdata = raw_input("Neuer FQDN lautet: ")
		mysystem.inifile_write('UNIT','unit_fqdn',newdata)
	elif eingabe=="3": 
		newdata = raw_input("Neuer Unittyp(01=Actor,02=Sensor,03=Actor und Sensor) lautet: ")
		mysystem.inifile_write('UNIT','unit_type',newdata)
	elif eingabe=="4": 
		newdata = raw_input("Neue(r) Typnamen (getrennt durch ';') lautet: ")
		mysystem.inifile_write('UNIT','unit_type_names',newdata)
	elif eingabe=="0": 
		print ("Diese Option ist durch das System vorgegeben oder\nmuss mit raspi-setup gesetzt werden\n")
	elif eingabe=="q": 
		again=False
	else:         # default:
		print(eingabe + " ist keine gültige Option\n")