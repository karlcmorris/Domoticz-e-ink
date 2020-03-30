#!/usr/bin/python3
try:
  import plotly.plotly as py
  import plotly.graph_objs as go
except ImportError:
  print ('Plotly ERROR')
import json
import requests
from requests.auth import HTTPBasicAuth
idx_total = '220'
idx_solar = '218'

# READING DOMOTICZ CALUES
urltotal ='http://XXXXXXXXXXXXX:XXXX/json.htm?type=graph&sensor=counter&idx=' + str(idx_total) + '&range=month&method=1'
urlsolar ='http://XXXXXXXXXXXXX:XXXX/json.htm?type=graph&sensor=counter&idx=' + str(idx_solar) + '&range=month&method=1'

jsontotal = requests.get(url=urltotal, auth=HTTPBasicAuth('USER', 'PASS'), timeout=5).json()
jsonsolar = requests.get(url=urlsolar, auth=HTTPBasicAuth('USER', 'PASS'), timeout=5).json()

hodnoty_total = jsontotal['result']
datumy_total = (', '.join(d['d'] for d in hodnoty_total))
datumy_total_l = [str(x) for x in datumy_total.split(',')]

hodnoty_total = (', '.join(d['v'] for d in hodnoty_total))
hodnoty_total_l = [str(x) for x in hodnoty_total.split(',')]

hodnoty_solar = jsonsolar['result']
datumy_solar = (', '.join(d['d'] for d in hodnoty_solar))
datumy_solar_l = [str(x) for x in datumy_solar.split(',')]

hodnoty_solar = (', '.join(d['v'] for d in hodnoty_solar))
hodnoty_solar_l = [str(x) for x in hodnoty_solar.split(',')]
hodnoty_solar_float = [float(i) for i in hodnoty_solar_l] # convert to float
hodnoty_total_float = [float(i) for i in hodnoty_total_l] # convert to float



def graf():
  layout = dict(title = 'Energy',
                paper_bgcolor='rgb(255,255,255)',
                plot_bgcolor='rgb(229,229,229)',
                xaxis = dict(
                               title = 'Months',showgrid=True,),
                yaxis = dict(title = 'Kwh',showgrid=True,rangemode='nonnegative'),
                legend=dict(x=0,y=1,bgcolor='rgb(229,229,229)'),
                barmode='stack'
                )
  trace0 = go.Bar(
      x = datumy_total_l,
      y = hodnoty_total_float,
      name = 'Energie celkem',
  )
  trace1 = go.Bar(
      x = datumy_solar_l,
      y = hodnoty_solar_float + hodnoty_total_float,
      name = 'Solar energy',
  )
  
  data = [trace0, trace1]
  fig = dict(data=data, layout=layout)
  py.plot(fig, filename='basic-line')

graf()