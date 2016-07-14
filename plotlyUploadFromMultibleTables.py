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
import numpy as np
import scanntronicTools as sT
from warningMail import sendWarningMail

def dfFromForSens(table, columns, filterMoist=False):
    con = sqlite3.connect(
    "C:\ProgramData\ForSens\Projekte\StuttgarterBruecke\Data\Data.db3")
    df = []    
    if type(table)==list:
        for tab, column in zip(table, columns):        
            if len(df)==0:
                df = pd.read_sql("SELECT * from "+tab, con, parse_dates = ['TimeStep']
                            , index_col=['TimeStep'])
            else:
                df.loc[:,column] = pd.read_sql("SELECT * from "+tab, con, parse_dates = ['TimeStep']
                            , index_col=['TimeStep'])
    else:
        df = pd.read_sql("SELECT * from "+table, con, parse_dates = ['TimeStep']
                        , index_col=['TimeStep'])

    if filterMoist == True:
        df = pd.rolling_mean(df, 30)
        df = df.where(df>10,np.nan)
        #df = df.where(df<30,np.nan)
    con.close()
    df.columns=columns
    df = df.sort_index()
    return df

def plotlyUpload(df, title, ylabel, limits, file_name, 
                 use_columns=[], secondary_y=[], start_date='2015-08-30 00:00:00', 
                    filterMoist=False, online=False, gl=False, 
                    auto_open=False):
    df = df[use_columns]
    data = []
    if gl==False:
        scatterLoc = go.Scatter
    if gl==True:
        scatterLoc = go.Scattergl
    if type(start_date) == str:
        start_date = [start_date for i in use_columns]
    if secondary_y == []:
        for column, start in zip(use_columns, start_date):
            dfi = df[df.index>start]
            trace = scatterLoc(
                x=dfi.index,
                y=dfi[column],
                name=column,
                )
            data.append(trace)    
        layout = go.Layout(
                    title=title)
    else:
        primary_y = [i for i in use_columns if i not in secondary_y]
        for y in secondary_y:
            trace = scatterLoc(
                x=df.index,
                y=df[y],
                name=y,
                yaxis='y2',
                line = dict(
                #color = ('rgb(22, 96, 167)'),
                #width = 4,
                dash = 'dash')
                )
            data.append(trace)
        for y in primary_y:
            trace = scatterLoc(
                x=df.index,
                y=df[y],
                name=y,
                yaxis='y'
                )
            data.append(trace)
            ylabel2='Temperatur in &deg;Celsius'
            layout = go.Layout(
                    title=title,
                    xaxis=dict(
                                domain=[0.1, 0.95]#damit die rechte y-Achse nicht unter der Legende liegt
                                ),
                    yaxis=dict(
                                title=ylabel
                    ),
                    yaxis2=dict(
                        title=ylabel2,
                        titlefont=dict(
                            color='rgb(148, 103, 189)'
                        ),
                        tickfont=dict(
                            color='rgb(148, 103, 189)'
                        ),
                        overlaying='y',
                        side='right'
                    )
                )
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
        py.plot(fig, filename=file_name, fileopt='overwrite',
                auto_open=auto_open)
                
def holzfeuchteAusWiderstand(widerstand, abstand_elektroden=3.):
    from numpy import log
    spezifischer_widerstand = widerstand / abstand_elektroden
    holzfeuchte = (13.25 - log(spezifischer_widerstand))/0.32
    return holzfeuchte


if __name__ == '__main__':    
    sT.updateDB()
    sT.R2u_intStoss()

    online = True    
    auto_open = False    
            
    columns = ['T_surf_oben','T_surf_unten',
    'u_seite_1cm','u_seite_6cm','u_seite_3cm',
    'u_unten_6cm','u_unten_20cm','u_unten_3cm','u_unten_10cm','u_unten_1cm']
    title = 'Holzfeuchten am Logger in Feldmitte'
    ylabel = "Holzfeuchte in %"
    file_name = 'HolzfeuchtenMitte'
    limits = [0,20]
    use_columns =  ['u_haus_1cm','u_haus_3cm','u_haus_6cm',
    'u_unten_1cm','u_unten_3cm','u_unten_6cm','u_unten_10cm','u_unten_20cm']
    #secondary_y = ['T_unten','T_int_Stoss','T_oben']
    start_date = ['2016-05-31 15:00:00', '2016-05-31 15:00:00', '2016-05-31 15:00:00', 
                  '2016-03-23 15:00:00', '2016-03-23 15:00:00', '2016-03-23 15:00:00', 
                  '2016-03-23 15:00:00', '2016-03-23 15:00:00', '2016-03-23 15:00:00']
    table = 'HygrofoxMitte'
    df = sT.dfFromScanntronicDB(table)
    df = df.where(df>3,np.nan)
    plotlyUpload(df, title, ylabel, limits, file_name, #mitte,id=1
                 use_columns=use_columns, start_date=start_date, 
                 filterMoist=False, online=online, auto_open=auto_open)
    
    columns = ['u_oben_3cm','u_oben_6cm','u_oben_1cm',
    'u_intStoss_20cm','u_intStoss_10cm','u_intStoss_30cm',
    'u_hirn_int_stoss','u_linearerSensor']
    columns = ['T_oben','T_stangen','u_intStoss_hirn','u_oben_1cm',
    'u_oben_6cm','u_oben_3cm','u_linearerSensor',
    'u_intStoss_20cm','u_intStoss_10cm','u_intStoss_30cm']
    title = 'Holzfeuchten am Logger beim integralen Stoss'
    ylabel = "Holzfeuchte in %"
    file_name = 'HolzfeuchtenIntStoss'
    limits = [0,20]
    use_columns =  ['u_oben_intStoss_1cm','u_oben_intStoss_3cm','u_oben_intStoss_6cm',
    'u_unten_intStoss_10cm','u_unten_intStoss_20cm','u_unten_intStoss_30cm',
    'u_intStoss_stirn', 'u_linear']
    start_date = ['2016-06-01 15:00:00','2016-06-01 15:00:00','2016-06-01 15:00:00',
                  '2016-06-01 15:00:00','2016-06-01 15:00:00','2016-06-01 15:00:00',
                  '2016-06-01 15:00:00','2016-06-01 15:00:00']
    #secondary_y = ['T_unten','T_int_Stoss','T_oben']
    table = 'HygrofoxIntegralerStoss_u'
    df = sT.dfFromScanntronicDB(table)
    plotlyUpload(df, title, ylabel, limits, file_name, #intStoss,id=3
                 use_columns=use_columns, online=online, 
                 filterMoist=False, start_date=start_date)
    
    columns = ['v_hor_unten','v_ver_haus','v_ver_weg','v_hor_oben_haus','v_hor_oben_weg']
    title = 'Verschiebungen am integralen Stoss'
    ylabel = "Verschiebung in mm"
    file_name = 'verschiebungenIntegralerStoss'
    limits = [-.5,.5]
    use_columns = ['v_hor_unten','v_hor_oben_haus','v_hor_oben_weg','v_ver_haus','v_ver_weg']
    start_date = '2016-03-30 15:00:00'
    table = 'RissFoxIntegralerStoss'              
    df = sT.dfFromScanntronicDB(table)
    df.sort_index()
    plotlyUpload(df, title, ylabel, limits, file_name, 
                 use_columns=use_columns, secondary_y=[], 
                    start_date=start_date, online=online, auto_open=auto_open)
    
    columns = ['v_hor_auflager','T_unten','rel_F_unten','T_int_Stoss','rel_F_int_Stoss','T_oben','rel_F_oben']
    title = 'Klimadaten'
    ylabel = "relative Feuche in %"
    file_name = 'Klimadaten'
    limits = []
    use_columns = ['t_unten_mitte','t_intStoss_oben','t_oben_mitte',
                   'rF_unten_mitte','rF_intStoss_oben','rF_oben_mitte']
    secondary_y = ['t_unten_mitte','t_intStoss_oben','t_oben_mitte']
    table = 'RissFoxMitte'
    df = sT.dfFromScanntronicDB(table)
    df = df.where(df>3,np.nan)
    plotlyUpload(df, title, ylabel, limits, file_name, 
                 use_columns=use_columns, secondary_y=secondary_y, online=online)
    
    columns = ['v_hor_auflager','T_unten','rel_F_unten','T_int_Stoss',
    'rel_F_int_Stoss','T_oben','rel_F_oben']
    title = 'Verschiebung Auflager'
    ylabel = "Auflagerverschiebung in mm"
    file_name = 'VerschiebungAuflager'
    limits = []
    use_columns = ['v_hor_auflager']
    table = 'RissFoxMitte'
    df = sT.dfFromScanntronicDB(table)
    plotlyUpload(df, title, ylabel, limits, file_name, 
                 use_columns=use_columns, start_date='2016-03-30 00:00:00',
                 online=online)
    
    sendWarningMail(text='Skript wurde erfolgreich ausgeführt', 
                    subject = 'ScanntronicDaten wurden aktualisiert')