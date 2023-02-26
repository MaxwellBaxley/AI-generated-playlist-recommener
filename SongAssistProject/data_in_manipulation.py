from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import pandas as pd

load_dotenv()
playlist_id1 = os.getenv("PLAYLIST_ID")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def make_target_array(pl_num):
    arr = [0,0,0,0]
    for i in len(arr):
        if i == pl_num:
            arr[i]=1
    return arr

def get_token(): #getting a token for accessing API
    auth_string = client_id + ":" + client_secret #getting access to spotifyAPI
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8") #going to return a string of a base64 object

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token): #getting header
    return {"Authorization": "Bearer "+ token}

def get_playlist_tracks(token, playlist_id): #input: playlist id, output:
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)

    result = get(url, headers = headers)
    json_result = json.loads(result.content) #taking my json results and loading them as a dictionary object
    #print(json_result)
    return json_result

def get_playlist_tracks_df(token, playlist_id): #
    result = get_playlist_tracks(token, playlist_id)
    playlistresultsdf = pd.DataFrame(result['items'])
    return playlistresultsdf

def get_audio_features(token, trackid): #gets audio features for track
    url = f"https://api.spotify.com/v1/audio-features/{trackid}"
    headers = get_auth_header(token)
    results = get(url, headers = headers)
    json_results = json.loads(results.content) #taking my json results and loading them as a dictionary object
    return json_results

def get_audio_features_series(token, trackid): #turning audio features into panda Data Frame and getting important features
    result = get_audio_features(token, trackid)
    res_sr = pd.Series(result) #below locates and returns important info
    return res_sr.loc[['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms','time_signature']]

def extract_all_songs_from_playlist(token, playlist_id): #extracting all songs from a playlist and getting audio features.
    df = get_playlist_tracks_df(token, playlist_id)
    size = df.size / 6
    indx = 0
    pl_data_frame = pd.DataFrame()
    for row in df.iterrows():
        id = df.get('track')[indx]['id']
        popularity = df.get('track')[indx]['popularity']
        print(f"{id}      {popularity}")
        indx = indx+1

def get_playlist_dataframe(token, playlist_id, pl_num): #turns a playlist_id into a dataframe with the important audio features data and is indexed by song_id
    play_list_resultsdf=get_playlist_tracks_df(token, playlist_id)
    llist = [] #creating list to append audio featurese series to
    ids = []
    for i in range(len(play_list_resultsdf)-1): #this causes the last song in a playlist to not be added to the data frame.
        song_id = play_list_resultsdf.get('track')[i]['id']
        song_features_series = get_audio_features_series(token, song_id)
        llist.append(song_features_series)
        ids.append(song_id)

    attri_df = pd.DataFrame(llist, index=ids, columns=['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms','time_signature', 'target'])
    attri_df['target'] = pl_num #sets all of target to playlist number 
    #  ^^^^^^^^^^^ 
    return attri_df

def all_playlist_df(token, playlist_id0, playlist_id1, playlist_id2, playlist_id3):
    df_0 = get_playlist_dataframe(token, playlist_id0, 0)
    df_1 = get_playlist_dataframe(token, playlist_id1, 1)
    df_2 = get_playlist_dataframe(token, playlist_id2, 2)
    df_3 = get_playlist_dataframe(token, playlist_id3, 3)
    frames = [df_0, df_1, df_2, df_3]
    df = pd.concat(frames) #creating a date frame of every song in all four playlists
    df.drop_duplicates(keep = 'first') #removing duplicate songs (some playlists may share songs)
    #^^^ probably should "one-hot" this in the future because songs can belong in multiple playlists
    df_shuffled = df.sample(frac = 1) #shuffling the data frame's rows (i.e. randomizing the song order)
    #^^^^ this does help improve the accuracy of the NN
    return df_shuffled

token = get_token()
#print(attri_df.iloc[0, 1:]) #prints all the audio_features data in row 0 as a series
#print(get_playlist_dataframe(token, playlist_id1))
#print(get_playlist_dataframe(token, playlist_id1, 0))