'''
Version: 0.3.0
Date: 03-12-2023

Allows User to get all Playlists for a Channel given its Id or Name.

Current Issues:
    - 

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
    spc = InitializeSpotifyClient()
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

    chosen_playlist_options = choosePlaylist(playlists, chooseAll=True)

    cleaned_playlists = {}
    for playlist in playlists:
        cleaned_playlists[playlist['ID']] = playlist['Title']

    toggle_youtube_display = st.toggle('Display Playlist Items')
    if toggle_youtube_display:
        total_songs = 0
        for chosen_playlist in chosen_playlist_options:

            playlist_songs = returnPlaylistItems(youtube,chosen_playlist)
            st.subheader(f"Playlist: {cleaned_playlists[chosen_playlist]}")
            st.write(playlist_songs)
            st.write(len(playlist_songs))
            total_songs += len(playlist_songs)

        st.subheader(total_songs)
    toggle_spotify_display = st.toggle("Display Spotify Results")
    if toggle_spotify_display:
        track_details = {}
        for chosen_playlist in chosen_playlist_options:
            st.subheader(f"Playlist: {cleaned_playlists[chosen_playlist]}")
            track_details[chosen_playlist] = {}
            playlist_songs = returnPlaylistItems(youtube,chosen_playlist)
            for song in playlist_songs:
                track_list = searchTrack(spc, song)
                track_details[chosen_playlist][track_list["track_name"]] = track_list["track_id"]
                st.write(track_list["track_name"])
                st.markdown(f"https://open.spotify.com/track/{track_list['track_id']}")

            st.toast(f"Completed Playlist: {cleaned_playlists[chosen_playlist]}")
        st.toast("Completed All")


if __name__ == '__main__':
    main()
