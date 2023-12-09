'''
This file contains all the functions that are used to get the spotify streamlit elements
'''

import streamlit as st
from components.YoutubeHelper import *
from components.SpotifyHelper import *
from components.HelperComponents import Notif
import components.YoutubeToSpotify as yts

def getYoutubeToSpotifySongIDs(youtube : object,spc : object,yt_playlistIDs : dict) -> dict():
    '''
    Get the Spotify URIs for songs in the youtube playlists
    
    Parameters
    ----------
    youtube : object
        The youtube object from the Youtube API
    spc : object
        The spotify object from the Spotify API
    yt_playlistIDs : dict
        The dictionary of playlist names and their IDs from youtube

    Returns
    -------
    youtube_to_spotify_uri : dict
        The dictionary of playlist names and their IDs from youtube
        

    Example
    --------
    >>> yt_playlistIDs = {
        "playlist 1" : "id 1",
        "playlist 2" : "id 2",
        "playlist 3" : "id 3"
    }

    >>> youtube_to_spotify_uri = getYoutubeToSpotifySongIDs(youtube,spc,yt_playlistIDs)
    
    youtube_to_spotify_uri = {
    "playlist 1" : {
            "song 1" : "uri 1", 
            "song 2" : "uri 2",
            "song 3" : "uri 3"
        }
    }
    '''
    st.title("Getting the Spotify URIs")
    youtube_to_spotifiy_uri = {} 

    # for each youtube playlist 
    for playlist_name in yt_playlistIDs.keys():
        playlist_songs = returnPlaylistItems(youtube,yt_playlistIDs[playlist_name])
        
        # Initialising a list for each playlist
        youtube_to_spotifiy_uri[playlist_name] = []
        

        counter = 0
        with st.status(f"Gettting Info for {playlist_name}",expanded=True) as status:
            for song in playlist_songs:
                # getting songID data for spotify
                song_data = searchTrack(spc, song)
                
                # appeding {name : id} to the list of songs to the list with the key as playlist name in this main dict 
                youtube_to_spotifiy_uri[playlist_name].append({song_data['track_name'] : song_data['track_id']})
                
                # get count of songs so far
                counter = counter + 1

                # displaying songs and the spotify links
                st.markdown(f"{counter}: {song_data['track_name']} ->  https://open.spotify.com/track/{song_data['track_id']}")
            status.update(label="Got all Info", state="complete",expanded=False)
            st.toast(f"Completed Playlist: {playlist_name}")

        # st.write(youtube_to_spotifiy_uri)
    st.toast("Completed All")

    return youtube_to_spotifiy_uri


def SpotifyIntegration(youtube : object,sp : object, spc : object, yt_chosen_playlistIDs : dict) -> None:
    '''
    Create Streamlit UI to integrate Spotify with Youtube

    Parameters
    ----------
    youtube : object
        Youtube API object
    sp : object
        Spotify API object
    spc : object
        No Auth Spotify API object
    yt_chosen_playlistIDs : dict
        Dictionary of playlist ID and playlist title

    Examples
    --------
    >>> yt_playlistIDs = {
        "playlist 1" : "id 1",
        "playlist 2" : "id 2",
        "playlist 3" : "id 3"
    }

    >>> SpotifyIntegration(youtube,sp,spc,yt_playlistIDs)
    '''

    me = sp.current_user()

    # Get current user's yt_channel_playlists
    sp_user_playlists = sp.current_user_playlists()
    
    sp_userPlaylistsName_list = [sp_playlist["name"] for sp_playlist in sp_user_playlists["items"]]
    sp_userPlaylist_to_uri_dict = {sp_playlist["name"]: sp_playlist["id"] for sp_playlist in sp_user_playlists["items"]}

    sp_add_songs = st.button("Add Songs",help="Add songs to your Spotify Playlist",use_container_width=True)
    if sp_add_songs:
        # CREATING PLAYLIST IF THEY DONT EXIST
        for playlist_name in yt_chosen_playlistIDs.keys():

            # if exists, skip
            if playlist_name in sp_userPlaylistsName_list:
                st.toast(f"Playlist {playlist_name} already exists")
            else:
                new_playlist = sp.user_playlist_create(
                    user=me["id"],
                    name=playlist_name
                )

                sp_userPlaylist_to_uri_dict[playlist_name] = new_playlist["uri"]
                st.toast(f"Added Spotify Playlist called {playlist_name}")
        
        Notif(message = "Created all Necessary Playlist!")

        # GETTING SPOTIFY URIs
        with st.status("Getting Spotify URIs",expanded=False) as status:
            st.caption("This may take a while...")
            yt_sp_songURIs = yts.getYoutubeToSpotifySongIDs(youtube,spc,yt_chosen_playlistIDs)
            status.update(label="Got all Info", state="complete",expanded=False)


        # ADDING SONGS TO PLAYLIST    
        with st.status("Adding Songs",expanded=True) as status:
            for playlist_name in yt_chosen_playlistIDs:
                st.write(f"Adding songs to `{playlist_name}` playlist")
                sp.playlist_add_items(
                    playlist_id=sp_userPlaylist_to_uri_dict[playlist_name],
                    items=yt_sp_songURIs[playlist_name]
                )                    

            status.update(label="Added Songs", state="complete",expanded=False)
