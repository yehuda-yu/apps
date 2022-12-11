# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 17:25:48 2022

@author: User
"""
import numpy as np
import streamlit as st
import pandas as pd
from xgboost import XGBRegressor
import seaborn as sns
sns.set_theme(style="white",font_scale = 1)
#import sklearn
import PIL
from PIL import Image
import pickle
#from sklearn.model_selection import train_test_split
#from sklearn.model_selection import KFold
#from sklearn.model_selection import cross_validate
#from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score



st.sidebar.header('User Input Parameters')

def user_input_features():
    # Create a list of Species for the selectbox
    Species = st.sidebar.select_slider("Species", options = ['Tradescantia', 'Peperomia', 'Spathiphyllum', 'Philodendron','Monalisa', 'Chlorophytum'])
    #Species = st.sidebar.slider('Species', 0, 5, 0)
    Qin = st.sidebar.slider('Light Intensity (PAR)', 0, 1200, 70)
    Ca = st.sidebar.slider('Ambient CO_2 levels (ppm)', 0, 1500,400 )
    RH = st.sidebar.slider('Relative Humidity (%)', 20, 80, 60)
    data = {'Species': Species,
            'Qin': Qin,
            'RH': RH,
            'Ca':Ca}
    features = pd.DataFrame(data, index=[0])
    labels_dict_rev = {
    'Tradescantia':0,
    'Peperomia':1,
    'Spathiphyllum':2,
    'Monalisa':3,
    'Philodendron':4,
    'Chlorophytum':5
    }
    features['Species'] = features['Species'].replace(labels_dict_rev)
    features = features[['Ca','Qin','RH','Species']]

    return features

df = user_input_features()

st.subheader('User Input parameters')
st.write(df)

# Prediction:
with open("XGB.pkl", 'rb') as file:
    model = pickle.load(file)

prediction = model.predict(df)
#prediction = fit_model.predict(df)
st.subheader(f'$CO_2$ Assimilation rate prediction {np.round(prediction,2)} µmol m$^2 s^{-1}$')
st.write(prediction)
