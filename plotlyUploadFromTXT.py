# -*- coding: utf-8 -*-
"""
Created on Thu Jun 02 18:37:44 2016

@author: stapfg
"""

import plotly
plotly.tools.set_credentials_file(username='AbteilungHolz',
                                  api_key='m8d49p3n7w')
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from schlangenSkript import dfFromOwnDB
from plotlyUploadFromMultibleTables import plotlyUpload
from warningMail import sendWarningMail


def dbFromCSV(dbfile, table, columns):
    df = pd.read_csv(table, na_values='error', sep='|',skiprows=[1,2],
                     parse_dates=[[0,1]], #index_col=[0], 
                     dayfirst=True)
    df.columns=columns
    cnx = sqlite3.connect(dbfile)
    df.to_sql('TDScounts', cnx, flavor='sqlite', if_exists='append', index=False)
    cur = cnx.cursor()
    table = 'TDScounts'
    sqlStr = "delete from "+table+" where rowid not in (select min(rowid) from "+table+" group by date)"
    cur.execute(sqlStr)
    cnx.commit()
    cnx.close()

if __name__ == '__main__':
    columns = ['sensor'+str(i) for i in range(1,12)]
    csvFile = r'M:/Abteilung/_Projekte/Forschung/Stuttgarter_Bruecke_Monitoring/TDS/logDateiTDS.txt'
    dbfile = r'M:/Abteilung/_Projekte/Forschung/Stuttgarter_Bruecke_Monitoring/TDS/logTDS.sqlite'
    dbFromCSV(dbfile, csvFile, ['date']+columns)
    table = 'TDScounts'
    df = dfFromOwnDB(dbfile, table, columns)
    df = df[0:-1:100]
    title = 'TDS-Sensoren'
    ylabel = "counts"
    file_name = 'TDSdaten'
    limits = [8500,9500]
    secondary_y = []
    plotlyUpload(df, title, ylabel, limits, file_name, 
                 use_columns=columns, secondary_y=[], start_date='2015-08-30 00:00:00', 
                    filterMoist=False, online=True, gl=True)
    sendWarningMail(text='Skript wurde erfolgreich ausgeführt', 
                subject = 'TDS-Daten wurden aktualisiert')