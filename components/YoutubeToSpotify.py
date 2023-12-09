from components.YoutubeHelper import returnPlaylistItems
from components.SpotifyHelper import searchTrack

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
        "playlist 1" : ["URI 1","URI 2","URI 3"],
        "playlist 2" : ["URI 4","URI 5","URI 6"],
        "playlist 3" : ["URI 7","URI 8","URI 9"]
    }
    '''
    youtube_to_spotifiy_uri = {} 
    # for each youtube playlist 
    for playlist_name in yt_playlistIDs.keys():
        playlist_songs = returnPlaylistItems(youtube,yt_playlistIDs[playlist_name])

        # Initialising a list for each playlist
        youtube_to_spotifiy_uri[playlist_name] = []

        for song in playlist_songs:
            # getting songID data for spotify
            song_data = searchTrack(spc, song)

            # # appeding {name : id} to the list of songs to the list with the key as playlist name in this main dict 
            # youtube_to_spotifiy_uri[playlist_name].append({song_data['track_name'] : song_data['track_id']})
            youtube_to_spotifiy_uri[playlist_name].append(song_data['track_id'])

    return youtube_to_spotifiy_uri