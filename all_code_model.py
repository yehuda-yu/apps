# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 17:25:48 2022

@author: User
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import xgboost as xgb
from xgboost import Booster
#from xgboost import DMatrix
from xgboost import XGBRegressor
import seaborn as sns
sns.set_theme(style="white",font_scale = 1)
#import sklearn
#import PIL
#from PIL import Image
#from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LinearRegression
#from sklearn.model_selection import KFold
#from sklearn.model_selection import cross_validate
#from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
#from sklearn.model_selection import GridSearchCV

# read the data
path = "Assimilation_model_data.xlsx"
data = pd.read_excel(path)
data = data[['A', 'Qin', 'Ca', 'RH','Species']]

labels_dict = {
    1:'Tradescantia',
    '1':'Tradescantia',
    2:'Peperomia',
    '2':'Peperomia',
    3:'Spathiphyllum',
    '3':"Spathiphyllum",
    'Sphatophilum':'Spathiphyllum',
    4:'Philodendron',
    '4': 'Philodendron',
    5: 'Monalisa',
    '5': 'Monalisa',
    6:'Chlorophytum',
    '6':'Chlorophytum',
    'Chlorophitum':'Chlorophytum'
    }
data['Species'] = data['Species'].replace(labels_dict)

data = data.sample(frac=1) # Shuffle the data 

###### Define features and labels ######
X = data[['Ca','Qin','RH']]
# Standardization:
# X = (X-X.mean())/X.std() #standardization
labels_dict_rev = {
    'Tradescantia':0,
    'Peperomia':1,
    'Spathiphyllum':2,
    'Monalisa':3,
    'Philodendron':4,
    'Chlorophytum':5
    }
X['Species'] = data['Species'].replace(labels_dict_rev)
Y = data.A


###### Split the data into train and test ######
X_train_val, X_test, y_train_val, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.25, random_state=0)
xgb_cv = XGBRegressor(colsample_bytree=1.0, learning_rate=0.01, max_depth=7,
             min_child_weight=3, n_estimators=500, objective='reg:squarederror',
             subsample=1.0)

fit_model = xgb_cv.fit(
    X_train,
    y_train,
    eval_metric='mae',
    verbose=False)


st.markdown("""
# CO$_2$ Assimilation Prediction app

#### This app predicts the **CO$_2$ Assimilation** of 6 different indoor plants based on the internal enviroment conditions.

#### You can use this application to match the type of plant with the highest potential for reducing the levels of PAH in the room.
#### Alternatively, you can get a quantitative estimate of the amount of CO$_2$ levels that the plants reduce indoor	:full_moon_with_face:)
""")
#image = Image.open(r"C:\downloads_py\Streamlit\Images\gw_image.jpg")
#st.image(image, caption='Green Wall in The M&M VS Lab at the Hebrew University')


st.sidebar.header('User Input Parameters')

def user_input_features():
    # Create a list of Species for the selectbox
    Species = st.sidebar.select_slider("Species", options = ['Tradescantia', 'Peperomia', 'Spathiphyllum', 'Philodendron','Monalisa', 'Chlorophytum'])
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
prediction = fit_model.predict(df)
import numpy as np
st.subheader(f'$CO_2$ Assimilation rate prediction {np.round(prediction,2)} µmol m$^2 s^{-1}$')
st.write(prediction)
