# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 09:31:00 2016

@author: stapfg
"""

import smtplib
from email.mime.text import MIMEText

def sendWarningMail():
    loginDatei = open('./login.txt','r')
    exec(loginDatei.read())
    loginDatei.close()

    server = smtplib.SMTP(host=url, port=port)
    server.starttls()
    server.login(user, password)
    toaddr = "gordian.stapf@mpa.uni-stuttgart.de"
    fromaddr = "bruecke.monitoring@mpa.uni-stuttgart.de"
    text = 'Das Skript funktioniert nicht'
    
    msg = MIMEText(text)
    msg['Subject'] = 'test warn mail'
    msg['From'] = fromaddr
    msg['To'] = toaddr

    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()
if __name__ == '__main__':
    sendWarningMail()
