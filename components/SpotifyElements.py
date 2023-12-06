'''
This file contains all the functions that are used to get the spotify streamlit elements
'''

import streamlit as st
from components.YoutubeHelper import *
from components.SpotifyHelper import *

def getYoutubeToSpotifySongIDs(youtube,spc,youtube_playlistIDs,playlist_id_title_dict):
    st.title("Getting the Spotify URIs")
    youtube_to_spotfiy_songID = {} 

    # for each youtube playlist 
    for chosen_playlistID in youtube_playlistIDs:
        playlist_name = playlist_id_title_dict[chosen_playlistID]
        st.subheader(f"Playlist: {playlist_name}")

        playlist_songs = returnPlaylistItems(youtube,chosen_playlistID)
        
        # Initialising a list for each playlist
        youtube_to_spotfiy_songID[playlist_name] = []
        
        # '''
        # Example
        # --------
        # youtube_to_spotify_songIDs = {
        #     "playlist 1" : {
        #         "song 1" : "song id", 
        #         "song 2" : "song id",
        #         "song 3" : "song id"
        #     }
        # }
        # '''

        counter = 0
        with st.status(f"Gettting Info for {playlist_name}",expanded=True) as status:
            for song in playlist_songs:
                # getting songID data for spotify
                song_data = searchTrack(spc, song)
                
                # appeding {name : id} to the list of songs to the list with the key as playlist name in this main dict 
                youtube_to_spotfiy_songID[playlist_name].append({song_data['track_name'] : song_data['track_id']})
                
                # get count of songs so far
                counter = counter + 1

                # displaying songs and the spotify links
                st.markdown(f"{counter}: {song_data['track_name']} ->  https://open.spotify.com/track/{song_data['track_id']}")
            status.update(label="Got all Info", state="complete",expanded=False)
            st.toast(f"Completed Playlist: {playlist_name}")

        st.write(youtube_to_spotfiy_songID)
    st.toast("Completed All")

    return youtube_to_spotfiy_songID