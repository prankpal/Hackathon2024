import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Create a Spotify instance using an existing access token
def create_spotify_instance(token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp

# Function to get user's playlists and analyze them
def analyze_user_playlists(sp, skipped_tracks):
    """
    Analyze user playlists to find out which playlists contain the most skipped tracks.
    
    :param sp: A Spotipy Spotify instance, authenticated with the user's token
    :param skipped_tracks: A dictionary of skipped tracks with artist and track information
    :return: A list of dictionaries containing playlist info and tracks to be removed
    """
    results = []
    playlists = sp.current_user_playlists(limit=50)  # Get user playlists (adjust the limit as needed)

    # Iterate over each playlist
    for playlist in playlists['items']:
        playlist_id = playlist['id']
        playlist_name = playlist['name']
        playlist_tracks = sp.playlist_tracks(playlist_id, fields='items(track(name,artists(id,name),id))', limit=100)
        tracks_to_remove = []

        for item in playlist_tracks['items']:
            track = item['track']
            if not track:
                continue

            artist_name = track['artists'][0]['name']
            track_name = track['name']
            track_id = f"{artist_name} - {track_name}"

            # Check if the track is in the skipped tracks list
            if track_id in skipped_tracks:
                tracks_to_remove.append({
                    'artist': artist_name,
                    'track': track_name,
                    'track_id': track['id'],
                    'count': skipped_tracks[track_id]['count']
                })

        # Append the analysis result for this playlist
        if tracks_to_remove:
            results.append({
                'playlist_name': playlist_name,
                'playlist_id': playlist_id,
                'tracks_to_remove': tracks_to_remove
            })

    return results
