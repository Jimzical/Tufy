'''
Version: 0.2.0
Date: 03-12-2023

Allows User to get all Playlists for a Channel given its Id or Name.

Current Issues:
    - choosePlaylsit changed to multiselect from selectbox so gotta fix the docs and currently have a temp fix to use only the first one


Updates:
    - Cleaned up Code
    - Added Docstrings

Future updates:
    - fixing raise error when user enters invalid channel name
    - fixing channel name cache issue
    - adding spotify functionality

'''
import streamlit as st
from googleapiclient.discovery import build
from components.YoutubeHelper import *
from components.YoutubeElements import *
from components.SpotifyHelper import *

def YouTubePart():
    st.title('Youtube Channel Information')
    # Create a YouTube API object
    youtube = InitializeYoutube()

    tab1,tab2 = st.tabs(["Channel Id","Channel Name"])
    with tab1:
        thru_id = throughChannelId(youtube)
    with tab2:
        thru_name = throughChannelName(youtube)

    if thru_id:
        channel_id = thru_id
    elif thru_name:
        channel_id = thru_name

    # Get all playlists for that channel
    playlists = get_all_playlists(youtube, channel_id)

    chosen_playlist = choosePlaylist(playlists)

    # TEMP FIX ----> Using only the first playlist
    chosen_playlist = chosen_playlist[0]

    # Display playlist information
    toggle_display = st.toggle('Display Playlist Items')
    if toggle_display:
        displayPlaylistItems(youtube,chosen_playlist)


def SpotifyPart():
    sp = InitializeSpotify()
    track_name = st.text_input('Enter track name')
    if track_name:
        track_list = searchTrack(sp, track_name)
        st.write(track_list)


def main(): 
    YouTubePart()
    # SpotifyPart()

if __name__ == '__main__':
    main()
