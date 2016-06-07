# -*- coding: utf-8 -*-
"""
Created on Mon Jun 06 17:32:23 2016

@author: stapfg
"""

import numpy as np 
import plotly.plotly as py  
import plotly.tools as tls   
import plotly.graph_objs as go

stream_id = 'fr7zjj3bhz'
# Make instance of stream id object 
stream_1 = go.Stream(
    token= stream_id,# link stream id to 'token' key
    maxpoints=80      # keep a max of 80 pts on screen
)

# Initialize trace of streaming plot by embedding the unique stream_id
trace1 = go.Scatter(
    x=[],
    y=[],
    mode='lines+markers',
    stream=stream_1         # (!) embed stream id, 1 per trace
)

data = go.Data([trace1])

# Add title to layout object
layout = go.Layout(title='TDS count Stream')

# Make a figure object
fig = go.Figure(data=data, layout=layout)

# Send fig to Plotly, initialize streaming plot, open new tab
py.plot(fig, filename='TDS-streaming')

# We will provide the stream link object the same token that's associated with the trace we wish to stream to
s = py.Stream(stream_id)

# We then open a connection
s.open()

fh = open('C:\TDS\logDateiTDS.txt', 'rb')
for line in fh:
    pass
last = line
lastStripped = last.strip()
last[]