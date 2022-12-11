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


'''
# read the data
path = "Clean_data.xlsx"
data = pd.read_excel(path)
data = data[['A', 'Qin', 'Ca', 'RH','Species']]
#data = data.sample(frac=1) # Shuffle the data 

###### Define features and labels ######
X = data[['Qin', 'Ca', 'RH','Species']]
# Standardization:
# X = (X-X.mean())/X.std() #standardization
Y = data.A


###### Split the data into train and test ######
X_train_val, X_test, y_train_val, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.25, random_state=0)
eval_set = [(X_train, y_train),
            (X_val, y_val)]

xgb_cv = (colsample_bytree=1.0, learning_rate=0.01, max_depth=7,
             min_child_weight=3, n_estimators=500, objective='reg:squarederror',
             subsample=1.0)

fit_model = xgb_cv.fit(
    X_train_val,
    y_train_val,
  set_params=eval_set,
  eval_metric='mae',
  early_stopping_rounds=50,
  verbose=2
)
'''

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
