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

def plotlyUploadCSV(table, columns, title, ylabel, limits, file_name, 
                 use_columns=columns, secondary_y=[], start_date=[], 
                    filterMoist=False, online=False):
    df = pd.read_csv(table, na_values='error', sep='|',skiprows=[1,2], 
                     parse_dates=[[0,1]], index_col=[0], dayfirst=True)
    df.columns=columns
    dfAusreisser = df[]
    df = df.sort_index()
    df = df[use_columns]
    data = []
    print secondary_y
    for column in use_columns:
        #print column, start
        dfi = df#[df.index>start]
        trace = go.Scattergl(
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
        

columns = [str(i) for i in range(1,12)]
title = 'TDS-Sensoren'
ylabel = "counts"
file_name = 'TDSdaten'
limits = [5000,10000]
secondary_y = []
plotlyUploadCSV('M:\Abteilung\_Mitarbeiter\Stapf\TDS\logDateiTDS.txt', columns, title, ylabel, limits, file_name, 
             use_columns=columns, secondary_y=secondary_y, online=False)
