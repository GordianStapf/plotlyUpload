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

def plotlyUpload(table, columns, title, ylabel, limits, file_name, 
                 use_columns=columns, secondary_y=[], online=False):
    con = sqlite3.connect(
    "C:\ProgramData\ForSens\Projekte\StuttgarterBruecke\Data\Data.db3")
    
    df = pd.read_sql("SELECT * from "+table, con, parse_dates = ['TimeStep']
                        , index_col=['TimeStep'])
    df.columns=columns
    con.close()
    df = df.sort_index()
    df = df[use_columns]
    data = []
    if secondary_y == []:
        for y in use_columns:
                    trace = go.Scatter(
                        x=df.index,
                        y=df[y],
                        name=y,
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
#plotlyUpload('TBTU145295', columns, title, ylabel, limits, file_name, #mitte,id=1
#             use_columns=use_columns, online=True)

columns = ['T_stangen','T_intStoss_oben',
'u_hirn_int_stoss',
'u_oben_1cm','u_oben_6cm','u_oben_3cm',
'u_linearerSensor',
'u_intStoss_20cm','u_intStoss_10cm','u_intStoss_30cm']
title = 'Holzfeuchten am Logger beim integralen Stoss'
ylabel = "Holzfeuchte in %"
file_name = 'HolzfeuchtenIntStoss'
limits = [0,20]
use_columns =  ['u_oben_1cm','u_oben_3cm','u_oben_6cm',
'u_intStoss_10cm','u_intStoss_20cm','u_intStoss_30cm',
'u_linearerSensor','u_hirn_int_stoss',]
#secondary_y = ['T_unten','T_int_Stoss','T_oben']
plotlyUpload('TBTU145296', columns, title, ylabel, limits, file_name, #intStoss,id=3
             use_columns=use_columns, online=True)

#columns = ['v_hor_auflager','T_unten','rel_F_unten','T_int_Stoss','rel_F_int_Stoss','T_oben','rel_F_oben']
#title = 'Klimadaten'
#ylabel = "relative Feuche in %"
#file_name = 'Klimadaten'
#limits = []
#use_columns = ['T_unten','rel_F_unten','T_int_Stoss','rel_F_int_Stoss','T_oben','rel_F_oben']
#secondary_y = ['T_unten','T_int_Stoss','T_oben']
#plotlyUpload('TBRissMini031507', columns, title, ylabel, limits, file_name, 
#             use_columns=use_columns, secondary_y=secondary_y, online=True)

#columns = ['TimeStep','v_hor_auflager','T_unten','rel_F_unten','T_int_Stoss','rel_F_int_Stoss','T_oben','rel_F_oben']
#title = 'Verschiebung Auflager'
#ylabel = "Auflagerverschiebung in mm"
#file_name = 'VerschiebungAuflager'
#limits = []
#use_columns = ['TimeStep','v_hor_auflager']
#plotlyUpload('TBRissMini031507', columns, title, ylabel, limits, file_name, use_columns=use_columns, online=True)

#columns = ['TimeStep','v_hor_unten','v_ver_haus','v_ver_weg','v_ver_oben_haus','v_ver_oben_weg']
#title = 'Verschiebungen am integralen Stoss'
#ylabel = "Verschiebung in mm"
#file_name = 'verschiebungenIntegralerStoss'
#limits = [-.5,.5]
#plotlyUpload('TBRissMini031506', columns, title, ylabel, limits, file_name, online=True)