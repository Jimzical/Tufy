'''
This file contains all the functions that are used to create the Streamlit UI for the Youtube section

Future Updates:
    - Change { from components.YoutubeHelper import * } to { import components.YoutubeHelper as yh }        
'''

import streamlit as st
from components.YoutubeHelper import *
import re
def throughChannelId(youtube : object) -> str:
    '''
    Create the Streamlit UI for entering the channel ID

    Parameters
    ----------
    youtube : object
        Youtube API object

    Returns
    -------
    channel_id : str
        Channel ID of the channel
    '''
    channel_id = st.text_input('Enter Channel ID', value='UCPKlrgZXnnb89nSeITvTdGA')
    # channel_id = st.text_input('Enter Channel ID', value='UCEXnhgo3qEjrlkDvljtf5xg')

    # using regex to check if the channel ID is valid. it can either be UCPKlrgZXnnb89nSeITvTdGA format or https://www.youtube.com/channel/UCPKlrgZXnnb89nSeITvTdGA format
    if re.match(r'UC[A-Za-z0-9_-]{22}', channel_id):
        st.caption(f"https://www.youtube.com/channel/{channel_id}",help = "You Can Click the Link to Verify the Channel")
        return channel_id

    elif re.match(r'https://www.youtube.com/channel/UC[A-Za-z0-9_-]{22}', channel_id):
        channel_id = channel_id[32:]
        st.caption(f"https://www.youtube.com/channel/{channel_id}")

        return channel_id

    else:
        raise ValueError("Invalid Channel ID")
def throughChannelName(youtube : object):
    '''
    Create the Streamlit UI for entering the channel name

    Parameters
    ----------
    youtube : object
        Youtube API object

    Returns
    -------
    channel_id : str
        Channel ID of the channel
    '''
    textbox, channelbutton = st.columns([4,1])

    with textbox:
        channel_name = st.text_input('Enter Channel Name')
    with channelbutton:
        st.write("")
        st.write("")
        channelbutton = st.button('Get Channel ID')
    if channelbutton:
        # Get channel ID
        channel_id = get_channel_id(youtube, channel_name)
        st.write("Channel ID:")
        # make a link to the channel
        st.markdown(f"https://www.youtube.com/channel/{channel_id}")
        return channel_id

def chooseChannel(youtube : object) -> str:
    '''
    Create the Streamlit UI to get the channel ID

    Parameters
    ----------
    youtube : object
        Youtube API object

    Returns
    -------
    channel_id : str
        Channel ID of the channel
    '''
    channel_id =throughChannelId(youtube)
    return channel_id

def choosePlaylist(playlists : list, testMode = False) -> dict:
    '''
    Create Streamlit UI to choose multiple playlist

    Parameters
    ----------
    playlists : list
        List of playlists (all playlists for a user)
    testMode : bool, default = False
        Only for debugging

    Returns
    -------
    playlistID_dict : dict
        Dictionary of playlist ID and playlist title

    Examples
    --------
    >>> yt_playlistIDs = choosePlaylist(playlists, testMode = False)
    {
        "playlist_title 1" : "playlist_id 1",
        "playlist_title 2" : "playlist_id 2",
        "playlist_title 3" : "playlist_id 3",
    }
    '''
    # Display playlists	
    title_id_mapping = {}
    for playlist in playlists:
        title_id_mapping[playlist['Title']] = playlist['ID']

    # Choosing the playlist
    if testMode:
        selected_playlists = st.multiselect('Select Playlist', options=title_id_mapping.keys(), default=["Loop"])
    else:
        selected_playlists = st.multiselect('Select Playlist', options=title_id_mapping.keys(), default=list(title_id_mapping.keys())[-1])

    playlistID_dict = {}
    # for all the selected playlists, get the playlist ID
    for chosen_playlist in selected_playlists:
        playlistID_dict[chosen_playlist] = title_id_mapping[chosen_playlist]

    return playlistID_dict


def displayPlaylistItems(youtube : object, yt_chosen_playlistIDs : dict) -> None:
    '''
    Create Streamlit UI to display the playlist items

    Parameters
    ----------
    youtube : object
        Youtube API object
    yt_chosen_playlistIDs : dict
        Dictionary of playlist ID and playlist title

    Examples
    --------
    >>> yt_playlistIDs = {
        "playlist 1" : "id 1",
        "playlist 2" : "id 2",
        "playlist 3" : "id 3"
    }

    >>> displayPlaylistItems(youtube, yt_playlistIDs)
    '''
    for chosen_playlistID in yt_chosen_playlistIDs.keys():
        # Showing the songs in the playlist
        response = playlistInfo(youtube,yt_chosen_playlistIDs[chosen_playlistID])
        res = response['items']

        st.subheader(f"Playlist: {chosen_playlistID}")
        for i in res:
            with st.expander(i['snippet']['title'],expanded=False):
                col1,col2,col3 = st.columns([1.5,2,2])
                # col1.markdown(f'<img src="{i["snippet"]["thumbnails"]["default"]["url"]}" alt="Thumbnail" style="max-width:100%;">', unsafe_allow_html=True)
                try:
                    col1.image(i['snippet']['thumbnails']['default']['url'], use_column_width=True)
                except:
                    col1.info("No Thumbnail")
                col2.write(f"{i['snippet']['title']}")
                try:
                    col3.write(f"by  {i['snippet']['videoOwnerChannelTitle']}")
                except:
                    col3.info("No Channel Name")
# Was a test feature
def toggleDisplayPlaylistItems(youtube : object, chosen_playlistIDs : dict) -> None:
    '''
    Create Streamlit UI to toggle the display of the playlist items

    Parameters
    ----------
    youtube : object
        Youtube API object
    chosen_playlistIDs : dict
        Dictionary of playlist ID and playlist title

    Examples
    --------
    >>> yt_playlistIDs = {
        "playlist 1" : "id 1",
        "playlist 2" : "id 2",
        "playlist 3" : "id 3"
    }

    >>> toggleDisplayPlaylistItems(youtube, yt_playlistIDs)
    '''
    toggle_youtube_display = st.toggle('Display Playlist Items')
    
    if toggle_youtube_display:
        total_songs = 0
    
        for chosen_playlistname in chosen_playlistIDs.keys():
            with st.status(f"Gettting Info for {chosen_playlistname}",expanded=True) as status:
                st.subheader(f"Playlist: {chosen_playlistname}")
                playlist_songs = returnPlaylistItems(youtube,chosen_playlistIDs[chosen_playlistname])
                st.write(playlist_songs)
                st.write(len(playlist_songs))
                total_songs += len(playlist_songs)
            status.update(label="Got all Info", state="complete",expanded=True)
        st.title(f"`Total Number of Songs ➡️ {total_songs}`")
    

def youtubeData(youtube : object) -> None:
    '''
    Create Streamlit UI to get the Youtube data

    Parameters
    ----------
    youtube : object
        Youtube API object

    Returns
    -------
    yt_chosen_playlistIDs : dict
        Dictionary of playlist ID and playlist title

    Examples
    --------
    >>> yt_playlistIDs = youtubeData(youtube)
    {
        "playlist_title 1" : "playlist_id 1",
        "playlist_title 2" : "playlist_id 2",
        "playlist_title 3" : "playlist_id 3",
    }
    '''

    yt_channel_id = chooseChannel(youtube)

    # Get all yt_channel_playlists for that channel
    try:
        yt_channel_playlists = get_all_playlists(youtube, yt_channel_id)
    except:
        st.error("No Playlists Found")
        return

    yt_chosen_playlistIDs = choosePlaylist(yt_channel_playlists, testMode=False)

    return yt_chosen_playlistIDs

def youtubeDisplayElements(youtube, yt_chosen_playlistIDs : dict) -> None:
    '''
    Create Streamlit UI for displaying the Youtube information

    Parameters
    ----------
    youtube : object
        Youtube API object
    yt_chosen_playlistIDs : dict
        Dictionary of playlist ID and playlist title

    Examples
    --------
    >>> yt_playlistIDs = {
        "playlist 1" : "id 1",
        "playlist 2" : "id 2",
        "playlist 3" : "id 3"
    }

    >>> youtubeDisplayElements(youtube, yt_playlistIDs)
    '''
    if st.toggle("Display Youtube Results"):
        with st.container(border=True):
            displayPlaylistItems(youtube,yt_chosen_playlistIDs) 
