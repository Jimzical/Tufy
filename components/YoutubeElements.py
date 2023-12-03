import streamlit as st
from components.YoutubeHelper import *
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
    if channel_id:
        st.caption(f"https://www.youtube.com/channel/{channel_id}")

        return channel_id

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

def choosePlaylist(playlists : list) -> str:
    # Display playlists	
    cleaned_playlists = {}
    for playlist in playlists:
        cleaned_playlists[playlist['Title']] = playlist['ID']

    # st.write(cleaned_playlists.keys())
    # Choosing the playlist
    play = st.multiselect('Select Playlist', options=cleaned_playlists.keys())
    cleaned_playlists_list = []
    for i in play:
        st.caption(f"https://www.youtube.com/playlist?list={cleaned_playlists[i]}")
        cleaned_playlists_list.append(cleaned_playlists[i])

    return cleaned_playlists_list
    # return cleaned_playlists[play]

def displayPlaylistItems(youtube,chosen_playlist : str) -> None:
    # Showing the songs in the playlist
    response = playlistInfo(youtube,chosen_playlist)
    res = response['items']

    for i in res:
        with st.expander(i['snippet']['title'],expanded=True):
            col1,col2,col3 = st.columns([4,2,2])
            col1.image(i['snippet']['thumbnails']['default']['url'])
            col2.subheader(f"{i['snippet']['title']}  -  {i['snippet']['videoOwnerChannelTitle']}")

