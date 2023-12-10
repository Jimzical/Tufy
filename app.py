'''
Version: 1.3.1
Date: 9-12-2023

Allows User to get all Playlists for a Channel given its Id or Name.


Updates:
    - Playlist Search is now cached
    - Feature that checks last song in playlist and only adds songs after that
Future updates:
    - Maybe use multithreading in sh to make searchTracks faster (maybe using mulitple ports or smthn)    
    - Deploy Website
    - Maybe upgrade the append-song feature to find the last common song intead of just checking the last song    
Current Issues:
    - Need to add a try execept to searchTrach sidebar status element to catch errors   

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
        youtube,sp,spc = items["youtube"], items["spotify"], items["spotify_no_auth"]
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
