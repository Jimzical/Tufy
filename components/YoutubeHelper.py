'''
This Module contains all the functions required to interact with the Youtube API
-------------------------------------------

Functions
---------
InitializeYoutube() -> youtube : object
    Initializes the Youtube API
get_channel_id(youtube,channel_name : str) -> str
    Get channel ID from channel name
get_all_playlists(youtube, channel_id : str) -> list()
    Get info on all the playlists created by a YouTube channel
playlistInfo(youtube,playlist_id : str) -> dict()
    Get all the info for a playlist
returnPlaylistItems(youtube,playlistID : str) -> list()
    Get all the songs in a playlist

'''

from googleapiclient.discovery import build

def InitializeYoutube(api_key : str) -> object:
    '''
    Initializes the Youtube API

    Returns
    -------
    youtube : object
        Youtube API object
    '''
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    return youtube
def get_channel_id(youtube : object, channel_name : str) -> str:
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

    Examples
    --------
    >>> get_channel_id(youtube, 'Google')
    UC_x5XG1OV2P6uZZ5FSM9Ttw

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

def get_all_playlists(youtube : object, channel_id : str) -> list():
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

    Examples
    --------
    >>> get_all_playlists(youtube, 'UC_x5XG1OV2P6uZZ5FSM9Ttw')
    [
        {   'Title': 'Playlist 1',
            'ID': 'PLx0sYbCqOb8TBPRdmBHs5Iftvv9TPboYG',
            'Description': 'Playlist 1 Description'
        },
        {   'Title': 'Playlist 2',
            'ID': 'PLx0sYbCqOb8Tb2nvn6Ol5_F-48ruhwPJf',
            'Description': 'Playlist 2 Description'
        }
    ]

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

    if playlists:
        return playlists
    else:
        raise Exception('No playlists found')

def playlistInfo(youtube : object, playlist_id : str) -> dict():
    '''
    Get all the info for a playlist

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

    Examples
    --------
    >>> playlistInfo(youtube, 'PLx0sYbCqOb8TBPRdmBHs5Iftvv9TPboYG')
    {
        'kind': 'youtube#playlistItemListResponse',
        'etag': '...',
        'nextPageToken': '...',
        'items': [
            {
                'kind': 'youtube#playlistItem',
                'etag': '...',
                'id': '...',
                'snippet': {
                    'publishedAt': '...',
                    'channelId': '...',
                    'title': '...',
                    'description': '...',
                    'thumbnails': {
                        'default': {
                            'url': '...',
                            'width': 120,
                            'height': 90
                        },
                        'medium': {
                            'url': '...',
                            'width': 320,
                            'height': 180
                        },
                        'high': {
                            'url': '...',
                            'width': 480,
                            'height': 360
                        },
                        'standard': {
                            'url': '...',
                            'width': 640,
                            'height': 480
                        },
                        'maxres': {
                            'url': '...',
                            'width': 1280,
                            'height': 720
                        }
                    },
                    'channelTitle': '...',
                    'playlistId': '...',
                    'position': 0,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': '...'
                    }
                },
                'contentDetails': {
                    'videoId': '...',
                    'videoPublishedAt': '...'
                }
            }
        ]
    }
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

def returnPlaylistItems(youtube : object, playlistID : str) -> list():
    '''
    Get all playlists created by a YouTube channel

    Parameters
    ----------
    youtube : object    
        YouTube API object
    playlistID : str
        Playlist ID of the playlist

    Returns
    -------
    playlist_items : list
        List of all the songs in the playlist

    Examples
    --------
    >>> returnPlaylistItems(youtube, playlistID)
    [
        'Song 1 by Artist 1 - Description',
        'Song 2 - Description', # Incase Song is but youtube's autogenerated channels
        'Song 3 by Artist 3 - Description'
    ]
    '''
    playlist_info = playlistInfo(youtube, playlistID)
    items = playlist_info.get('items', [])

    playlist_items = []

    for item in items:
        snippet = item.get('snippet', {})
        title = snippet.get('title', '')
        owner_channel = snippet.get('videoOwnerChannelTitle', '')
        description = snippet.get('description', '').strip().replace("\n", "  ")[:100]

        if title not in ['Private video', 'Deleted video']:
            playlist_items.append(f"{title} by {owner_channel} - {description}")

    return playlist_items