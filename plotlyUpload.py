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

def plotlyUpload(table, columns, title, ylabel, limits, file_name, online=False):
    con = sqlite3.connect(
    "C:\ProgramData\ForSens\Projekte\StuttgarterBruecke\Data\Data.db3")
    
    df = pd.read_sql("SELECT * from "+table, con, parse_dates = ['TimeStep'])
    df.columns=columns
    con.close()
    df = df.sort_index()
    fig, ax = plt.subplots()
    
    df.plot(ax=ax, x='TimeStep', legend=False)
    ax.set_xlabel('')
    ax.set_title(title)
    ax.set_ylim(-.5,.5)
    plotly_fig = tls.mpl_to_plotly(fig)
    plotly_fig['layout']['plot_bgcolor'] = "rgb(213, 226, 233)"
    plotly_fig['layout']['xaxis']['gridcolor'] = "white"
    plotly_fig['layout']['yaxis']['gridcolor'] = "white"
    plotly_fig['layout']['xaxis']['ticks'] = ""
    plotly_fig['layout']['yaxis']['range'] = limits
    plotly_fig['layout']['yaxis']['title'] = ylabel
    plotly_fig['layout']['autosize'] = True
    plotly_fig['layout']['showlegend'] = True
    
    if online==False:
        plotly.offline.plot(plotly_fig, filename=file_name)
    if online==True:    
        py.plot(plotly_fig, filename=file_name, fileopt='overwrite')
        
columns = ['TimeStep','v_hor_unten','v_ver_haus','v_ver_weg','v_ver_oben_haus','v_ver_oben_weg']
title = 'Verschiebungen am integralen Stoss'
ylabel = "Verschiebung in mm"
file_name = 'verschiebungenIntegralerStoss'
limits = [-.5,.5]
plotlyUpload('TBRissMini031506', columns, title, ylabel, limits, file_name, online=True)

#columns = ['TimeStep','v_hor_unten','v_ver_haus','v_ver_weg','v_ver_oben_haus','v_ver_oben_weg']
#title = 'Verschiebungen am integralen Stoss'
#ylabel = "Verschiebung in mm"
#file_name = 'verschiebungenIntegralerStoss'
#limits = [-.5,.5]
#plotlyUpload('TBRissMini031506', columns, title, ylabel, limits, file_name, online=True)