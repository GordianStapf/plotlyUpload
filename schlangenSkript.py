# -*- coding: utf-8 -*-
# ME_Systems_V02.py by mowa::solutions
#
# Version 2.01 vom 07.06.2016
# Skript verbindet sich mit FTP-Server von ME
# und holt die Daten der beiden letzten Wochen
# in die ForSens-Datenbank
#
# 2Do:
# - ForSens-Datenbankschema für ME per Skript parametriert erzeugen
# - Interaktion mit der ForSens-GUI, wenn Sensornamen umbenannt werden
#
# Anmerkungen:
# - Das Skript kann bzgl. Oberflächenfeuchte angepasst werden
# -> Achtung: Hierzu müssen die ForSens-SQLite-Datenbankschemata angepasst werden
# - Um historische Daten zu übertragen, entsprechend der Variable datum ein
#   anderes Datum zuweisen

from datetime import date, timedelta
import pandas as pd
import sqlite3
import sys
import plotly
plotly.tools.set_credentials_file(username='AbteilungHolz', 
                                  api_key='m8d49p3n7w')
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import time

dbfile = "C:/bruecke/dmsDaten/dmsDaten.sqlite"
sensorenFTP = ['mpaBruecke','mpaBox2']
sensorenDB = ['dmsStangen','dmsHolz']
headerDB =[["date", 'N_u_haus','Q_u_weg','N_o_weg','Q_o_weg',
           'N_u_weg','Q_u_haus','N_o_haus','Q_o_haus'],
            ["date", 't_haus','t_weg','e_m_haus','e_m_weg',
           'e_q_haus','e_q_weg','e_q_oben','e_q_unten']]
#sensorenFTP = ['mpaBox2']
#sensorenDB = ['TBME002']
# Berechne das Anfangsdatum einer Kalenderwoche
def get_week_days(year, week):
    d = date(year,1,1)
    if(d.weekday()>3):
        d = d+timedelta(7-d.weekday())
    else:
        d = d - timedelta(d.weekday())
    dlt = timedelta(days = (week-1)*7)
    return d + dlt #,  d + dlt + timedelta(days=6)

def plotlyDownload(table, columns, filterMoist=False):
    con = sqlite3.connect(
        r"c:\bruecke\dmsDaten\dmsDaten.sqlite")

    df = pd.read_sql("SELECT * from "+table, con, parse_dates = ['date']
                        , index_col=['date'])
    if filterMoist == True:
        df = pd.rolling_mean(df, 30)
        df = df.where(df>10,np.nan)
        #df = df.where(df<30,np.nan)
    con.close()
    df.columns=columns
    df = df.sort_index()
    print df.index.max()
    print df.index.min()
    df = df[use_columns]
    df = df.where(df>-1000,np.nan)
    df = df.where(df<1000,np.nan)
    return df



def plotlyUpload(df, title, ylabel, limits, file_name, 
                 use_columns=[], start_date='2015-08-30 00:00:00', 
                    filterMoist=False, faktoren=[], online=False, 
                fileopt='overwrite'):

    data = []
    if type(start_date) == str:
        start_date = [start_date for i in use_columns]
    for column, start, faktor in zip(use_columns, start_date, faktoren):
#        for column in use_columns:
        dfi = df[df.index>start]
        dfj = dfi -dfi.iloc[0]
        dfj = dfj[::5]        
        trace = go.Scatter(
            x=dfj.index,
            y=dfj[column]*faktor,
            name=column,
            #yaxis='y2',
            #line = dict(
            #color = ('rgb(22, 96, 167)'),
            #width = 4,
            #dash = 'dash')
            )
        data.append(trace)    
    layout = go.Layout(
                title=title)
    fig = go.Figure(data=data, layout=layout)    
    fig['layout']['plot_bgcolor'] = "rgb(213, 226, 233)"
    fig['layout']['xaxis']['gridcolor'] = "white"
    fig['layout']['yaxis']['gridcolor'] = "white"
    fig['layout']['xaxis']['ticks'] = ""
    fig['layout']['yaxis']['range'] = limits
    fig['layout']['yaxis']['title'] = ylabel
    fig['layout']['autosize'] = True
    fig['layout']['showlegend'] = True
    
    if online==False:
        plotly.offline.plot(fig, filename=file_name)
    if online==True:    
        py.plot(fig, filename=file_name, fileopt=fileopt, autoopen=False)

    

<<<<<<< HEAD
#while 1:
# Bestimme Datumswerte, um die FTP-Verzeichnisse korrekt zu ermitteln
datum = date.today() # <- HIER KÖNNEN SIE EIN ANDERES DATUM EINSETZEN
week = datum.isocalendar()[1]
datumNeu = get_week_days(datum.year, week)

nweeks = 1
for i in range(0,nweeks):
    week = datum.isocalendar()[1]
    datumNeu = get_week_days(datum.year, week)
    #datum = datum - timedelta(days=7)
    
    # ************
    # Hole die Daten von ME-Box "mpaBruecke"
    # Dubletten werden von sqlite automatisch ignoriert
        
    for SensFTP, SensDB, header in zip(sensorenFTP,sensorenDB,headerDB):    
        folder = str(datumNeu.year) + "/" + str(datumNeu.month).zfill(2) + "/week" + str(week).zfill(2) + "/"
        fname = SensFTP + "-week" + str(week).zfill(2) + ".txt"
        
        # Daten aus der Vorwoche
        try:
            if SensFTP == 'mpaBruecke':        
                strftp = "ftp://stapfg1:wipogexe@ftp.smartgage.net/" + folder + fname
            if SensFTP == 'mpaBox2':        
                strftp = "ftp://stapfg:wipogexe@ftp.smartgage.net/" + folder + fname
            else:
                'sensor', SensFTP, 'nicht vorhanden'
            print strftp
            pf1 = pd.read_csv(strftp, delimiter=";", decimal=',', 
                parse_dates = [0], infer_datetime_format=True, 
                skiprows=2, header=None, dayfirst=True,
                names = header)
            pf1.index.names = ['rowid']
            dbfile = "C:/bruecke/dmsDaten/dmsDaten.sqlite"
            cnx = sqlite3.connect(dbfile)
            pf1.to_sql(SensDB, cnx, flavor='sqlite', if_exists='append', index=False)
            cnx.close()
        except:
            print ("Datei " + folder + fname + " auf FTP-Server "+SensFTP+" nicht vorhanden")
            print sys.exc_info()


columns = ['t_haus','t_weg','e_m_haus','e_m_weg',
           'e_q_haus','e_q_weg','e_q_oben','e_q_unten']
title = 'Dehnungen im Holzquerschnitt beim integralen Stoss'
ylabel = "Dehnung in Promille"
file_name = 'DehnungenHolzaktuell'
limits = [-.1,.1]
use_columns = columns
start_date = '2016-06-08 18:00:00'
faktor = [1, 1, 0.5, 0.5, 2, 2, 2, 2]
df = plotlyDownload('dmsHolz', columns)
plotlyUpload(df, title, ylabel, limits, file_name, 
         use_columns=use_columns, start_date = start_date, 
         faktoren=faktor, online=True, 
            fileopt='overwrite')
            
columns = ['N_u_haus','Q_u_weg','N_o_weg','Q_o_weg',
       'N_u_weg','Q_u_haus','N_o_haus','Q_o_haus']
title = 'Kraft in Stangen'
ylabel = "Kraft in kN"
file_name = 'StangenKraftaktuell'
limits = [-5.,5.]
use_columns = ['N_u_haus','N_u_weg','N_o_haus','N_o_weg',
               'Q_u_haus','Q_u_weg','Q_o_haus','Q_o_weg']
start_date = '2016-06-08 18:00:00'
faktor = [26.89, 26.89, 26.89, 26.89, -26.89, -26.89, 26.89, -26.89]
df = plotlyDownload('dmsStangen', columns)
plotlyUpload(df, title, ylabel, limits, file_name, 
             use_columns=use_columns, start_date=start_date,
             faktoren=faktor, online=True)


            
=======
while 1:
    # Bestimme Datumswerte, um die FTP-Verzeichnisse korrekt zu ermitteln
    datum = date.today() # <- HIER KÖNNEN SIE EIN ANDERES DATUM EINSETZEN
    week = datum.isocalendar()[1]
    datumNeu = get_week_days(datum.year, week)
    
    nweeks = 1
    for i in range(0,nweeks):
        week = datum.isocalendar()[1]
        datumNeu = get_week_days(datum.year, week)
        #datum = datum - timedelta(days=7)
        
        # ************
        # Hole die Daten von ME-Box "mpaBruecke"
        # Dubletten werden von sqlite automatisch ignoriert
            
        for SensFTP, SensDB, header in zip(sensorenFTP,sensorenDB,headerDB):    
            folder = str(datumNeu.year) + "/" + str(datumNeu.month).zfill(2) + "/week" + str(week).zfill(2) + "/"
            fname = SensFTP + "-week" + str(week).zfill(2) + ".txt"
            
            # Daten aus der Vorwoche
            try:
                if SensFTP == 'mpaBruecke':        
                    strftp = "ftp://stapfg1:wipogexe@ftp.smartgage.net/" + folder + fname
                if SensFTP == 'mpaBox2':        
                    strftp = "ftp://stapfg:wipogexe@ftp.smartgage.net/" + folder + fname
                else:
                    'sensor', SensFTP, 'nicht vorhanden'
                print strftp
                pf1 = pd.read_csv(strftp, delimiter=";", decimal=',', 
                    parse_dates = [0], infer_datetime_format=True, 
                    skiprows=2, header=None, dayfirst=True,
                    names = header)
                pf1.index.names = ['rowid']
                dbfile = "C:/bruecke/dmsDaten/dmsDaten.sqlite"
                cnx = sqlite3.connect(dbfile)
                pf1.to_sql(SensDB, cnx, flavor='sqlite', if_exists='append', index=False)
                cnx.close()
            except:
                print ("Datei " + folder + fname + " auf FTP-Server "+SensFTP+" nicht vorhanden")
                print sys.exc_info()


    columns = ['t_haus','t_weg','e_m_haus','e_m_weg',
               'e_q_haus','e_q_weg','e_q_oben','e_q_unten']
    title = 'Dehnungen im Holzquerschnitt beim integralen Stoss'
    ylabel = "Dehnung in Promille"
    file_name = 'DehnungenHolzaktuell'
    limits = [-.1,.1]
    use_columns = columns
    start_date = '2016-06-08 18:00:00'
    faktor = [1, 1, 0.5, 0.5, 2, 2, 2, 2]
    df = plotlyDownload('dmsHolz', columns)
    plotlyUpload(df, title, ylabel, limits, file_name, 
             use_columns=use_columns, start_date = start_date, 
             faktoren=faktor, online=True, 
                fileopt='overwrite')
                
    columns = ['N_u_haus','Q_u_weg','N_o_weg','Q_o_weg',
           'N_u_weg','Q_u_haus','N_o_haus','Q_o_haus']
    title = 'Kraft in Stangen'
    ylabel = "Kraft in kN"
    file_name = 'StangenKraftaktuell'
    limits = []
    use_columns = ['N_u_haus','N_u_weg','N_o_haus','N_o_weg',
                   'Q_u_haus','Q_u_weg','Q_o_haus','Q_o_weg']
    start_date = '2016-06-08 18:00:00'
    faktor = [26.89, 26.89, 26.89, 26.89, -26.89, -26.89, 26.89, -26.89]
    df = plotlyDownload('dmsStangen', columns)
    plotlyUpload(df, title, ylabel, limits, file_name, 
                 use_columns=use_columns, start_date=start_date,
                 faktoren=faktor, online=True)
    time.sleep(3600)
    


                
>>>>>>> 9807098f9512b6009abb956586b5410ab0ae4aef

