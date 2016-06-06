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
    if secondary_y == []:
        df.plot(x='TimeStep', legend=False)
    else:
        primary_y = [i for i in use_columns if i not in secondary_y]
        data = []        
        for y in secondary_y:
            trace = go.Scatter(
                x=df.index,
                y=df[y],
                name=y,
                yaxis='y2'
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
        
columns = ['v_hor_auflager','T_unten','rel_F_unten','T_int_Stoss','rel_F_int_Stoss','T_oben','rel_F_oben']
title = 'Klimadaten'
ylabel = "relative Feuche in %"
file_name = 'Klimadaten'
limits = []
use_columns = ['T_unten','rel_F_unten','T_int_Stoss','rel_F_int_Stoss','T_oben','rel_F_oben']
secondary_y = ['T_unten','T_int_Stoss','T_oben']
plotlyUpload('TBRissMini031507', columns, title, ylabel, limits, file_name, 
             use_columns=use_columns, secondary_y=secondary_y, online=True)

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