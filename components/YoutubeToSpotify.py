import streamlit as st
import concurrent.futures
import components.YoutubeHelper as yh
import components.SpotifyHelper as sh

def Authentication() -> dict():
    # Create a YouTube API object
    youtube = yh.InitializeYoutube(st.secrets["youtube"]["api_key"])
    sp_oauth = sh.StreamlitInitializeSpotifyAuth(
        client_id = st.secrets["spotify"]["client_id"],
        client_secret = st.secrets["spotify"]["client_secret"],
        redirect_uri = st.secrets["spotify"]["redirect_uri"]
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
            client_id = st.secrets["spotify"]["client_id"],
            client_secret = st.secrets["spotify"]["client_secret"],
    )

    items = {
        "youtube" : youtube,
        "spotify" : sp,
        "spotify_no_auth" : spc
    }

    return items

# Function to get all the playlists from a channel wihtout multithreading
# @st.cache_resource()
def getYoutubeToSpotifySongIDs(_youtube: object, _spc: object, yt_playlistIDs: dict, streamlitMode=False) -> dict:
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
    streamlitMode : bool, optional
        Flag to indicate whether Streamlit mode is enabled, by default False

    Returns
    -------
    youtube_to_spotify_uri : dict
        The dictionary of playlist names and their IDs from _youtube
    '''

    youtube_to_spotifiy_uri = {} 
    # for each _youtube playlist 
    for playlist_name in yt_playlistIDs.keys():
        playlist_songs = yh.returnPlaylistItems(_youtube, yt_playlistIDs[playlist_name])

        # Initializing a list for each playlist
        youtube_to_spotifiy_uri[playlist_name] = []

        if streamlitMode:
            st.write(playlist_name)
            progress_bar = st.progress(0)  # Create a progress bar

        for i, song in enumerate(playlist_songs):
            # getting songID data for spotify
            song_data = sh.searchTrack(_spc, song)

            # Append song_id to the list with the key as playlist name in this main dict 
            youtube_to_spotifiy_uri[playlist_name].append(song_data['track_id'])

            if streamlitMode:
                # Update the progress bar
                progress_percent = (i + 1) / len(playlist_songs)
                progress_bar.progress(progress_percent)

        if streamlitMode:
            # Show the final progress as 100%
            progress_bar.progress(1.0)

    if streamlitMode:
        # Print the resulting dictionary
        st.write(youtube_to_spotifiy_uri)

    return youtube_to_spotifiy_uri# Function to get Spotify URIs for a playlist
def get_playlist_uris(youtube, spc, playlist_name, playlist_id):
    '''
    Get the Spotify URIs for songs in the youtube playlists

    Parameters
    ----------
    youtube : object
        The youtube object from the Youtube API
    spc : object
        The spotify object from the Spotify API
    playlist_name : str
        Name of the playlist
    playlist_id : str
        ID of the playlist  

    Returns
    -------
    playlist_name : str
        Name of the playlist
    uri_list : list
        List of Spotify URIs for the songs in the playlist

    Example
    --------
    >>> playlist_name, uri_list = get_playlist_uris(youtube, spc, playlist_name, playlist_id)

    >>> playlist_name
    'Playlist 1'

    >>> uri_list
    ['URI 1','URI 2','URI 3']

    '''
    playlist_songs = yh.returnPlaylistItems(youtube, playlist_id)
    uri_list = []

    for song in playlist_songs:
        song_data = sh.searchTrack(spc, song)
        uri_list.append(song_data['track_id'])

    return playlist_name, uri_list

# Function to get all Spotify URIs using multithreading
@st.cache_resource()
def get_youtube_to_spotify_song_ids(_youtube, _spc, yt_playlist_ids):
    youtube_to_spotify_uri = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks for each playlist
        future_to_playlist = {executor.submit(get_playlist_uris, _youtube, _spc, playlist_name, playlist_id): playlist_name
                              for playlist_name, playlist_id in yt_playlist_ids.items()}

        for future in concurrent.futures.as_completed(future_to_playlist):
            playlist_name = future_to_playlist[future]
            try:
                result = future.result()
                youtube_to_spotify_uri[result[0]] = result[1]
            except Exception as e:
                st.error(f"An error occurred while processing playlist {playlist_name}: {str(e)}")

    return youtube_to_spotify_uri