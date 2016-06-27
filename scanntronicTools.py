# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 10:39:38 2016

@author: stapfg
"""

import imaplib
from email.parser import Parser
import StringIO
import pandas as pd
import time

#def convertDisplacements(array):
        
    
sensorDict = {
'Rissfox Mini RissMini031506':{'name':'RissFoxIntegralerStoss','sensors':
    {'03':'v_hor_unten','04':'v_ver_haus', '05':'v_ver_weg', 
    '06':'v_hor_oben_haus', '07':'v_hor_oben_web'}},
'Rissfox Mini RissMini031507':{'name':'RissFoxMitte','sensors':
    {'03':'v_hor_auflager', 
     '04':'t_unten_mitte', '05':'rF_unten_mitte',
     '06':'t_intStoss_oben', '07':'rF_intStoss_oben',
     '08':'t_oben_mitte', '09':'rF_oben_mitte'}},
'Thermofox Universal TU145295':{'name':'HygrofoxMitte','sensors':
    {'01':'t_surf_mitte_oben', '02':'t_surf_mitte_unten',
     '04':'u_haus_1cm', '05':'u_haus_6cm', '06':'u_haus_3cm'},
     '07':'u_unten_6cm', '08':'u_unten_20cm', '09':'u_unten_3cm', 
     '10':'u_unten_10cm', '11':'u_unten_1cm'},
'Thermofox Universal TU145296':{'name':'HygrofoxIntegralerStoss','sensors':
    {'01':'t_stangen', '02':'t_surf_intStoss_oben',
     '04':'u_intStoss_stirn', '05':'u_oben_intStoss_1cm',
     '06':'u_oben_intStoss_6cm','07':'u_oben_intStoss_3cm',
     '08':'u_linear', '09':'u_unten_intStoss_20cm', '10':'u_unten_intStoss_10cm',
     '11':'u_unten_intStoss_30cm'}}
}

def connectToExchange(url='EXCHANGE.mpa.loc', user = 'brueckemoni', 
                      password = 'Start123'):
    conn = imaplib.IMAP4_SSL(url)
    conn.login(user, password)
    conn.select('INBOX')
    return conn

def getMessageID_list(conn): 
    results, inboxData = conn.search(None,'ALL')
    msg_ids = inboxData[0]
    msg_id_list = msg_ids.split()
    return msg_id_list
    

def getMailAttachment(connection, mailID, AttachmentNr):
    """AttachmentNr starting with 1
    """
    result,data = connection.fetch(mailID,"(RFC822)")
    raw_email = data[0][1]
    p = Parser()
    msg = p.parsestr(raw_email)
    subject = msg.get('Subject')
    date_of_mail = msg.get('Date')
    mail_as_list = msg.get_payload()
    try:
        attachment = mail_as_list[AttachmentNr] # 0 is the message itself
        attachmentName =attachment.get_filename()
    except:
        attachment = None
        attachmentName = None
        print 'Anhang Nr. ', AttachmentNr, ' of mail ', mailID, ' does not exist.'
    return attachment, attachmentName, date_of_mail, subject
    
def calcDisplacement(value, zeroPoint, calValue):
    if value<0:
        value +=4095
    zeroedValue = value - zeroPoint
    out = zeroedValue - calValue
    return out
    

def getDataFrameFromAttachment(attachment):
    filecontent = attachment.get_payload()
    filecontent = filecontent.replace('=\r\n','')
    filecontent_list = filecontent.splitlines()
    logger = filecontent_list[3].strip()
    date_in_header = filecontent_list[5]
    data, lastDate = filecontent_list[-1].split('@')
    if len(lastDate) < 10:
        lastDate = lastDate + ' ' + date_in_header
    data = data.replace('-',',-')
    data = data.replace('+',',')
    data = data.replace(';,',';')
    data = data.replace(';','\n')
    dataIO = StringIO.StringIO(data)
    if filecontent_list[1] == '137':
        loggerType = 'Rissfox'
        frequency = filecontent_list[9].replace('m','Min')
        channels = filecontent_list[11].split(' ')
        zeroPoint = filecontent_list[17] + filecontent_list[19]*256
        calLen = filecontent_list[15] + filecontent_list[17]*256
        calLow = filecontent_list[25] + filecontent_list[27]*256
        calHigh = filecontent_list[29] + filecontent_list[31]*256
        calValue = calLen / ( calHigh - calLow)
        
    if filecontent_list[1] == '38':
        loggerType = 'Gigamodul'
        frequency = filecontent_list[7].replace('m','Min')
        channels = filecontent_list[9].split(' ')
    channels = channels[1:-1]
    df_raw = pd.read_table(dataIO, sep=',', names=channels)
    pdLastDate = pd.to_datetime(lastDate, dayfirst=True)
    index = pd.date_range(end=pdLastDate, periods=len(df_raw), freq = frequency)
    df_raw.index = index    
    dataIO.close()
    df = pd.DataFrame()
    for column in df_raw.columns:
        value = sensorDict[logger]['sensors'][column]
        if value[1] == 'v':
            df[value] = [x+4095 if x < 0 else x for x in df_raw[column]]
            df[value] = (df[value] - zeroPoint) * calValue
        else:
            df[value] = df_raw[column]/10.

                                
    return df
    
if __name__ == '__main__':
    conn = connectToExchange()
    msg_id_list = getMessageID_list(conn)
    latest_email_id = msg_id_list[-51]
    attachment, name, date, subject = getMailAttachment(conn, latest_email_id, 1)
    print date, name, subject
    if name:
        df = getDataFrameFromAttachment(attachment)
    else:
        print 'No attachment'
    print df[-5:]
