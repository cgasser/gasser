#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# send email via smtp
# 2013-06-06 V0.2 by Thomas Hoeser
#
 
import sys
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mail_server   = 'mail.gasser-net.com'            				# Mail Server
mail_account  = 'markus@gasser-net.com'    						# name of mail account
mail_password = 'gam0257'            							# password
addr_sender   = 'raspi@gasser-net.com'    						# sender email
addr_receiver = 'markus@gasser-net.com;margas@datacomm.ch'    	# receiver email

 # --------------------------------------------------------------------------------
def send_mail(title,message):

	debug_level = 0 # set to 1 to get more messages
    # Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = title
	msg['From'] = addr_sender
	msg['To'] = addr_receiver
     
    # Create the body of the message (a plain-text and an HTML version).
	text = message

	html = """\
	<html>
	<head></head>
	<body>
	<h>
	"""

	html += message
	html += """\
	</h>
	</body>
	</html>
	"""
	# print html
         
	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	# Attach parts into message container.
	msg.attach(part1)
	msg.attach(part2)

	#mailsrv = smtplib.SMTP(mail_server)
	#mailsrv.login(mail_account,mail_password)
	#mailsrv.sendmail(addr_sender, addr_receiver, msg.as_string())
	#mailsrv.quit()
	#return()

	try:
		if debug_level > 0: 
			print "smtplib.SMTP:", mail_server
		mailsrv = smtplib.SMTP(mail_server) # Send the message via local SMTP server.
	except:
		print "Error: unable to send email - smtp server"
		print "Server on ", mail_server, " cannot be reached or service is down"
		return()

	try:
		if debug_level > 0: 
			print "mailsrv.login:", mail_account,  mail_password
		mailsrv.login(mail_account,mail_password)
	except:
		print "Error: unable to send email - login failed"
		print "login is not valid - check name and password:",mail_account,mail_password
		return()

	try:
		# sendmail function takes 3 arguments: sender's address, recipient's address and message to send - here it is sent as one string.
		if debug_level > 0: 
			print "mailsrv.sendmail:", addr_sender,  addr_receiver
		mailsrv.sendmail(addr_sender, addr_receiver, msg.as_string())
		mailsrv.quit()
		print "Successfully sent email"
	except:
		print "Error: unable to send email - wrong address"
		print "mail address for sender or receiver invalid:",addr_sender,addr_receiver

	version = '0.2'