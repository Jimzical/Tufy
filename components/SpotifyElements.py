'''
This file contains all the functions that are used to get the spotify streamlit elements
'''

import streamlit as st
from components.YoutubeHelper import *
from components.SpotifyHelper import *

def getYoutubeToSpotifySongIDs(youtube,spc,yt_playlistIDs) -> dict():
    '''
    Example
    --------
    youtube_to_spotify_uri = {
        "playlist 1" : {
            "song 1" : "uri 1", 
            "song 2" : "uri 2",
            "song 3" : "uri 3"
        }
    }
    '''
    st.title("Getting the Spotify URIs")
    youtube_to_spotifiy_uri = {} 

    # for each youtube playlist 
    for chosen_playlist in yt_playlistIDs.keys():
        playlist_name = chosen_playlist
        st.subheader(f"Playlist: {playlist_name}")

        playlist_songs = returnPlaylistItems(youtube,yt_playlistIDs[chosen_playlist])
        
        # Initialising a list for each playlist
        youtube_to_spotifiy_uri[playlist_name] = []
        

        counter = 0
        with st.status(f"Gettting Info for {playlist_name}",expanded=True) as status:
            for song in playlist_songs:
                # getting songID data for spotify
                song_data = searchTrack(spc, song)
                
                # appeding {name : id} to the list of songs to the list with the key as playlist name in this main dict 
                youtube_to_spotifiy_uri[playlist_name].append({song_data['track_name'] : song_data['track_id']})
                
                # get count of songs so far
                counter = counter + 1

                # displaying songs and the spotify links
                st.markdown(f"{counter}: {song_data['track_name']} ->  https://open.spotify.com/track/{song_data['track_id']}")
            status.update(label="Got all Info", state="complete",expanded=False)
            st.toast(f"Completed Playlist: {playlist_name}")

        st.write(youtube_to_spotifiy_uri)
    st.toast("Completed All")

    return youtube_to_spotifiy_uri