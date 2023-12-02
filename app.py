import streamlit as st
from googleapiclient.discovery import build
from components.YoutubeHelper import *
from components.YoutubeElements import *

def main(): 
    st.title('Youtube Channel Information')

    # Create a YouTube API object
    youtube = Initialize()
    tab1,tab2 = st.tabs(["Channel Id","Channel Name"])
    with tab1:
        thru_id = throughChannelId(youtube)
    with tab2:
        thru_name = throughChannelName(youtube)

    if thru_id:
        channel_id = thru_id
    elif thru_name:
        channel_id = thru_name

    # Get all playlists for that channel
    playlists = get_all_playlists(youtube, channel_id)

    chosen_playlist = choosePlaylist(playlists)

    # Display playlist information
    toggle_display = st.toggle('Display Playlist Items')
    if toggle_display:
        displayPlaylistItems(youtube,chosen_playlist)



if __name__ == '__main__':
    main()
