'''
Version: 1.4.3
Date: 9-12-2023

Allows User to get all Playlists for a Channel given its Id or Name.


Updates:
    - Used sets to remove any duplicates being added to spotify playlists
Future updates:
    - Add a Checkbox right next to the multiselect to select all
    - Add a Counter to show progress
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
