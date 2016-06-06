# -*- coding: utf-8 -*-
"""
Created on Thu Jun 02 18:37:46 2016

@author: stapfg
"""

import plotly
plotly.tools.set_credentials_file(username='AbteilungHolz', api_key='m8d49p3n7w')
import plotly.plotly as py
import matplotlib.pyplot as plt
import plotly.tools as tls
import matplotlib.image as mpimg

img=mpimg.imread('c:\etc\Querschnitt_integraler_Stoss.jpg')
fig, ax = plt.subplots()
ax.imshow(img)
#ax.plot([1,2],[1,2])
plotly_fig = tls.mpl_to_plotly(fig)
plotly.offline.plot(plotly_fig)
#py.plot(plotly_fig)
