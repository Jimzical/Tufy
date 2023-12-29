'''
Version: 1.6.3
Date: 29-12-2023

Allows User to get all Playlists for a Channel given its Id or Name.


Updates:
    - Added Missing Docs
Future updates:
    - Deploy Website
Current Issues:
'''
import streamlit as st
import components.HelperComponents as hc
import components.YoutubeElements as ye
import components.SpotifyElements as se
import components.YoutubeToSpotify as yts

def main(): 
    hc.ColoredHeader('Youtube To Spotify Convertor',anchor=False)

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
