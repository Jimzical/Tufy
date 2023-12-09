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
3. Create `.streamlit/secrets.toml`
    ```sh
    mkdir .streamlit
    touch .streamlit/secrets.toml
    ```

4. Add the following to `secrets.toml`
    ```toml
    [youtube]
    api_key = "YOUTUBE API KEY"

    [spotify]
    client_id = "SPOTIFY CLIENT ID"
    client_secret = "SPOTIFY CLIENT SECRET"
    redirect_uri = "http://localhost:8501/"
    ```
    > You can get your YouTube API Key [here](https://console.developers.google.com/apis/credentials) and your Spotify Client ID and Secret [here](https://developer.spotify.com/dashboard/applications).

5. Run the app
    ```sh
    streamlit run app.py
    ```

## Usage
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
3. Click the `Add Songs` Button


## Future Updates
- Put all functions in their respective files
- Clean up code
- Deploy Website



## Contact
Project Link: https://github.com/Jimzical/Tufy