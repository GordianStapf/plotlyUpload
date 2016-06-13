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

def plotlyUpload(table, columns, title, ylabel, limits, file_name, 
                 use_columns=[], start_date='2015-08-30 00:00:00', 
                    filterMoist=False, faktoren=[], online=False, 
                fileopt='extend'):
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


    data = []
    if type(start_date) == str:
        start_date = [start_date for i in use_columns]
    for column, start, faktor in zip(use_columns, start_date, faktoren):
        dfi = df[df.index>start]
        dfj = dfi -dfi.iloc[0]
        trace = go.Scatter(
            x=dfj.index,
            y=dfj[column]*faktor*26.89981366,
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
        py.plot(fig, filename=file_name, fileopt='overwrite')
        

columns = ['N_u_haus','Q_u_weg','N_o_weg','Q_o_weg',
           'N_u_weg','Q_u_haus','N_o_haus','Q_o_haus']
title = 'Kraft in Stangen'
ylabel = "Kraft in kN"
file_name = 'StangenKraft'
limits = [-5, 5]
use_columns = ['N_u_haus','N_u_weg','N_o_haus','N_o_weg',
               'Q_u_haus','Q_u_weg','Q_o_haus','Q_o_weg']
start_date = '2016-05-23 00:00:00'
faktor = [1, 1, 1, 1, -1, -1, 1, -1]
plotlyUpload('dmsStangen', columns, title, ylabel, limits, file_name, 
             use_columns=use_columns, start_date=start_date,
             faktoren=faktor, online=False)

