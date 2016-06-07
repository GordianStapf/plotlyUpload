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
import matplotlib.pyplot as plt
import plotly.tools as tls
import numpy as np

def plotlyUpload(table, columns, title, ylabel, limits, file_name, 
                 use_columns=columns, secondary_y=[], start_date=[], 
                    filterMoist=False, online=False):
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
                print df[:1]
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
    df = df[use_columns]
    data = []
    print secondary_y
    if secondary_y == []:
        for column, start in zip(use_columns, start_date):
#        for column in use_columns:
            print column, start
            dfi = df[df.index>start]
            trace = go.Scatter(
                x=dfi.index,
                y=dfi[column],
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
    else:
        primary_y = [i for i in use_columns if i not in secondary_y]
        for y in secondary_y:
            trace = go.Scatter(
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
            trace = go.Scatter(
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
        py.plot(fig, filename=file_name, fileopt='overwrite')
        
#columns = ['T_surf_oben','T_surf_unten',
#'u_seite_1cm','u_seite_6cm','u_seite_3cm',
#'u_unten_6cm','u_unten_20cm','u_unten_3cm','u_unten_10cm','u_unten_1cm']
#title = 'Holzfeuchten am Logger in Feldmitte'
#ylabel = "Holzfeuchte in %"
#file_name = 'HolzfeuchtenMitte'
#limits = [0,20]
#use_columns =  ['u_seite_1cm','u_seite_3cm','u_seite_6cm',
#'u_unten_1cm','u_unten_3cm','u_unten_6cm','u_unten_10cm','u_unten_20cm']
##secondary_y = ['T_unten','T_int_Stoss','T_oben']
#start_date = ['2016-05-30 20:30:00','2016-05-30 20:30:00','2016-05-30 20:30:00',
#              '2016-01-01 15:00:00','2016-01-01 15:00:00','2016-01-01 15:00:00',
#              '2016-01-01 15:00:00','2016-01-01 15:00:00']
#plotlyUpload('TBTU145295', columns, title, ylabel, limits, file_name, #mitte,id=1
#             use_columns=use_columns, start_date=start_date, 
#             filterMoist=False, online=True)
#
#columns = ['u_oben_3cm','u_oben_6cm','u_oben_1cm',
#'u_intStoss_20cm','u_intStoss_10cm','u_intStoss_30cm',
#'u_hirn_int_stoss','u_linearerSensor']
#title = 'Holzfeuchten am Logger beim integralen Stoss'
#ylabel = "Holzfeuchte in %"
#file_name = 'HolzfeuchtenIntStoss'
#limits = [0,20]
#use_columns =  ['u_oben_1cm','u_oben_3cm','u_oben_6cm',
#'u_intStoss_10cm','u_intStoss_20cm','u_intStoss_30cm',
#'u_hirn_int_stoss', 'u_linearerSensor']
#start_date = ['2016-06-01 15:00:00','2016-06-01 15:00:00','2016-06-01 15:00:00',
#              '2016-06-01 15:00:00','2016-06-01 15:00:00','2016-06-01 15:00:00',
#              '2016-06-01 15:00:00','2016-06-01 15:00:00']
##secondary_y = ['T_unten','T_int_Stoss','T_oben']
#tables = ['TBC00'+str(i).zfill(2) for i in range(17,25)]
#plotlyUpload(tables, columns, title, ylabel, limits, file_name, #intStoss,id=3
#             use_columns=use_columns, online=True, 
#             filterMoist=False, start_date=start_date)
#
#columns = ['v_hor_unten','v_ver_haus','v_ver_weg','v_hor_oben_haus','v_hor_oben_weg']
#title = 'Verschiebungen am integralen Stoss'
#ylabel = "Verschiebung in mm"
#file_name = 'verschiebungenIntegralerStoss'
#limits = [-.5,.5]
#use_columns = ['v_hor_unten','v_hor_oben_haus','v_hor_oben_weg','v_ver_haus','v_ver_weg']
#start_date = ['2016-05-09 15:00:00','2016-06-03 10:30:00','2016-06-03 10:30:00',
#              '2016-01-01 15:00:00','2016-01-01 15:00:00']
#plotlyUpload('TBRissMini031506', columns, title, ylabel, limits, file_name, 
#             use_columns=use_columns, secondary_y=[], start_date=start_date, online=True)

columns = ['v_hor_auflager','T_unten','rel_F_unten','T_int_Stoss','rel_F_int_Stoss','T_oben','rel_F_oben']
title = 'Klimadaten'
ylabel = "relative Feuche in %"
file_name = 'Klimadaten'
limits = []
use_columns = ['T_unten','T_int_Stoss','T_oben',
               'rel_F_unten','rel_F_int_Stoss','rel_F_oben']
secondary_y = ['T_unten','T_int_Stoss','T_oben']
plotlyUpload('TBRissMini031507', columns, title, ylabel, limits, file_name, 
             use_columns=use_columns, secondary_y=secondary_y, online=False)

columns = ['TimeStep','v_hor_auflager','T_unten','rel_F_unten','T_int_Stoss',
'rel_F_int_Stoss','T_oben','rel_F_oben']
title = 'Verschiebung Auflager'
ylabel = "Auflagerverschiebung in mm"
file_name = 'VerschiebungAuflager'
limits = []
use_columns = ['TimeStep','v_hor_auflager']
plotlyUpload('TBRissMini031507', columns, title, ylabel, limits, file_name, 
             use_columns=use_columns, online=False)

#columns = ['TimeStep','v_hor_unten','v_ver_haus','v_ver_weg','v_ver_oben_haus','v_ver_oben_weg']
#title = 'Verschiebungen am integralen Stoss'
#ylabel = "Verschiebung in mm"
#file_name = 'verschiebungenIntegralerStoss'
#limits = [-.5,.5]
#plotlyUpload('TBRissMini031506', columns, title, ylabel, limits, file_name, online=True)