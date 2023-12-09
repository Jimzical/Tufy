'''
This file contains all the functions that are used to create the Streamlit UI for the Youtube section
'''

import streamlit as st
from components.YoutubeHelper import *
import re
def throughChannelId(youtube) -> str:
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
    # using regex to check if the channel ID is valid. it can either be UCEXnhgo3qEjrlkDvljtf5xg format or https://www.youtube.com/channel/UCEXnhgo3qEjrlkDvljtf5xg format
    if re.match(r'UC[A-Za-z0-9_-]{22}', channel_id):
        st.caption(f"https://www.youtube.com/channel/{channel_id}",help = "You Can Click the Link to Verify the Channel")
        return channel_id

    elif re.match(r'https://www.youtube.com/channel/UC[A-Za-z0-9_-]{22}', channel_id):
        channel_id = channel_id[32:]
        st.caption(f"https://www.youtube.com/channel/{channel_id}")

        return channel_id

    else:
        raise ValueError("Invalid Channel ID")
def throughChannelName(youtube):
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

def chooseChannel(youtube) -> str:
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
    # tab1,tab2 = st.tabs(["Channel Id","Channel Name"])
    # with tab1:
    #     thru_id = throughChannelId(youtube)
    #     st.write("Channel ID:")
    # with tab2:
    #     thru_name = throughChannelName(youtube)

    # # Fix for using Tabs
    # if thru_id:
    #     channel_id = thru_id
    # if thru_name:
    #     channel_id = thru_name

    # return channel_id

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

    
    # playlistID_list = []
    # for chosen_playlist in selected_playlists:
    #     if displayLink:
    #         st.caption(f"https://www.youtube.com/playlist?list={title_id_mapping[chosen_playlist]}")
    #     playlistID_list.append(title_id_mapping[chosen_playlist])

    # return playlistID_list





def displayPlaylistItems(youtube,yt_chosen_playlistIDs : dict) -> None:
    for chosen_playlistID in yt_chosen_playlistIDs.keys():
        # Showing the songs in the playlist
        response = playlistInfo(youtube,yt_chosen_playlistIDs[chosen_playlistID])
        res = response['items']

        st.subheader(f"Playlist: {chosen_playlistID}")
        for i in res:
            with st.expander(i['snippet']['title'],expanded=False):
                col1,col2,col3 = st.columns([1.5,2,2])
                # col1.markdown(f'<img src="{i["snippet"]["thumbnails"]["default"]["url"]}" alt="Thumbnail" style="max-width:100%;">', unsafe_allow_html=True)
                col1.image(i['snippet']['thumbnails']['default']['url'], use_column_width=True)
                col2.write(f"{i['snippet']['title']}")
                col3.write(f"by  {i['snippet']['videoOwnerChannelTitle']}")

def toggleDisplayPlaylistItems(youtube,chosen_playlistIDs : dict) -> None:
    
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
    