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
from components.helper_components import ColoredHeader
from components.YoutubeHelper import *
from components.YoutubeElements import *
from components.SpotifyHelper import *
from components.SpotifyElements import *
def main(): 
    ColoredHeader('Youtube Channel Information',anchor=False)
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
   
    channel_id = chooseChannel(youtube)

    # Get all playlists for that channel
    try:
        playlists = get_all_playlists(youtube, channel_id)
    except:
        st.error("No Playlists Found")
        return

    youtube_playlistIDs = choosePlaylist(playlists, testMode=True)


    playlist_id_title_dict = {}
    for playlist in playlists:
        playlist_id_title_dict[playlist['ID']] = playlist['Title']
    
    # Youtube Display Stuff 
    toggleDisplayPlaylistItems(youtube,youtube_playlistIDs,playlist_id_title_dict)

    # Spotify Stuff
    toggle_spotify_display = st.toggle("Display Spotify Results")
    if toggle_spotify_display:
        youtube_to_spotify_songIDs = getYoutubeToSpotifySongIDs(youtube,spc,youtube_playlistIDs,playlist_id_title_dict)
    
    with st.sidebar:
        ColoredHeader("Start Creating Playlist!")
        me = sp.current_user()

        # Get current user's playlists
        user_playlists = sp.current_user_playlists()
        userPlaylistsName_list = [playlist["name"].lower().strip() for playlist in user_playlists["items"]]
        userPlaylistName_ID_dict = {playlist["name"].lower().strip(): playlist["id"] for playlist in user_playlists["items"]}



        if st.toggle("Display Existing Playlist Names"):
            st.write(userPlaylistName_ID_dict)

        create_playlist = st.button("Create Playlist",help="Recommended before adding songs",use_container_width=True)
        
        if create_playlist:    
            for chosen_playlistID in playlist_IDs:
                playlist_name = playlist_id_title_dict[chosen_playlistID]
                # if not exist in account lib add
                if playlist_name.strip().lower() in userPlaylistsName_list:
                    break

                sp.user_playlist_create(
                    user=me["id"],
                    name=playlist_name
                )
                st.toast(f"Added Spotify Playlist called {playlist_name}")
            st.toast("Created all Necessary Playlist!")
        for chosen_playlistID in playlist_IDs:
            playlist_name = playlist_id_title_dict[chosen_playlistID]
            if playlist_name.strip().lower() in userPlaylistsName_list:
                break



if __name__ == '__main__':
    main()
