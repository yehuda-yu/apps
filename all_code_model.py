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



st.markdown("""
# CO$_2$ Assimilation Prediction App
""")
# present the gw image
image = Image.open("Images/gw_image.jpg")
st.image(image, caption='Green Wall in The M&M VS Lab at the Hebrew University')
st.markdown("""
#### This app predicts the **CO$_2$ Assimilation** of 6 different indoor plants based on AI algorithm.

###### Use the slide bars to set your indoor condition and get a quantitative estimate of the amount of CO$_2$ levels that your plants reduce indoor.
###### Alternatively, you can use this application to match the type of plant with the highest potential for reducing the levels of CO$_2$ in the room :full_moon_with_face:)
""")



st.sidebar.header('User Input Parameters')

#Dict for replace species name to number:
labels_dict_rev = {
'Tradescantia':0,
'Peperomia':1,
'Spathiphyllum':2,
'Monalisa':3,
'Philodendron':4,
'Chlorophytum':5
}
def user_input_features():
    # Create a list of Species for the selectbox
    options = ['Tradescantia', 'Peperomia', 'Spathiphyllum', 'Philodendron','Monalisa', 'Chlorophytum']
    Species = st.sidebar.selectbox('Species:', options)
    Qin = st.sidebar.slider('Light Intensity (PAR)', 0, 1200, 70)
    Ca = st.sidebar.slider('Ambient CO2 levels (ppm)', 0, 1500,400 )
    RH = st.sidebar.slider('Relative Humidity (%)', 20, 80, 60)
    data = {'Species': Species,
            'Qin': Qin,
            'RH': RH,
            'Ca':Ca}
    features = pd.DataFrame(data, index=[0])
    features['Species'] = features['Species'].replace(labels_dict_rev)
    features = features[['Ca','Qin','RH','Species']]

    return features

df = user_input_features()

st.subheader('User Input parameters')
st.write(df)

# Prediction:
prediction = fit_model.predict(df)
st.write(f'CO$_2$ Assimilation rate prediction {np.round(prediction[0],2)} µmol m$^2 s^{-1}$')



##### Predict under this condition which species assimilate more CO2 ##### 

st.subheader('Which Species Is Better Under Your conditions?')
# list of Species
species = ['Tradescantia', 'Peperomia', 'Spathiphyllum', 'Philodendron','Monalisa', 'Chlorophytum']
predictions = [] # empty list for prediction:
# Predict assismilation rate for each species:
for plant in species:
  df['Species'] = plant
  df['Species'] = df['Species'].replace(labels_dict_rev)
  prediction = fit_model.predict(df)
  predictions.append(prediction)

# Find the maximum value in the list
max_value = max(predictions)
# Find the index of the maximum value in the prediction list
max_index = predictions.index(max_value)
# Find the species of the maximum value in the prediction list:
top_species = species[max_index]
st.write(f'Under this conditions, the best species for reduce CO$_2$ is {top_species} with {np.round(max_value[0],2)} µmol m$^2 s^{-1}$')

##### Show image ot the species with highest assimilation rate ##### 
images_dict = {
'Tradescantia':"Images/Tradescantia.jpg",
'Peperomia':"Images/Peperomia.jpg",
'Spathiphyllum':"Images/Sphatophilum.jpg",
'Monalisa':"Images/Monalisa.jpg",
'Philodendron':"Images/Philodendron.jpg",
'Chlorophytum':"Images/Chloropytum.jpg"
}
img = Image.open(images_dict[top_species]) # image based on top assimilation species
st.image(img, caption=top_species,width=400)
# Credit header
st.markdown(""" 
Credit: [Yehuda Yungstein](mailto:yehudayu@gmail.com)
""")
