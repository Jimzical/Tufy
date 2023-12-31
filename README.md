# TUFY

A Web Application to Convert Playlists from a YouTube Channel to Spotify Playlists.

## Getting Started

### Prerequisites
> Python 3.9 or higher

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/Jimzical/Tufy.git
    ```

2. Install requirements
    ```sh
    pip install -r requirements.txt
    ```
3. Add the API keys to `secrets.toml`
    > You can get your YouTube API Key from [here](https://console.developers.google.com/apis/credentials) and your Spotify Client ID and Secret from [here](https://developer.spotify.com/dashboard/applications).

4. Run the app
    ```sh
    streamlit run app.py
    ```

## Usage
Choose between `Channel` or `Playlist`
- `Channel` - Convert Playlists from a YouTube Channel
    1. Enter the YouTube Channel ID
        - To get your `Own Channel ID`
            - Go to your Channel and copy the ID from the URL
            > Example: https://www.youtube.com/channel/UCPKlrgZXnnb89nSeITvTdGA
            </br>
            Your channel ID is `UCPKlrgZXnnb89nSeITvTdGA`
        - To get `Another Channel's ID`
            - Go to their `About page` 
            - Click on the `Share` Button
            - Click on the `Copy Channel ID` Button
    2. Select the `Playlists` you want to Convert
- `Playlist` - Convert a Single YouTube Playlist
    1. Enter the YouTube Playlist ID
        - To get a `Playlist ID`
            - Go to the Playlist and copy the ID from the URL
            > Example: https://www.youtube.com/playlist?list=PL4o29bINVT4EG_y-k5jGoOu3-Am8Nvi10
            </br>
            Your Playlist ID is `PL4o29bINVT4EG_y-k5jGoOu3-Am8Nvi10`
 -  Click the `Add Songs` Button


## Updates
- Fixed Progress Bar

## Future Updates
- Deploy Website



## Contact
Github: https://github.com/Jimzical
</br>
Project Link: https://github.com/Jimzical/Tufy
