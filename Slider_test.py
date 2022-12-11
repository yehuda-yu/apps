# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 14:19:23 2022

@author: User
"""
import streamlit as st
import pandas as pd
#import PIL
#from PIL import Image
import xgboost as xgb

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

    return features

df = user_input_features()

st.subheader('User Input parameters')
st.write(df)
st.write(st.__version__)
st.write(pd.__version__)
st.write(xgb.__version__)


#image1 = Image.open(r"C:\downloads_py\Streamlit\Images\Tradescantia.jpg")
#image2 = Image.open(r"C:\downloads_py\Streamlit\Images\Peperomia.jpg")
#image3 = Image.open(r"C:\downloads_py\Streamlit\Images\Sphatophilum.jpg")
#image4 = Image.open(r"C:\downloads_py\Streamlit\Images\Philodendron.jpg")
#image5 = Image.open(r"C:\downloads_py\Streamlit\Images\Monalisa.jpg")
#image6 = Image.open(r"C:\downloads_py\Streamlit\Images\Chloropytum.jpg")

# Create a grid to hold the images
#st.image([image1, image2, image3], width=150)
#st.image([image4, image5, image6], width=150)
