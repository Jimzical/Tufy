import streamlit as st
from googleapiclient.discovery import build
from streamlit.runtime.caching import cache_data

@cache_data
def Initialize():
    '''
    --------------------------------------------
    initializes the API
    --------------------------------------------
    '''
    api_key = st.secrets['api_key']
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    return youtube
def get_channel_id(youtube,channel_name):
    '''
    --------------------------------------------
    prints the channel ID
    --------------------------------------------
    params
    @youtube: youtube object
    @channel_name: name of the channel
    '''
    # using https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={CHANNEL_NAME}&type=channel&key={YOUTUBE_API_KEY}
    req = youtube.search().list(
        part='snippet',
        q=channel_name,
        type='channel'
    )
    res = req.execute()

    respones_json = {}
    try:
        respones_json = res['items'][0]['id']['channelId']
        return respones_json
    except:
        return 'Channel not found'


def get_all_playlists(youtube, channel_id):
    '''
    --------------------------------------------
    Get all playlists created by a YouTube channel
    --------------------------------------------
    '''
    playlists = []
    # Get the playlists for the specified channel
    playlists_request = youtube.playlists().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50  # Adjust as needed
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

    return playlists

def throughChannelId(youtube):
    channel_id = st.text_input('Enter Channel ID', value='UCEXnhgo3qEjrlkDvljtf5xg')
    if channel_id:
        st.markdown(f"https://www.youtube.com/channel/{channel_id}")

        return channel_id

def throughChannelName(youtube):
    channel_name = st.text_input('Enter Channel Name')
    if channel_name:
        # Get channel ID
        channel_id = get_channel_id(youtube, channel_name)
        st.write("Channel ID:")
        # make a link to the channel
        st.markdown(f"https://www.youtube.com/channel/{channel_id}")
        return channel_id


def main(): 
    st.title('Youtube Channel Information')
    youtube = Initialize()
    # tab1,tab2 = st.tabs(["Channel Id","Channel Name"])
    # with tab1:
    #     channel_id = throughChannelId(youtube)
    #     st.write("Channel ID:")
    #     st.write(channel_id)

    # with tab2:
    #     channel_id = throughChannelName(youtube)

    channel_id = throughChannelId(youtube)
    if not channel_id:
        st.error("Channel not found")
        return
    
    # Get all playlists
    playlists = get_all_playlists(youtube, channel_id)
    st.subheader("Playlists:")
    st.write(playlists)

if __name__ == '__main__':
    main()
