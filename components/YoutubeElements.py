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
    channel_id = st.text_input('Enter Channel ID', value='UCEXnhgo3qEjrlkDvljtf5xg')
    # using regex to check if the channel ID is valid. it can either be UCEXnhgo3qEjrlkDvljtf5xg format or https://www.youtube.com/channel/UCEXnhgo3qEjrlkDvljtf5xg format
    if re.match(r'UC[A-Za-z0-9_-]{22}', channel_id):
        st.caption(f"https://www.youtube.com/channel/{channel_id}")
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
    tab1,tab2 = st.tabs(["Channel Id","Channel Name"])
    with tab1:
        thru_id = throughChannelId(youtube)
        st.write("Channel ID:")
    with tab2:
        thru_name = throughChannelName(youtube)

    # Fix for using Tabs
    if thru_id:
        channel_id = thru_id
    if thru_name:
        channel_id = thru_name

    return channel_id

def choosePlaylist(playlists : list, chooseAll = False, testMode = False, displayLink = False) -> list:
    '''
    Create Streamlit UI to choose multiple playlist

    Parameters
    ----------
    playlists : list
        List of playlists (all playlists for a user)
    chooseAll : bool, default = False
        Has all playlists selected by default
    testMode : bool, default = False
        Only for debugging
    displayLink : bool, default = False
        To Display the link

    Returns
    -------
    playlistID_list : list
        List of all the IDs for all the playlists that are selected
    '''
    # Display playlists	
    title_id_mapping = {}
    for playlist in playlists:
        title_id_mapping[playlist['Title']] = playlist['ID']

    # Choosing the playlist
    if chooseAll:
        selected_playlists = st.multiselect('Select Playlist', options=title_id_mapping.keys(), default=list(title_id_mapping.keys()))
    elif testMode:
        selected_playlists = st.multiselect('Select Playlist', options=title_id_mapping.keys(), default=["Loop"])
    else:
        selected_playlists = st.multiselect('Select Playlist', options=title_id_mapping.keys(), default=list(title_id_mapping.keys())[0])


    
    playlistID_list = []
    for chosen_playlist in selected_playlists:
        if displayLink:
            st.caption(f"https://www.youtube.com/playlist?list={title_id_mapping[chosen_playlist]}")
        playlistID_list.append(title_id_mapping[chosen_playlist])

    return playlistID_list

def displayPlaylistItems(youtube,chosen_playlist : str) -> None:
    # Showing the songs in the playlist
    response = playlistInfo(youtube,chosen_playlist)
    res = response['items']

    for i in res:
        with st.expander(i['snippet']['title'],expanded=True):
            col1,col2,col3 = st.columns([4,2,2])
            col1.image(i['snippet']['thumbnails']['default']['url'])
            col2.subheader(f"{i['snippet']['title']}  -  {i['snippet']['videoOwnerChannelTitle']}")

def toggleDisplayPlaylistItems(youtube,chosen_playlistID_options : list, id_title_mapping : dict) -> None:
    toggle_youtube_display = st.toggle('Display Playlist Items')
    if toggle_youtube_display:
        total_songs = 0
        for chosen_playlistID in chosen_playlistID_options:
            with st.status(f"Gettting Info for {id_title_mapping[chosen_playlistID]}",expanded=True) as status:
                st.subheader(f"Playlist: {id_title_mapping[chosen_playlistID]}")
                playlist_songs = returnPlaylistItems(youtube,chosen_playlistID)
                st.write(playlist_songs)
                st.write(len(playlist_songs))
                total_songs += len(playlist_songs)
            status.update(label="Got all Info", state="complete",expanded=True)
        st.title(f"`Total Number of Songs ➡️ {total_songs}`")
    