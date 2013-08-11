#!/usr/bin/python
# -*- coding: latin-1 -*-
# File			: mydb.py 
# description	: module to provide database functionality for MySQL database
# autor			: c2013, Markus Gasser

import MySQLdb
import sys
import mysystem
import time
import datetime
import socket

#------------------------------------------------------------------
# def open_db
#	description	: open a MySQL - database, tables formated as utf8 (latin-1)
#
#	input		: aHost, String 	(IP or hostname of databes holding)
#				  aUser, String 	(username as part of databse credential)
#				  aPassword, String (password as part of database credential)
#
#	output		: a instance of databse connection or 
#				  error code(-1) in case of failure
#
#	use	/ call	: mydb.open_db('www.gasser-net.com', 'username', 'password')
#	created		: 2013-08-05, Markus Gasser
#	modified	: 2013-08-06, Markus Gasser
#------------------------------------------------------------------
def open_db(aHost, aDB, aUser, aPassword):
	try:
		db = MySQLdb.connect(host=aHost, user=aUser, passwd=aPassword, db=aDB, charset = "utf8", use_unicode = False)
		return db		
	except MySQLdb.Error, e:
		try:
			# used for debug reasons
			#print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
			pass
		except:
			# used for debug reasons
			#print ("MySQL Error: %s" % str(e))
			pass
		finally:
			return -1

#------------------------------------------------------------------
# def close_db
#	description	: close a previously opened database
#
#	input		: aDB, instance of open database
#	output		:  1 = database closed
#				  -1 = fault, could not close database or database(aDB) periously not opend
#
#	use	/ call	: mydb.open_db(databasecnnection)
#	created		: 2013-08-05, Markus Gasser
#	modified	: 2013-08-05, Markus Gasser
#------------------------------------------------------------------
def close_db(aDB):
	try:
		aDB.close()
		return 1		
	except:
		return -1

		
#------------------------------------------------------------------
# def create_table_units
#	description	: first create table iot_units and 
#				  then insert this unit in the table iot_units,
#				  (deppend on aallways_create)
#
#	input		: aallways_create, Boolean 
#				  TRUE 	= existing table will be deleted and then created
#				  FALSE = table will be created if the table not already exists 
#	output		:  1 	= table exists already or created
#				  -1 	= error while trying to create table or 
#						  trying to insert this unit in created table
#
#	use	/ call	: mydb.create_table_units([TRUE]¦[FALSE])
#	created		: 2013-08-05, Markus Gasser
#	modified	: 2013-08-07, Markus Gasser
#---------------
#	definitions
#---------------
#	sn			:	serialnumber of this unit
#	hostname	:		
# 	type		:	01 = unit acts as a sensor
#					02 = unit acts as a actor
#					03 = unit acts as a sensor and as a actor
#	status		:	status of actifity [ACTIVE]¦[DOWN]
#	IP			:	IP-address of this unit mostly not accesseble outher subnet
#	hostFQDN	:	Fully Qualified Domain Name of this unit/host
#	installed	:	date and time of installation(database view)
#	current		:	date and time of last pull
#------------------------------------------------------------------
def create_table_units(aallways_create):
	# Open Database
	db = open_db("www.gasser-net.com","gasserne_raspi","gasserne_raspi","raspiwetter")

	# create a cursor for the select
	cur = db.cursor()
	
	if aallways_create:
		try:
			cur.execute("DROP TABLE IF EXISTS iot_units")			
		except:
			pass
		finally:
			pass

	try:
		cur.execute("""CREATE TABLE IF NOT EXISTS iot_units 
			(
				sn			VARCHAR(25),
				hostname	VARCHAR(40),
				type		VARCHAR(10),
				status		VARCHAR(50),
				IP			VARCHAR(25),
				hostFQDN	VARCHAR(200),
				installed	DATETIME, 
				current		TIMESTAMP, 				
				PRIMARY KEY (sn)
			)	
		""")		
		return 1		
	except:
		return -1		
	finally:
		# close cursor and database
		cur.close()
		close_db(db)

		
#------------------------------------------------------------------
# def delete_table_units
#	description	: delete table iot_units
#				  coution, all units will be erased
#
#	input		: none
#	output		:  0 = table deleted
#				  -1 = fault, table could not be erased
#
#	use	/ call	: mydb.delete_table_units()
#	created		: 2013-08-05, Markus Gasser
#	modified	: 2013-08-05, Markus Gasser
#------------------------------------------------------------------
def delete_table_units():
	# open database
	db=open_db("www.gasser-net.com","gasserne_raspi","gasserne_raspi","raspiwetter")

	# create a cursor for the select
	cur = db.cursor()
	
	try:
		# erase table [mySerialNumber]
		cur.execute ("DROP TABLE IF EXISTS iot_units")
		return 1		
	except:
		return -1				
	finally:
		# close cursor and database
		cur.close()
		close_db(db)


#------------------------------------------------------------------
# def update_this_unit
#	description	: insert this unit into table iot_units
#
#	input		: aType, String 	(type of this unit)
#				  aStatus, String 	(aktual status of this unit)
#				  
#	output		:  1 = insert
#				   2 = update
#				  -1 = falid to do a insert
#				  -2 = falid to do a update
#
#	use	/ call	: mydb.update_this_units(['001']-['nnn'],[active]¦[not active])
#	created		: 2013-08-05, Markus Gasser
#	modified	: 2013-08-07, Markus Gasser
#------------------------------------------------------------------	
def update_this_unit(aType, aStatus):	

	# get serialnumber of this Raspberry pi (used for table name)
	# mySN is used as sn, moniker for unique identifier of a unit
	mySN = mysystem.getserial()
	
	# get ip-address, wlan or lan depends on current usage
	try:
		myip = str(mysystem.get_ip_address('wlan0'))
	except:
		myip = str(mysystem.get_ip_address('eth0'))

	#localtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	n = datetime.datetime.now()
	unix_time = time.mktime(n.timetuple())
	
	# get hostname of this unit
	myhostname = socket.gethostname()

	# get hostFQDN of this unit (Fully Qualified Domain Name)
	myhostFQDN = "none"
	
	# open database
	db = open_db("www.gasser-net.com","gasserne_raspi","gasserne_raspi","raspiwetter")

	# create a cursor
	cur = db.cursor()
	
	# check if a record of this unit allredy exists
	cur.execute("""SELECT sn FROM iot_units WHERE sn=%s""", (mySN))
	print (cur.rowcount)
	if cur.rowcount <= 0:
		# insert a new record
		try:
			cur.execute("""INSERT INTO iot_units(sn,hostname,type,status,ip,hostFQDN,installed) 
						VALUES
							(
								%s, %s, %s, %s, %s, %s, FROM_UNIXTIME(%s)
							) 
						""", 
						(mySN,myhostname,aType,aStatus,myip,myhostFQDN,unix_time))
			return 1
		except:
			return -1
		finally:
			# close cursor and database
			cur.close()
			close_db(db)
			
	else:
		# update record
		try:
			cur.execute("""UPDATE iot_units 
							SET hostname=%s, type=%s, status=%s, ip=%s, hostFQDN=%s, current=FROM_UNIXTIME(%s)
							WHERE sn = %s 
						""", 
						(myhostname,aType,aStatus,myip,myhostFQDN,unix_time,mySN))
			return 2			
		except:	
			return -2
			# Rollback in case there is any error
			db.rollback()
		finally:			
			# close cursor and database
			cur.close()
			close_db(db)