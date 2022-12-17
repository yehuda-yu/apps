import streamlit as st
import pandas as pd
import numpy as np
#import seaborn as sns
#sns.set_theme(style="white",font_scale = 1)
import PIL
from PIL import Image
from sklearn.ensemble import RandomForestRegressor

# read the data
path = "Clean_data.xlsx"
data = pd.read_excel(path)
data = data[['A', 'Qin', 'Ca', 'RH','Species']]
#data = data.sample(frac=1) # Shuffle the data 

###### Define features and labels ######
X = data[['Ca','Qin','RH','Species']]
# Standardization:
# X = (X-X.mean())/X.std() #standardization
Y = data.A
# Create model
fit_model = RandomForestRegressor(max_depth=100, n_estimators=800).fit(X,Y)


# Load model:
#with open("RF.pkl", 'rb') as file:
 #   fit_model = pickle.load(file)


st.markdown("""
# CO$_2$ Assimilation Prediction App
""")
# present the gw image
image = Image.open("gw_image.jpg")
st.image(image, caption='Green Wall in The M&M VS Lab at the Hebrew University')
st.markdown("""
#### This app predicts the **CO$_2$ Assimilation** of 6 different indoor plants based on AI algorithm.

###### Use the slide bars to set your indoor condition and get a quantitative estimate of the amount of CO$_2$ levels that your plants reduce indoor.
###### Alternatively, you can use this application to match the type of plant with the highest potential for reducing the levels of CO$_2$ in the room :full_moon_with_face:)
""")



st.sidebar.header('User Input Parameters')

def user_input_features():
    # Create a list of Species for the selectbox
    Species = st.sidebar.select_slider("Species", options = ['Tradescantia', 'Peperomia', 'Spathiphyllum', 'Philodendron','Monalisa', 'Chlorophytum'])
    Qin = st.sidebar.slider('Light Intensity (PAR)', 0, 1200, 70)
    Ca = st.sidebar.slider('Ambient CO2 levels (ppm)', 0, 1500,400 )
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
st.subheader(f'$CO_2$ Assimilation rate prediction {np.round(prediction,2)} µmol m$^2 s^{-1}$')
#st.write(prediction)

st.markdown(""" 
Credit: [Yehuda Yungstein](mailto:yehudayu@gmail.com)
""")
