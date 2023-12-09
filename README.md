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
2. Select the playlists you want to convert
3. Click the `Add Songs` button


## Future Updates
- Put all functions in their respective files
- Clean up code
- Deploy Website



## Contact
Project Link: https://github.com/Jimzical/Tufy