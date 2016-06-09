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
        print column, start
        dfi = df[df.index>start]
        dfj = dfi# -dfi.iloc[0]
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
        py.plot(fig, filename=file_name, fileopt=fileopt)
        

columns = ['t_haus','t_weg','e_m_haus','e_m_weg',
           'e_q_haus','e_q_weg','e_q_oben','e_q_unten']
title = 'Dehnungen im Holzquerschnitt beim integralen Stoss'
ylabel = "Dehnung in Promille"
file_name = 'DehnungenHolz'
limits = []
use_columns = columns
start_date = '2016-05-29 00:00:00'
faktor = [1, 1, 0.5, 0.5, 2, 2, 2, 2]
df = plotlyDownload('dmsHolz', columns)
plotlyUpload(df, title, ylabel, limits, file_name, 
             use_columns=use_columns, start_date = start_date, 
             faktoren=faktor, online=True, 
                fileopt='overwrite')

