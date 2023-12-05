import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


# Having issues with streamlit constantly opening tabs for some reason

# GOT THE ANSWER
# ITS DUE TO playlist-modify-public, when tbhis is added to scope the app goes crazy 
# playlist-read-private 
def InitializeSpotify(client_id,client_secret,redirect_uri,openBrowser = True):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                            client_secret=client_secret,
                                            redirect_uri=redirect_uri,
                                            open_browser=openBrowser,
                                            scope='playlist-modify-public'))
    
    return sp

# Im sorry for the naming schme here
def StreamlitInitializeSpotifyAuth(client_id,client_secret,redirect_uri): 
    sp_oauth = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri,
                            scope='playlist-modify-private playlist-modify-public playlist-read-private',
                            open_browser=False)
    return sp_oauth


def getAuthLink(sp_oauth):
        auth_url = sp_oauth.get_authorize_url()
        return auth_url
    
def FinalzieAuth(sp_oauth,auth_code):
    token_info = sp_oauth.get_access_token(auth_code)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp


def InitializeSpotifyClient(client_id,client_secret):
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