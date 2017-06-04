#!/usr/bin/env python
# coding: utf-8

import folium
import pandas as pd

state_geo = r'data_file/china.geo.json'
state_music_comments = r'data_file/user_locate.csv'

state_data = pd.read_csv(state_music_comments)

map = folium.Map(location=[33, 108], zoom_start=4)
map.choropleth(geo_path=state_geo, data=state_data,
	columns=['State', 'Comment'],
	key_on='feature.id',
	fill_color='YlGn', fill_opacity=0.7, line_opacity=0.2,
	legend_name='Comment Rate (%)')
map.save(r'data_file/html.html')
