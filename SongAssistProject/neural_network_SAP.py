from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import seaborn as sn
import data_in_manipulation as dm

load_dotenv()
playlist_id0 = os.getenv("PLAYLIST_ID0")
playlist_id1 = os.getenv("PLAYLIST_ID1")
playlist_id2 = os.getenv("PLAYLIST_ID2")
playlist_id3 = os.getenv("PLAYLIST_ID3")

test_playlist_id = os.getenv("PLAYLIST_TEST")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
token = dm.get_token()

df = dm.all_playlist_df(token, playlist_id0, playlist_id1, playlist_id2, playlist_id3)


df_before_train_playlist = dm.get_playlist_dataframe(token, test_playlist_id, 6)
print(df)
target = df.pop('target') #defining a target series
num_features = ['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms','time_signature']
df_num_features = df[num_features] #cutting down our data frame to only the info we want
tf.convert_to_tensor(df_num_features) #converting dataframe object to something our NN can handle
normalizer = tf.keras.layers.Normalization(axis=-1) #creating the input layer
normalizer.adapt(df_num_features) #the layer will compute a mean and variance separately for each position in each axis specified by the axis

#print(normalizer(df_num_features.iloc[:3]))

df_train_playlist = df_before_train_playlist[num_features]

def create_NN(): #defining neural network model object
    model = keras.models.Sequential([                                #creating a 'dense' neural network of 784 
        normalizer,
        keras.layers.Dense(50, activation='relu'),
        keras.layers.Dense(25, activation = 'swish'),
        keras.layers.Dense(4,  activation='sigmoid') #inputs (brightness of each pixel:0.0-1.0) 
    ])                                                               #and 10 outputs (number prediction: 0-10)

    model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics =['accuracy']
    )
    return model 



model = create_NN()
model.fit(df_num_features, target, epochs = 5, batch_size = 1)

predicted = model.predict(df_train_playlist)  

#print(len(predicted))

print(predicted)