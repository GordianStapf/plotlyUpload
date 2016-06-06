# -*- coding: utf-8 -*-
"""
Created on Sun Jun 05 17:25:20 2016

@author: stapfg
"""

#import plotly.plotly as py


import requests, json

dashboard_json = {
    "rows": [
#    [{"plot_url": graph_url1}, {"plot_url": graph_url2}],
    [{"plot_url": 'https://plot.ly/~AbteilungHolz/49/verschiebungen-am-integralen-stoss/'}]
    ],
    "banner": {
        "visible": True,
        "backgroundcolor": "#3d4a57",
        "textcolor": "white",
        "title": "Verschiebungen am integralen Stoss",
        "links": []
    },
    "requireauth": False,
    "auth": {
        "username": "AbteilungHolz",
        "passphrase": "holzkonstruktionen"
    }
}

response = requests.post('https://dashboards.ly/publish',
data={'dashboard': json.dumps(dashboard_json)},
headers={'content-type': 'application/x-www-form-urlencoded'})

response.raise_for_status()

dashboard_url = response.json()['url']
print('dashboard url: https://dashboards.ly{}'.format(dashboard_url))
# View here: https://dashboards.ly/ua-vNxpsNCb9aYTzb2Q64ZDUa
