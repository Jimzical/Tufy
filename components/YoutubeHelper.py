from googleapiclient.discovery import build
from streamlit.runtime.caching import cache_data
import streamlit as st

@cache_data
def Initialize():
    '''
    Initializes the Youtube API

    Returns
    -------
    youtube : object
        Youtube API object
    '''
    api_key = st.secrets['api_key']
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    return youtube
def get_channel_id(youtube,channel_name : str) -> str:
    '''
    Get channel ID from channel name    


    Parameters
    ----------
    youtube : object
        Youtube API object
    channel_name : str
        Name of the channel

    Returns
    -------
    channel_id : str
        Channel ID of the channel


    '''
    req = youtube.search().list(
        part='snippet',
        q=channel_name,
        type='channel'
    )
    res = req.execute()

    channel_id = {}
    try:
        channel_id = res['items'][0]['id']['channelId']
        return channel_id
    except:
        return 'Channel not found'

def get_all_playlists(youtube, channel_id : str) -> list():
    '''
    Get all playlists created by a YouTube channel

    Parameters
    ----------
    youtube : object    
        YouTube API object
    channel_id : str    
        Channel ID of the channel

    Returns
    -------
    playlists : list
        List of playlists created by the channel
    '''
    playlists = []
    next_page_token = None

    while True:
        # Get the playlists for the specified channel with pagination
        playlists_request = youtube.playlists().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,  # Adjust as needed
            pageToken=next_page_token
        )
        playlists_response = playlists_request.execute()

        # Extract playlist information
        for playlist in playlists_response['items']:
            playlist_info = {
                'Title': playlist['snippet']['title'],
                'ID': playlist['id'],
                'Description': playlist['snippet']['description']
            }
            playlists.append(playlist_info)

        # Check if there are more playlists
        next_page_token = playlists_response.get('nextPageToken')
        if not next_page_token:
            break  # No more playlists

    return playlists


def playlistInfo(youtube,playlist_id : str) -> dict():
    '''
    Get all playlists created by a YouTube channel

    Parameters
    ----------
    youtube : object    
        YouTube API object
    playlist_id : str    
        Playlist ID of the playlist

    Returns
    -------
    response : dict
        Response of the API call
    '''
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults=50,
    )
    response = request.execute()
    
    newToken = response.get('nextPageToken')
    while newToken:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=newToken
        )
        response['items'] += request.execute()['items']
        newToken = request.execute().get('nextPageToken')
    
    return response

