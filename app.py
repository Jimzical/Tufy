'''
Version: 0.5.1
Date: 03-12-2023

Allows User to get all Playlists for a Channel given its Id or Name.

Current Issues:
    - Test changes in SpSpotifyHelper 
    - Put all the Functions where they belong
    - Remove the default Channel ID
    - Remove testMode from choosePlaylist in YoutubeElements
Updates:
    - Fixed Naming Schemes to be Clearer
    - Added SpotifyHelper Documentation
Future updates:
    - fixing channel name cache issue
'''
import streamlit as st
from streamlit import secrets
from googleapiclient.discovery import build
from components.helper_components import ColoredHeader, Notif
import components.YoutubeHelper as yh
import components.YoutubeElements as ye
import components.SpotifyHelper as sh
import components.SpotifyElements as se

def main(): 
    ColoredHeader('Youtube Channel Information',anchor=False)


    #  ----------------------------------------------------------------------
    # ------------------------------ Authentication -------------------------
    # ----------------------------------------------------------------------

    # Create a YouTube API object
    youtube = yh.InitializeYoutube()
    sp_oauth = sh.StreamlitInitializeSpotifyAuth(
        client_id = secrets["spotify"]["client_id"],
        client_secret = secrets["spotify"]["client_secret"],
        redirect_uri = secrets["spotify"]["redirect_uri"]
    )
    auth_url = sh.getAuthLink(sp_oauth)
    auth_link = st.empty()
    auth_link.markdown(f"Click [here]({auth_url}) to authorize the app.")
    try:
        auth_code = st.experimental_get_query_params()["code"]
    except:
        st.info("Please Click the Link to Choose your Account")
        return

    sp = sh.FinalzieAuth(sp_oauth=sp_oauth,auth_code=auth_code)
   
    auth_link.empty()

    spc = sh.InitializeSpotifyClient(
            client_id = secrets["spotify"]["client_id"],
            client_secret = secrets["spotify"]["client_secret"],
    )
    
    # ----------------------------------------------------------------------
    # ------------------------------ Youtube -------------------------------
    # ----------------------------------------------------------------------


    yt_channel_id = ye.chooseChannel(youtube)

    # Get all yt_channel_playlists for that channel
    try:
        yt_channel_playlists = yh.get_all_playlists(youtube, yt_channel_id)
    except:
        st.error("No Playlists Found")
        return

    yt_playlistIDs = ye.choosePlaylist(yt_channel_playlists, testMode=True)

    # TODO : Remove this
    # yt_playlist_id_title_dict = {}
    # for yt_playlist in yt_channel_playlists:
    #     yt_playlist_id_title_dict[yt_playlist['ID']] = yt_playlist['Title'].strip().lower()
        # yt_playlist_title_id_dict = {yt_playlist['Title'].strip().lower(): yt_playlist['ID'] for yt_playlist in yt_channel_playlists}
    
    # Youtube Display Stuff 
    ye.toggleDisplayPlaylistItems(youtube,yt_playlistIDs)

    # ----------------------------------------------------------------------
    # ------------------------------ Spotify -------------------------------
    # ----------------------------------------------------------------------

    # Spotify Stuff
    toggle_spotify_display = st.toggle("Display Spotify Results")
    if toggle_spotify_display:
        yt_to_sp_songIDs = se.getYoutubeToSpotifySongIDs(youtube,spc,yt_playlistIDs)
    
    with st.sidebar:
        ColoredHeader("Start Creating Playlist!")
        me = sp.current_user()

        # Get current user's yt_channel_playlists
        sp_user_playlists = sp.current_user_playlists()
        sp_userPlaylistsName_list = [sp_playlist["name"].lower().strip() for sp_playlist in sp_user_playlists["items"]]
        sp_userPlaylistName_ID_dict = {sp_playlist["name"].lower().strip(): sp_playlist["id"] for sp_playlist in sp_user_playlists["items"]}



        if st.toggle("Display Existing Playlist Names"):
            st.write(sp_userPlaylistName_ID_dict)


        # CREATING PLAYLIST IF THEY DONT EXIST
        sp_create_playlist = st.button("Create Playlist",help="Recommended before adding songs",use_container_width=True)
        if sp_create_playlist:    
            for playlist_name in yt_playlistIDs.keys():

                playlist_name = playlist_name.lower().strip()
                # if exists, skip
                if playlist_name in sp_userPlaylistsName_list:
                    st.toast(f"Playlist {playlist_name} already exists")
                else:
                    sp.user_playlist_create(
                        user=me["id"],
                        name=playlist_name
                    )
                    st.toast(f"Added Spotify Playlist called {playlist_name}")
            
            Notif(message = "Created all Necessary Playlist!")
    
        sp_add_songs = st.button("Add Songs",help="Add songs to your Spotify Playlist",use_container_width=True)
        if sp_add_songs:
            pass

if __name__ == '__main__':
    main()
