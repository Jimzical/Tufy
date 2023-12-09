'''
Version: 1.2.1
Date: 9-12-2023

Allows User to get all Playlists for a Channel given its Id or Name.


Updates:
    - Cleaned up code
    - Put all functions in their respective files
    - Fixed the Error where button needed to be double clicked to work
Future updates:
    - Deploy Website
'''
import streamlit as st
from streamlit import secrets
from googleapiclient.discovery import build
import components.HelperComponents as hc
import components.YoutubeHelper as yh
import components.YoutubeElements as ye
import components.SpotifyHelper as sh
import components.SpotifyElements as se
import components.YoutubeToSpotify as yts

def main(): 
    hc.ColoredHeader('Youtube Channel Information',anchor=False)

    # ------------------------------ Authentication -------------------------
    
    try:
        items = yts.Authentication()
        youtube = items["youtube"]
        sp = items["spotify"]
        spc = items["spotify_no_auth"]
    except:
        st.stop()   

    # ------------------------------ Youtube -------------------------------
    # Youtube Channel IDs
    yt_chosen_playlistIDs = ye.youtubeData(youtube)

    # Youtube Display Stuff
    ye.youtubeDisplayElements(youtube, yt_chosen_playlistIDs)

    # ------------------------------ Spotify -------------------------------
    # Spotify Playlist IDs
    with st.sidebar:
        hc.ColoredHeader("Start Creating Playlist!")
        se.SpotifyIntegration(youtube, sp, spc, yt_chosen_playlistIDs)

if __name__ == '__main__':
    main()
