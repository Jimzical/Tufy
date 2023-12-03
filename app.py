'''
Version: 0.2.0
Date: 03-12-2023

Allows User to get all Playlists for a Channel given its Id or Name.

Current Issues:
    - choosePlaylsit changed to multiselect from selectbox so gotta fix the docs and currently have a temp fix to use only the first one


Updates:
    - Cleaned up Code
    - Added Docstrings
    - Raise Error on Invalid Channel Name

Future updates:
    - fixing channel name cache issue
    - adding spotify functionality

'''
import streamlit as st
from googleapiclient.discovery import build
from components.YoutubeHelper import *
from components.YoutubeElements import *
from components.SpotifyHelper import *


def main(): 
    st.title('Youtube Channel Information')
    # Create a YouTube API object
    youtube = InitializeYoutube()
    sp = InitializeSpotify()

    tab1,tab2 = st.tabs(["Channel Id","Channel Name"])
    try:
        with tab1:
            thru_id = throughChannelId(youtube)
        with tab2:
            thru_name = throughChannelName(youtube)
       
    except:
        st.error("Invalid Channel Name")
        return
        
    if thru_id:
        channel_id = thru_id
    elif thru_name:
        channel_id = thru_name

    # Get all playlists for that channel
    try:
        playlists = get_all_playlists(youtube, channel_id)
    except:
        st.error("No Playlists Found")
        return

    chosen_playlist = choosePlaylist(playlists)

    # TEMP FIX ----> Using only the first playlist
    chosen_playlist = chosen_playlist[0]

    # Display playlist information
    toggle_youtube_display = st.toggle('Display Playlist Items')
    if toggle_youtube_display:
        displayPlaylistItems(youtube,chosen_playlist)

    toggle_spotify_display = st.toggle("Display Spotify Results")
    if toggle_spotify_display:
        playlist_songs = returnPlaylistItems(youtube,chosen_playlist)
        for song in playlist_songs:
            with st.expander(f"{song}",expanded=True):
                track_list = searchTrack(sp, song)
                st.write(track_list)
                st.markdown(f"https://open.spotify.com/track/{track_list['track_id']}")
                

    # track_name = st.text_input('Enter track name')
    # if track_name:
    #     track_list = searchTrack(sp, track_name)
    #     st.write(track_list)


if __name__ == '__main__':
    main()
