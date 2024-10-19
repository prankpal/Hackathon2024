import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="YOUR_CLIENT_ID",
                                               client_secret="YOUR_CLIENT_SECRET",
                                               redirect_uri="YOUR_REDIRECT_URI",
                                               scope="user-library-modify,playlist-modify-public,playlist-modify-private"))

def remove_tracks_from_spotify(tracks):
    for item in tracks:
        search_result = sp.search(q=f"artist:{item['artist']} track:{item['track']}", type='track', limit=1)
        if search_result['tracks']['items']:
            track_id = search_result['tracks']['items'][0]['id']
            sp.current_user_saved_tracks_delete([track_id])
