'''
This file contains helper functions for the Spotify API
-------------------------------------------

Functions
---------
InitializeSpotify(client_id : str, client_secret : str, redirect_uri : str, openBrowser = True) -> object
    Initializes the Spotify API
StreamlitInitializeSpotifyAuth(client_id : str, client_secret : str, redirect_uri : str) -> object
    Initializes the Spotify API for Streamlit
getAuthLink(sp_oauth : object) -> str
    Gets the authorization link for Spotify
FinalzieAuth(sp_oauth : object,auth_code  : str) -> object
    Finalizes the authorization for Spotify
InitializeSpotifyClient(client_id : str, client_secret : str) -> object
    Initializes the Spotify API for client credentials
searchTrack(sp : object, track_name : str, explicit : bool = False) -> list()
    Search for a track on Spotify
'''

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


def InitializeSpotify(client_id : str, client_secret : str, redirect_uri : str, openBrowser = True) -> object:
    '''
    Initializes the Spotify API
    Parameters
    ----------
    client_id : str
        Client ID from Spotify
    client_secret : str
        Client Secret from Spotify
    redirect_uri : str
        Redirect URI from Spotify
    openBrowser : bool, optional
        Open the browser to authenticate, by default True

    Returns
    -------
    sp : object
        Spotify API object

    Example
    -------
    >>> sp = InitializeSpotify(client_id,client_secret,redirect_uri)
    '''
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                            client_secret=client_secret,
                                            redirect_uri=redirect_uri,
                                            open_browser=openBrowser,
                                            scope='playlist-modify-public'))
    
    return sp

# Im sorry for the naming schme here
def StreamlitInitializeSpotifyAuth(client_id : str, client_secret : str, redirect_uri : str) -> object: 
    '''
    Initializes the Spotify API for Streamlit
    
    Parameters
    ----------
    client_id : str
        Client ID from Spotify
    client_secret : str
        Client Secret from Spotify
    redirect_uri : str  
        Redirect URI from Spotify

    Returns
    -------
    sp_oauth : object
        Spotify API object

    Example
    -------
    >>> sp_oauth = StreamlitInitializeSpotifyAuth(client_id,client_secret,redirect_uri)
    '''
    sp_oauth = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri,
                            scope='playlist-modify-private playlist-modify-public playlist-read-private',
                            open_browser=False)
    return sp_oauth

def getAuthLink(sp_oauth : object) -> str:
    '''
    Gets the Authorization Link for Spotify

    Parameters
    ----------
    sp_oauth : object
        Spotify API object

    Returns
    -------
    auth_url : str
        Authorization URL

    Example
    -------
    >>> auth_url = getAuthLink(sp_oauth)
    >>> print(auth_url)
    https://accounts.spotify.com/authorize?client_id=1234567890qwertyuiopasdfghjklzxcvbnm&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2F&scope=playlist-modify-private+playlist-modify-public+playlist-read-private&state=123

    '''
    auth_url = sp_oauth.get_authorize_url()
    return auth_url
    
def FinalzieAuth(sp_oauth : object, auth_code : str) -> object:
    '''
    Finalizes the authorization for Spotify

    Parameters
    ----------
    sp_oauth : object
        Spotify API object
    auth_code : str
        Authorization Code

    Returns
    -------
    sp : object
        Spotify API object

    Example
    -------
    >>> sp = FinalzieAuth(sp_oauth,auth_code)
    '''
    token_info = sp_oauth.get_access_token(auth_code)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp

def InitializeSpotifyClient(client_id : str, client_secret : str) -> object():
    '''
    Initializes the Spotify API for client credentials

    Parameters
    ----------
    client_id : str
        Client ID from Spotify
    client_secret : str
        Client Secret from Spotify

    Returns
    -------
    spc : object
        Spotify API object

    Example
    -------
    >>> spc = InitializeSpotifyClient(client_id,client_secret)
    '''
    # Authenticate using SpotifyOAuth
    spc = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                                client_secret=client_secret
                                                                ))
    return spc

def searchTrack(sp : object, track_name : str, explicit : bool = False) -> list():
    '''
    Search for a track on Spotify

    Parameters
    ----------
    sp : object
        Spotify API object
    track_name : str
        Name of the track
    explicit : bool, optional
        Return the full response, by default False

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
    track_list = sp.search(q=track_name, limit=1, offset=0, type='track', market=None)
    
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
