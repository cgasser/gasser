#!/usr/bin/python
# -*- coding: latin-1 -*-
# File			: update_iot_units.py 
# description	: module to update status in MySQL database table iot_units
#				  used by crontab, called every minute
# autor			: c2013, Markus Gasser

import mydb

mydb.create_table_units(False)
mydb.update_this_unit("03","ACTIVE")