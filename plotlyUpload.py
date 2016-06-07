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
                 use_columns=columns, online=False):
    con = sqlite3.connect(
    "C:\ProgramData\ForSens\Projekte\StuttgarterBruecke\Data\Data.db3")
    
    df = pd.read_sql("SELECT * from "+table, con, parse_dates = ['TimeStep'])
    df.columns=columns
    con.close()
    df = df.sort_index()
    df = df[use_columns]
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
    print dir(plotly_fig.layout)
    
    if online==False:
        plotly.offline.plot(plotly_fig, filename=file_name)
    if online==True:    
        py.plot(plotly_fig, filename=file_name, fileopt='overwrite')
        
#columns = ['TimeStep','v_hor_auflager','T_unten','rel_F_unten','T_int_Stoss','rel_F_int_Stoss','T_oben','rel_F_oben']
#title = 'Klimadaten'
#ylabel = "relative Feuche in %"
#file_name = 'Klimadaten'
#limits = []
#use_columns = ['TimeStep','T_unten','rel_F_unten','T_int_Stoss','rel_F_int_Stoss','T_oben','rel_F_oben']
#plotlyUpload('TBRissMini031507', columns, title, ylabel, limits, file_name, 
#             use_columns=use_columns, online=True)
#
#columns = ['TimeStep','v_hor_auflager','T_unten','rel_F_unten','T_int_Stoss','rel_F_int_Stoss','T_oben','rel_F_oben']
#title = 'Verschiebung Auflager'
#ylabel = "Auflagerverschiebung in mm"
#file_name = 'VerschiebungAuflager'
#limits = []
#use_columns = ['TimeStep','v_hor_auflager']
#plotlyUpload('TBRissMini031507', columns, title, ylabel, limits, file_name, use_columns=use_columns, online=True)

columns = ['TimeStep','v_hor_unten','v_ver_haus','v_ver_weg','v_hor_oben_haus','v_hor_oben_weg']
title = 'Verschiebungen am integralen Stoss'
ylabel = "Verschiebung in mm"
file_name = 'verschiebungenIntegralerStoss'
limits = [-.5,.5]
use_columns = ['TimeStep','v_hor_unten','v_hor_oben_haus','v_hor_oben_weg','v_ver_haus','v_ver_weg']
plotlyUpload('TBRissMini031506', columns, title, ylabel, limits, file_name, online=True)