'''
Version: 0.5.0
Date: 03-12-2023

Allows User to get all Playlists for a Channel given its Id or Name.

Current Issues:
    - Put all the Functions where they belong
    - Remove the default Channel ID
    - Remove testMode from choosePlaylist in YoutubeElements
Updates:
    -
Future updates:
    - fixing channel name cache issue
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
   
    channel_id = chooseChannel(youtube)

    # Get all playlists for that channel
    try:
        playlists = get_all_playlists(youtube, channel_id)
    except:
        st.error("No Playlists Found")
        return

    playlist_IDs = choosePlaylist(playlists, testMode=True)


    playlist_id_title_mapping = {}
    for playlist in playlists:
        playlist_id_title_mapping[playlist['ID']] = playlist['Title']
    
    # Youtube Display Stuff 
    toggleDisplayPlaylistItems(youtube,playlist_IDs,playlist_id_title_mapping)

    # Spotify Stuff
    toggle_spotify_display = st.toggle("Display Spotify Results")
    if toggle_spotify_display:
        st.title("Getting the Spotify URIs")
        track_details = {}
        youtube_to_spotfiy_songID = {} 

        # for each youtube playlist 
        for chosen_playlistID in playlist_IDs:
            playlist_name = playlist_id_title_mapping[chosen_playlistID]
            st.subheader(f"Playlist: {playlist_name}")

            playlist_songs = returnPlaylistItems(youtube,chosen_playlistID)
            # Example
            # --------
            # youtube_to_spotify_songIDs = {
            #     "playlist 1" : {
            #         "song 1" : "song id", 
            #         "song 2" : "song id",
            #         "song 3" : "song id"
            #     }
            # }

            # Initialising a list for each playlist
            youtube_to_spotfiy_songID[playlist_name] = []

            counter = 0
            with st.status(f"Gettting Info for {playlist_name}",expanded=True) as status:
                for song in playlist_songs:
                    track_data = searchTrack(spc, song)
                    
                    track_details[playlist_name][track_data["track_name"]] = track_data["track_id"]

                    # appeding {name : id} to the list of songs to the list with the key as playlist name in this main dict 
                    youtube_to_spotfiy_songID[playlist_name].append({track_data['track_name'] : track_data['track_id']})
                    
                    
                    counter = counter + 1
                    st.markdown(f"{counter}: {track_data['track_name']} ->  https://open.spotify.com/track/{track_data['track_id']}")
                status.update(label="Got all Info", state="complete",expanded=False)
                st.toast(f"Completed Playlist: {playlist_name}")

            st.write(youtube_to_spotfiy_songID)
        st.toast("Completed All")

    with st.sidebar:
        me = sp.current_user()
        st.write(me)

        # Get current user's playlists
        user_playlists = sp.current_user_playlists()
        # user_playlists_name_list = [playlist["name"] for playlist in user_playlists["items"]]
        user_playlists_name_list = [playlist["name"].lower().strip() for playlist in user_playlists["items"]]

        # st.subheader("user_playlists_name_list")
        # st.write(user_playlists_name_list)

        # for chosen_playlistID in playlist_IDs:
        #     # if not exist in account lib add
        #     if playlist_id_title_mapping[chosen_playlistID].strip().lower() in user_playlists_name_list:
        #         break

        #     sp.user_playlist_create(
        #         user=me["id"],
        #         name=playlist_id_title_mapping[chosen_playlistID]
        #     )
        #     st.toast(f"Added Spotify Playlist called {playlist_id_title_mapping[chosen_playlistID]}")
        # st.toast("Created all Necessary Playlist!")


if __name__ == '__main__':
    main()
