'''
Version: 1.4.1
Date: 9-12-2023

Allows User to get all Playlists for a Channel given its Id or Name.


Updates:
    - Upgraded the Search feature with better default values as well
    - Fixed the 100 songs limit
Future updates:
    - Add a Checkbox right next to the multiselect to select all
    - Deploy Website
    - Maybe upgrade the append-song feature to find the last common song intead of just checking the last song
        - CAN USE SETS TO DO THIS   
Current Issues:
    - MAJOR: songs seem repeat, might be a cache issue or seach issue [ FOUND: when trying the ........ playlist]
        POSSIBLE SOLUTION: replace with no multithreading function and check
    - Remove Redundant Functions from the multithreading file
        - And check if its the cause for the above error
    - Rename that function to match the other functions
'''
import streamlit as st
import components.HelperComponents as hc
import components.YoutubeHelper as yh
import components.YoutubeElements as ye
import components.SpotifyHelper as sh
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


    testbutton = st.button("Test")
    if testbutton:
        id = "PL08xzvm7_udyKrmapy8TFfBCMnkAiOaFR"
        um = yh.returnPlaylistItems(youtube,id)
        st.write(um)
        short = um[0:12]
        st.write(short)

        uri_dict = {}

        for song in short:
            song_data = sh.searchTrack(spc, song)
            uri_dict[song_data['track_id']] = song_data['track_name']

        st.write( uri_dict )
    # ------------------------------ Spotify -------------------------------
    # Spotify Playlist IDs
    with st.sidebar:
        hc.ColoredHeader("Start Creating Playlist!")
        se.SpotifyIntegration(youtube, sp, spc, yt_chosen_playlistIDs)

if __name__ == '__main__':
    main()
