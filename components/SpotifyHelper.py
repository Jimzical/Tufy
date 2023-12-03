import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from streamlit import secrets 

def InitializeSpotify():
    # Set your Spotify API credentials
    client_id = secrets["spotify"]["client_id"]
    client_secret = secrets["spotify"]["client_secret"]
    redirect_uri = secrets["spotify"]["redirect_uri"]

    # Authenticate using SpotifyOAuth
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope='user-library-read playlist-read-private'))

    return sp

def InitializeSpotifyClient():
    client_id = secrets["spotify"]["client_id"]
    client_secret = secrets["spotify"]["client_secret"]
    redirect_uri = secrets["spotify"]["redirect_uri"]

    # Authenticate using SpotifyOAuth
    spc = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                                client_secret=client_secret
                                                                ))
    return spc
    

def searchTrack(sp, track_name : str, explicit : bool = False) -> list():
    '''
    Search for a track on Spotify

    Parameters
    ----------
    sp : object
        Spotify API object
    track_name : str
        Name of the track

    Returns
    -------
    track_list : list()
        List of tracks matching the search query 

    Example
    ------- 
    >>> searchTrack(sp, "Dynamite") 
     {
         "track_name" : "Dynamite",
         "track_id" : "0t1kP63rueHleOhQkYSXFY",
         "track_artist" : "BTS",
         "track_artist_id" : "3Nrfpe0tUJi4K4DXYWgMUX",
         "track_album" : "Dynamite (DayTime Version)",
     }
    '''
    track_list = sp.search(q=track_name, limit=10, offset=0, type='track', market=None)
    
    if explicit:
        return track_list
    
    response = {
        "track_name" : track_list['tracks']['items'][0]['name'],
        "track_id" : track_list['tracks']['items'][0]['id'],
        "track_artist" : track_list['tracks']['items'][0]['artists'][0]['name'],
        "track_artist_id" : track_list['tracks']['items'][0]['artists'][0]['id'],
        "track_album" : track_list['tracks']['items'][0]['album']['name'],
        "track_album_id" : track_list['tracks']['items'][0]['album']['id'],
        "track_url" : track_list['tracks']['items'][0]['external_urls']['spotify'],
    }

    return response