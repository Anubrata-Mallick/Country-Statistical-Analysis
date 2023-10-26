'''
Title: App 
Description: This is the main controll unit of the app which react according to circumstances 
'''

import numpy as np
import pandas as pd
import streamlit as st

import Routers

# Reading the data 
df = pd.read_csv('../Data/country_profile_variables.csv')
df.replace({'~0':np.nan, '-~0':np.nan, '~0.0':np.nan, '-~0.0':np.nan, '-99': np.nan, '-99.0':np.nan, '...':np.nan, '.../...':np.nan}, inplace=True)
df.dropna(inplace=True)

# Creating Side bar with radio buttons 
User_choice = st.sidebar.radio(
    #Theme
    'Select A Parameter to Analyze',
    #Options
    ('Overall Analysis', 'Regional Economy', 'Education & Technology')
)


#showing the analysis according to the User direction
if User_choice == 'Overall Analysis':
    Routers.Overall_Analysis_page(df)

if User_choice == 'Regional Economy':
    Routers.Regional_Economy_Page(df)

if User_choice == 'Education & Technology':
    Routers.Education_Technology_Page(df)