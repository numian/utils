#!/usr/bin/env python

import sys, urllib2
from mailer import Mailer, Message

def send(url, email):
    """Sends a html page to an email. Requires a local smtp server and the mailer module"""
    html = urllib2.urlopen(url).read()
    
    mail = Message(From = "test",
                   To = email)
                   
    mail.Subject = "Test email"
    mail.Html = html
    
    sender = Mailer()
    sender.send(mail)
    
    

if __name__ == '__main__':

    arg_len = len(sys.argv)

    if arg_len < 2:
        print "No url defined or destination provided"
        print "Usage: python send-html2mail.py url email"
    else:
        send(sys.argv[1], sys.argv[2])
