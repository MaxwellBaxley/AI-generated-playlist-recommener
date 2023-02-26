# AI-generated-playlist-recommener
every playlist has a "vibe" and it is often very difficult to pinpoint exactly what that "vibe" is. it is damn-near impossible to explain why a song fits that particular vibe. the goal of this project is for an AI to understand the "vibes" of multiple of your playlists and then determine how well a particular song fits that "vibe."

this is a Neural Network (NN) that is designed to intake four of your playlists and one "test" playlsit. for each song, the program will create a pandas data frame that is indexed by song ID. for each song (rows) it will use the spotify API to find these data points (columns):
'danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms','time_signature','target'
the 'target' data point refers to which playlist the song is found on. this is important information that will be passed to the NN when training it. these are passed as int values. obviously this leads a problem when playlist 1 and playlist 2 share one or more songs between them. currently, duplicate songs are simply removed. in the future, i would like to one-hot encode this to solve this issue.

input:
the input of this NN is found in the .env file provided:
CLIENT_ID= "" #client ID and client secret can be accessed through the spotify API

CLIENT_SECRET = ""

PLAYLIST_ID0 = "" #these are where you input the playlist IDs for the four playlists you want the NN to learn

PLAYLIST_ID1 = "" #they can be found either through the API or by copying everything after the last '/' in the URL

PLAYLIST_ID2 = "" 

PLAYLIST_ID3 = "" 

PLAYLIST_TEST = "" #this is where you put the ID for the playlist that you want it to predict


output:
the NN will output a double array of size [the test playlist size] X [4]. each array represents a song from your playlist and the inner arrays correspond to the probability that they will be in one of your playlist. here is an example:

lets say your "test" playlist is 6 songs long:

       probability of that song being in playlist:
       
        playlist 0|playlist 1|playlist 2|playlist 3
        
song1 [[0.91398555 0.03893068 0.9498765  0.37815166]

 song2 [0.905545   0.13801654 0.85223573 0.2733887 ]
 
 song3 [0.6153971  0.68480366 0.3932283  0.41274834]
 
 song4 [0.7370439  0.15393828 0.80482304 0.45380738]
 
 song5 [0.73338205 0.30363542 0.6327116  0.39805007]
 
 song6 [0.6340241  0.5521786  0.23822287 0.47930247]]
 
 as you can see, for song 1, the NN 91.4% confident that it would fit the "vibe" of playlist 0, 3.9% confident for playlist 1, and so on.

 
