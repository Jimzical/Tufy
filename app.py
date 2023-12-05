'''
Version: 0.4.0
Date: 03-12-2023

Allows User to get all Playlists for a Channel given its Id or Name.

Current Issues:
    - Remove the default Channel ID
    - Fix documentation and naming schemes
Updates:
    - Fixed Oauth Bug where there way an infinite tab opening
    - Added Create Playlist Feature for Spotify
Future updates:
    - fixing channel name cache issue
    - adding documentation to new functions
    - adding songs to playlist in spotify
'''
import streamlit as st
from streamlit import secrets
from googleapiclient.discovery import build
from components.YoutubeHelper import *
from components.YoutubeElements import *
from components.SpotifyHelper import *

def main(): 
    st.title('Youtube Channel Information')
    # Create a YouTube API object
    youtube = InitializeYoutube()

    sp_oauth = StreamlitInitializeSpotifyAuth(
        client_id = secrets["spotify"]["client_id"],
        client_secret = secrets["spotify"]["client_secret"],
        redirect_uri = secrets["spotify"]["redirect_uri"]
    )
    auth_url = getAuthLink(sp_oauth)
    auth_link = st.empty()
    auth_link.markdown(f"Click [here]({auth_url}) to authorize the app.")
    try:
        auth_code = st.experimental_get_query_params()["code"]
    except:
        st.info("Please Click the Link to Choose your Account")
        return

    sp = FinalzieAuth(sp_oauth=sp_oauth,auth_code=auth_code)
   
    auth_link.empty()

    spc = InitializeSpotifyClient(
            client_id = secrets["spotify"]["client_id"],
            client_secret = secrets["spotify"]["client_secret"],
    )
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

    chosen_playlist_options = choosePlaylist(playlists, testMode=True)

    cleaned_playlists = {}
    for playlist in playlists:
        cleaned_playlists[playlist['ID']] = playlist['Title']

    toggle_youtube_display = st.toggle('Display Playlist Items')
    if toggle_youtube_display:
        total_songs = 0
        for chosen_playlist in chosen_playlist_options:
            with st.status(f"Gettting Info for {cleaned_playlists[chosen_playlist]}",expanded=True) as status:
                st.subheader(f"Playlist: {cleaned_playlists[chosen_playlist]}")
                playlist_songs = returnPlaylistItems(youtube,chosen_playlist)
                st.write(playlist_songs)
                st.write(len(playlist_songs))
                total_songs += len(playlist_songs)
            status.update(label="Got all Info", state="complete",expanded=True)
        st.title(f"`Total Number of Songs ➡️ {total_songs}`")
    toggle_spotify_display = st.toggle("Display Spotify Results")
    if toggle_spotify_display:
        st.title("Getting the Spotify URIs")
        track_details = {}
        for chosen_playlist in chosen_playlist_options:
            st.subheader(f"Playlist: {cleaned_playlists[chosen_playlist]}")
            track_details[cleaned_playlists[chosen_playlist]] = {}
            playlist_songs = returnPlaylistItems(youtube,chosen_playlist)

            counter = 0
            with st.status(f"Gettting Info for {cleaned_playlists[chosen_playlist]}",expanded=True) as status:
                for song in playlist_songs:
                    track_list = searchTrack(spc, song)
                    
                    track_details[cleaned_playlists[chosen_playlist]][track_list["track_name"]] = track_list["track_id"]
                    
                    counter = counter + 1
                    st.markdown(f"{counter}: {track_list['track_name']} ->  https://open.spotify.com/track/{track_list['track_id']}")
                status.update(label="Got all Info", state="complete",expanded=False)
                st.toast(f"Completed Playlist: {cleaned_playlists[chosen_playlist]}")
        st.toast("Completed All")

    with st.sidebar:
        me = sp.current_user()
        st.write(me)

        # Get current user's playlists
        user_playlists = sp.current_user_playlists()
        # user_playlists_name_list = [playlist["name"] for playlist in user_playlists["items"]]
        user_playlists_name_list = [playlist["name"].lower().strip() for playlist in user_playlists["items"]]

        st.subheader("user_playlists_name_list")
        st.write(user_playlists_name_list)

        for chosen_playlist in chosen_playlist_options:
            # if not exist in account lib add
            if cleaned_playlists[chosen_playlist].strip().lower() in user_playlists_name_list:
                break

            sp.user_playlist_create(
                user=me["id"],
                name=cleaned_playlists[chosen_playlist]
            )
            st.toast(f"Added Spotify Playlist called {cleaned_playlists[chosen_playlist]}")
        st.toast("Created all Necessary Playlist!")


if __name__ == '__main__':
    main()
