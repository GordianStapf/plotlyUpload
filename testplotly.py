# -*- coding: utf-8 -*-
"""
Created on Thu Jun 02 18:37:44 2016

@author: stapfg
"""

import plotly
plotly.tools.set_credentials_file(username='AbteilungHolz', api_key='m8d49p3n7w')
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import cufflinks as cf
import sqlite3
import matplotlib.pyplot as plt
import plotly.tools as tls


con = sqlite3.connect("C:\ProgramData\ForSens\Projekte\StuttgarterBruecke\Data\Data.db3")

#df = pd.read_sql_query("SELECT * from TBRissMini031506", con, index_col = 'TimeStep', parse_dates = ['TimeStep'])
df = pd.read_sql("SELECT * from TBRissMini031506", con, parse_dates = ['TimeStep'])
df.columns=['TimeStep','v_hor_unten','v_ver_haus','v_ver_weg','v_ver_oben_haus','v_ver_oben_weg']
#cf.set_config_file(offline=False, world_readable=True, theme='ggplot')
# verify that result of SQL query is stored in the dataframe
print(df.head())
con.close()
df = df.sort()
#trace1 = {'x':df.index, 'y':df.C03}
#trace2 = {'x':df.index, 'y':df.C04}
#data = [trace1, trace2]
#fig = go.Figure(data=data)
fig, ax = plt.subplots()

df.plot(ax=ax, x='TimeStep', legend=False)
#sc = plt.plot(df, label=df.columns)
ax.set_xlabel('')
ax.grid(color='w')
ax.set_title('Verschiebungen am integralen Stoss')
ax.set_ylabel('Verschiebung in mm')
ax.set_ylim(-.5,.5)
plotly_fig = tls.mpl_to_plotly(fig)
plotly_fig['layout']['plot_bgcolor'] = "rgb(213, 226, 233)"
plotly_fig['layout']['xaxis']['gridcolor'] = "white"
plotly_fig['layout']['yaxis']['gridcolor'] = "white"
plotly_fig['layout']['xaxis']['ticks'] = ""
plotly_fig['layout']['yaxis']['range'] = [-.5,.5]
plotly_fig['layout']['yaxis']['title'] = "Verschiebung in mm"
plotly_fig['layout']['autosize'] = True
plotly_fig['layout']['showlegend'] = True

#plotly.offline.plot_mpl(fig, filename='plotlytest35')
#plotly.offline.plot(plotly_fig)
py.plot(plotly_fig)
#trace = go.Scatter( x=df.index, y=df['C04'] )
#data = [trace]
#plot_url = py.plot_mpl(fig, filename='pd_mpl_plotly_test')
#plotly.offline.plot(data, filename='forSensTest35',      # name of the file as saved in your plotly account
#df.iplot(kind='scatter', filename='c:/etc/test')
#sharing='public'#for online plot
#)
