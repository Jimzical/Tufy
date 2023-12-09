
import streamlit as st
from streamlit import secrets
from googleapiclient.discovery import build
from components.helper_components import ColoredHeader, Notif
import components.YoutubeHelper as yh
import components.YoutubeElements as ye
import components.SpotifyHelper as sh
import components.SpotifyElements as se
import components.YoutubeToSpotify as yts

def main(): 
    ColoredHeader('Youtube Channel Information',anchor=False)


    #  ----------------------------------------------------------------------
    # ------------------------------ Authentication -------------------------
    # ----------------------------------------------------------------------

    # Create a YouTube API object
    youtube = yh.InitializeYoutube()
    sp_oauth = sh.StreamlitInitializeSpotifyAuth(
        client_id = secrets["spotify"]["client_id"],
        client_secret = secrets["spotify"]["client_secret"],
        redirect_uri = secrets["spotify"]["redirect_uri"]
    )
    auth_url = sh.getAuthLink(sp_oauth)
    auth_link = st.empty()
    auth_link.markdown(f"Click [here]({auth_url}) to authorize the app.")
    try:
        auth_code = st.experimental_get_query_params()["code"]
    except:
        st.info("Please Click the Link to Choose your Account")
        return

    sp = sh.FinalzieAuth(sp_oauth=sp_oauth,auth_code=auth_code)
   
    auth_link.empty()

    spc = sh.InitializeSpotifyClient(
            client_id = secrets["spotify"]["client_id"],
            client_secret = secrets["spotify"]["client_secret"],
    )
    
    # ----------------------------------------------------------------------
    # ------------------------------ Youtube -------------------------------
    # ----------------------------------------------------------------------


    yt_channel_id = ye.chooseChannel(youtube)

    # Get all yt_channel_playlists for that channel
    try:
        yt_channel_playlists = yh.get_all_playlists(youtube, yt_channel_id)
    except:
        st.error("No Playlists Found")
        return

    yt_chosen_playlistIDs = ye.choosePlaylist(yt_channel_playlists, testMode=False)

    # Youtube Display Stuff
    if st.toggle("Display Youtube Results"):
        # stuff = st.contr
        with st.container(border=True):
            ye.displayPlaylistItems(youtube,yt_chosen_playlistIDs) 

    # ----------------------------------------------------------------------
    # ------------------------------ Spotify -------------------------------
    # ----------------------------------------------------------------------

    # # Spotify Stuff
    # toggle_spotify_display = st.toggle("Display Spotify Results")
    # if toggle_spotify_display:
    #     yt_to_sp_songIDs = se.getYoutubeToSpotifySongIDs(youtube,spc,yt_chosen_playlistIDs)
    

    with st.sidebar:
        ColoredHeader("Start Creating Playlist!")
        me = sp.current_user()

        # Get current user's yt_channel_playlists
        sp_user_playlists = sp.current_user_playlists()
        
        sp_userPlaylistsName_list = [sp_playlist["name"] for sp_playlist in sp_user_playlists["items"]]
        sp_userPlaylist_to_uri_dict = {sp_playlist["name"]: sp_playlist["id"] for sp_playlist in sp_user_playlists["items"]}
    
        sp_add_songs = st.button("Add Songs",help="Add songs to your Spotify Playlist",use_container_width=True)
        if sp_add_songs:
            # CREATING PLAYLIST IF THEY DONT EXIST
            for playlist_name in yt_chosen_playlistIDs.keys():

                # if exists, skip
                if playlist_name in sp_userPlaylistsName_list:
                    st.toast(f"Playlist {playlist_name} already exists")
                else:
                    sp.user_playlist_create(
                        user=me["id"],
                        name=playlist_name
                    )
                    st.toast(f"Added Spotify Playlist called {playlist_name}")
            
            Notif(message = "Created all Necessary Playlist!")

            # GETTING SPOTIFY URIs
            with st.status("Getting Spotify URIs",expanded=False) as status:
                st.caption("This may take a while...")
                yt_sp_songURIs = yts.getYoutubeToSpotifySongIDs(youtube,spc,yt_chosen_playlistIDs)
                status.update(label="Got all Info", state="complete",expanded=False)


            # ADDING SONGS TO PLAYLIST    
            with st.status("Adding Songs",expanded=True) as status:
                for playlist_name in yt_chosen_playlistIDs:
                    st.write(f"Adding songs to `{playlist_name}` playlist")
                    sp.playlist_add_items(
                        playlist_id=sp_userPlaylist_to_uri_dict[playlist_name],
                        items=yt_sp_songURIs[playlist_name]
                    )                    

                status.update(label="Added Songs", state="complete",expanded=False)

if __name__ == '__main__':
    main()
