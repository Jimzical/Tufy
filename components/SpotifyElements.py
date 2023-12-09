'''
This file contains all the functions that are used to get the spotify streamlit elements
'''

import streamlit as st
from components.YoutubeHelper import *
from components.SpotifyHelper import *

def getYoutubeToSpotifySongIDs(youtube : object,spc : object,yt_playlistIDs : dict) -> dict():
    '''
    Get the Spotify URIs for songs in the youtube playlists
    
    Parameters
    ----------
    youtube : object
        The youtube object from the Youtube API
    spc : object
        The spotify object from the Spotify API
    yt_playlistIDs : dict
        The dictionary of playlist names and their IDs from youtube

    Returns
    -------
    youtube_to_spotify_uri : dict
        The dictionary of playlist names and their IDs from youtube
        

    Example
    --------
    >>> yt_playlistIDs = {
        "playlist 1" : "id 1",
        "playlist 2" : "id 2",
        "playlist 3" : "id 3"
    }

    >>> youtube_to_spotify_uri = getYoutubeToSpotifySongIDs(youtube,spc,yt_playlistIDs)
    
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
    for playlist_name in yt_playlistIDs.keys():
        playlist_songs = returnPlaylistItems(youtube,yt_playlistIDs[playlist_name])
        
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

        # st.write(youtube_to_spotifiy_uri)
    st.toast("Completed All")

    return youtube_to_spotifiy_uri
