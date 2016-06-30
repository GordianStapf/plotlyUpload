# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 10:39:38 2016

@author: stapfg
"""

import imaplib
from email.parser import BytesParser
import io
import pandas as pd
import sqlite3
import re

#def convertDisplacements(array):
        
    
sensorDict = {
'Rissfox Mini RissMini031506':{'name':'RissFoxIntegralerStoss','sensors':
    {'03':'v_hor_unten','04':'v_ver_haus', '05':'v_ver_weg', 
    '06':'v_hor_oben_haus', '07':'v_hor_oben_weg'}},
'Rissfox Mini RissMini031507':{'name':'RissFoxMitte','sensors':
    {'03':'v_hor_auflager', 
     '04':'t_unten_mitte', '05':'rF_unten_mitte',
     '06':'t_intStoss_oben', '07':'rF_intStoss_oben',
     '08':'t_oben_mitte', '09':'rF_oben_mitte'}},
'Thermofox Universal TU145295':{'name':'HygrofoxMitte','sensors':
    {'01':'t_surf_mitte_oben', '02':'t_surf_mitte_unten',
     '04':'u_haus_1cm', '05':'u_haus_6cm', '06':'u_haus_3cm',
     '07':'u_unten_6cm', '08':'u_unten_20cm', '09':'u_unten_3cm', 
     '10':'u_unten_10cm', '11':'u_unten_1cm'}},
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
    
global msg
def getMailAttachment(connection, mailID, AttachmentNr):
    """AttachmentNr starting with 1
    """
    result,data = connection.fetch(mailID,"(RFC822)")
    raw_email = data[0][1]
    p = BytesParser()
    msg = p.parsebytes(raw_email)
    sender = msg.get('From')
    subject = msg.get('Subject')
    date_of_mail = msg.get('Date')
    mail_as_list = msg.get_payload()
    try:
        attachment = mail_as_list[AttachmentNr] # 0 is the message itself
        attachmentName = attachment.get_filename()
    except:
        attachment = None
        attachmentName = None
        print('Anhang Nr. ', AttachmentNr, ' of mail ', mailID, ' does not exist.')
    if 'Remotefox' not in sender:
        attachment = None
        attachmentName = None     
    return attachment, attachmentName, date_of_mail, subject
    
def calcDisplacement(value, zeroPoint, calValue):
    if value<0:
        value +=4095
    zeroedValue = value - zeroPoint
    out = zeroedValue - calValue
    return out
    
def initTables(dict):
    for key in dict.keys():
        df = pd.DataFrame(columns=dict[key]['sensors'].values())
        table = dict[key]['name']
        dbfile = r'M:\Abteilung\_Mitarbeiter\Stapf\bruecke\scanntronicDaten.sqlite'
        cnx = sqlite3.connect(dbfile)
        df.to_sql(table, cnx, flavor='sqlite', if_exists='append', 
              index=True, index_label='timestamp')
        cnx.close()
    
def getDataFrameFromAttachment(attachment):
    filecontent = attachment.get_payload(decode=True)
    #print(type(filecontent))
    filecontent = filecontent.replace(b'=\r\n',b'')
    print(filecontent[-100:])
    filecontent_list = filecontent.splitlines()
    logger = filecontent_list[3].strip()
    date_in_header = filecontent_list[5]
    print(logger)
    if len(filecontent_list[-1]) == 0:
        filecontent_list.pop()
    #print(filecontent_list[-2:][-100:])
    data, lastDate = filecontent_list[-1].split(b'@')
    if len(lastDate) < 10:
        lastDate = lastDate + b' ' + date_in_header
    data = data.replace(b'-',b',-')
    data = data.replace(b'+',b',')
    data = data.replace(b';,',b';')
    data = data.replace(b';',b'\n')
    if b'!' in data:
        normal_line = re.findall(b'\n([^!]*?)\n',data)[0]
        nan_line = re.sub(b'-?\d+',b'nan',normal_line)
        def repl(matchobj):
            return int(matchobj.groups()[0])*(b'\n'+nan_line)
        data = re.sub(b'!,(\d\d\d)', repl, data)
            
    data = data.replace(b'!',b'')
    dataIO = io.BytesIO(data)
    if filecontent_list[1] == b'137':
        frequency = filecontent_list[9].replace(b'm',b'Min')
        channels = filecontent_list[11].split(b' ')
        zeroPoint = int(filecontent_list[17]) + int(filecontent_list[19])*256
        calLen = int(filecontent_list[15]) + int(filecontent_list[17])*256
        calLow = int(filecontent_list[25]) + int(filecontent_list[27])*256
        calHigh = int(filecontent_list[29]) + int(filecontent_list[31])*256
        calValue = float(calLen) / ( calHigh - calLow)
        
    if filecontent_list[1] == b'38':
        frequency = filecontent_list[7].replace(b'm',b'Min')
        channels = filecontent_list[9].split(b' ')
    channels = channels[1:-1]
    df_raw = pd.read_csv(dataIO, sep=',', names=channels)
    pdLastDate = pd.to_datetime(lastDate.decode(), dayfirst=True)
    timestamp = pd.date_range(end=pdLastDate, periods=len(df_raw), 
                          freq = frequency.decode())
    df_raw.index = timestamp    
    dataIO.close()
    df = pd.DataFrame()
    for column in df_raw.columns:
        value = sensorDict[logger.decode()]['sensors'][column.decode()]
        if value[1] == 'v':
            df[value] = [x+4095 if x < 0 else x for x in df_raw[column]]
            df[value] = (df[value] - zeroPoint) * calValue
        else:
            df[value] = df_raw[column]/10.                               

#            try:
#                df[value] = df_raw[column]/10.                               
#            except:
#                print('spalte', value, column, 'fehler')
#                for wert in df_raw[column]:
#                    try:
#                        int(wert)
#                    except:
#                        print('-'+wert+'-')
#    df['timestamp'] = timestamp    
    return df, logger

def dfToScanntronicDB(df, table, dbInput):
    dbfile = r'M:\Abteilung\_Mitarbeiter\Stapf\bruecke\scanntronicDaten.sqlite'
    cnx = sqlite3.connect(dbfile)
    df.to_sql(table, cnx, flavor='sqlite', if_exists='append', 
              index=True, index_label='timestamp')
#    index=False)
    cur = cnx.cursor()
    attachment, name, date, subject, emailID, logger = dbInput
    print(dbInput)
    sqlStr = "INSERT INTO checkedAttachments VALUES ("+str(int(emailID.decode()))+", '"+date+"', '"+subject+"', '"+name+"', '"+logger.decode()+"')"
    cur.execute(sqlStr)
    cnx.commit()
    cnx.close()

def dropDuplicates(table):
    dbfile = r'M:\Abteilung\_Mitarbeiter\Stapf\bruecke\scanntronicDaten.sqlite'
    cnx = sqlite3.connect(dbfile)
    cur = cnx.cursor()
    sqlStr = "delete from "+table+" where rowid not in (select min(rowid) from "+table+" group by timestamp)"
    cur.execute(sqlStr)
    cnx.commit()
    cnx.close()


def resetDB():
    dbfile = r'M:\Abteilung\_Mitarbeiter\Stapf\bruecke\scanntronicDaten.sqlite'
    cnx = sqlite3.connect(dbfile)
    cur = cnx.cursor()
    for key in sensorDict.keys():
        table = sensorDict[key]['name']
        sqlStr = "DROP TABLE "+table
        cur.execute(sqlStr)
    sqlStr = "DELETE FROM checkedAttachments"
    cur.execute(sqlStr)
    cnx.commit()
    cnx.close()

def updateDB():
    conn = connectToExchange()
    msg_id_list = getMessageID_list(conn)
    msg_id_list.reverse()
    dbfile = r'M:\Abteilung\_Mitarbeiter\Stapf\bruecke\scanntronicDaten.sqlite'
    cnx = sqlite3.connect(dbfile)
    sqlStr = "SELECT emailID FROM checkedAttachments"
    already_checked = pd.read_sql(sqlStr, cnx)
    existingMails = already_checked.emailID.values    
    cnx.close()
   
    for emailID in msg_id_list:
        if int(emailID) not in existingMails:
            for attachmentNr in [1, 2]:
                output = getMailAttachment(conn, emailID, attachmentNr)
                attachment, name, date, subject = output
                print(date, name, subject)
                if attachment:
                    df, logger = getDataFrameFromAttachment(attachment)
                    #print df[:5], logger
                    table = sensorDict[logger.decode()]['name']
                    print(table)
                    #df.to_json(r'm:\abteilung\_mitarbeiter\stapf\bruecke\test.json')
                    dbInput = output + (emailID, logger)                
                    dfToScanntronicDB(df, table, dbInput)
                    dropDuplicates(table)
                else:
                    print('No attachment in email ')
        else:
            print('Email Nr '+emailID.decode()+' wurde schon eingelesen')

if __name__ == '__main__':
    #resetDB()    
    #initTables(sensorDict)    
    updateDB()