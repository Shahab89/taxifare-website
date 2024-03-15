import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import requests
import folium
from streamlit_folium import folium_static
import osm2geojson
import polyline
'''
# Welcome to taxifare prediction
'''
col1, col2,col3 = st.columns(3)
with col1:
    pickup_date = st.date_input("Select your pickup date")
    pickup_time = st.time_input('Select your pickup time')
with col2:
    pickup_longitude = st.number_input('Your pickup longitude')   # -73.950655
    pickup_latitude = st.number_input('Your pickup latitude')  # 40.783282
with col3:
    dropoff_longitude = st.number_input('Your dropoff longitude') # -73.984365
    dropoff_latitude = st.number_input('Your dropoff latitude') # 40.769802
passenger_count = st.slider('Select number of passenger', 1, 8, 2)


pickup_datetime = datetime.combine(pickup_date, pickup_time)


url = 'https://taxifare-tyv7xwh6tq-ew.a.run.app/predict'
#url = 'https://taxifare.lewagon.ai/predict'
inputs = {
        'pickup_datetime' : pd.Timestamp(pickup_datetime, tz='UTC'),
        'pickup_longitude' :  pickup_longitude,
        'pickup_latitude' : pickup_latitude,
        'dropoff_longitude' : dropoff_longitude,
        'dropoff_latitude' : dropoff_latitude,
        'passenger_count': passenger_count
}

df = pd.DataFrame([inputs])

response = requests.get(url, params = inputs )
response_json = response.json()['fare_amount']

if st.button('predict the taxi fare', use_container_width = True) and df.shape == (1,6) :
    # print is visible in the server output, not in the page
    st.write('**_The taxi fare prediction is:_**')
    #st.write(f'{round(response_json,2)}$', unsafe_allow_html=True)
    st.write(f"""
    <div style="padding: 10px; background-color: #3498db; color: white; border-radius: 5px; font-size: 20px; width: fit-content;">
        {round(response_json, 2)}$
    </div>
    """, unsafe_allow_html=True)
else:
    st.write('**_The taxi fare prediction is:_**')
    #st.write(f'{round(response_json,2)}$', unsafe_allow_html=True)
    st.write(f"""
    <div style="padding: 10px; background-color: #3498db; color: white; border-radius: 5px; font-size: 20px; width: fit-content;">
        {round(0, 2)}$
    </div>
    """, unsafe_allow_html=True)
    st.write('please fillout all required!')




# Create map object
m = folium.Map(location=[pickup_latitude, pickup_longitude], zoom_start=10)

# Add pickup marker
folium.Marker(
    location=[pickup_latitude, pickup_longitude],
    popup='Pickup Location',
    draggable = True,
    icon=folium.Icon(color='blue')
).add_to(m)

# Add dropoff marker
folium.Marker(
    location=[dropoff_latitude, dropoff_longitude],

    popup='Dropoff Location',
    draggable = True,
    icon=folium.Icon(color='red')
).add_to(m)

# Add directional line
# folium.PolyLine(
#     locations=[[pickup_latitude, pickup_longitude], [dropoff_latitude, dropoff_longitude]],
#     color='green',
#     weight=5,
#     tooltip='Route'
# ).add_to(m)

# Display map
folium_static(m)
