import streamlit as st
from streamlit import secrets
from googleapiclient.discovery import build
import components.YoutubeHelper as yh
import components.SpotifyHelper as sh

def Authentication() -> dict():
    # Create a YouTube API object
    youtube = yh.InitializeYoutube(secrets["youtube"]["api_key"])
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

    items = {
        "youtube" : youtube,
        "spotify" : sp,
        "spotify_no_auth" : spc
    }

    return items

@st.cache_resource()
def getYoutubeToSpotifySongIDs(_youtube : object, _spc : object, yt_playlistIDs : dict) -> dict():
    '''
    Get the Spotify URIs for songs in the _youtube playlists
        
    Parameters
    ----------
    _youtube : object
        The _youtube object from the _Youtube API
    _spc : object
        The spotify object from the Spotify API
    yt_playlistIDs : dict
        The dictionary of playlist names and their IDs from _youtube

    Returns
    -------
    youtube_to_spotify_uri : dict
        The dictionary of playlist names and their IDs from _youtube
        

    Example
    --------
    >>> yt_playlistIDs = {
        "playlist 1" : "id 1",
        "playlist 2" : "id 2",
        "playlist 3" : "id 3"
    }

    >>> youtube_to_spotify_uri = getYoutubeToSpotifySongIDs(_youtube,_spc,yt_playlistIDs)
    
    youtube_to_spotify_uri = {
        "playlist 1" : ["URI 1","URI 2","URI 3"],
        "playlist 2" : ["URI 4","URI 5","URI 6"],
        "playlist 3" : ["URI 7","URI 8","URI 9"]
    }
    '''
    youtube_to_spotifiy_uri = {} 
    # for each _youtube playlist 
    for playlist_name in yt_playlistIDs.keys():
        playlist_songs = yh.returnPlaylistItems(_youtube,yt_playlistIDs[playlist_name])

        # Initialising a list for each playlist
        youtube_to_spotifiy_uri[playlist_name] = []

        for song in playlist_songs:
            # getting songID data for spotify
            song_data = sh.searchTrack(_spc, song)

            # # appeding {name : id} to the list of songs to the list with the key as playlist name in this main dict 
            # youtube_to_spotifiy_uri[playlist_name].append({song_data['track_name'] : song_data['track_id']})
            youtube_to_spotifiy_uri[playlist_name].append(song_data['track_id'])

    return youtube_to_spotifiy_uri