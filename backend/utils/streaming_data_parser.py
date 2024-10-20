import json

THRESHOLD = 3000  # Time in milliseconds to determine a 'skip'

def parse_skipped_tracks(streaming_data):
    # Parse skipped tracks from streaming data
    skipped_tracks = {}
    for item in streaming_data:
        if item['msPlayed'] < THRESHOLD:
            track_id = f"{item['artistName']} - {item['trackName']}"
            if track_id in skipped_tracks:
                skipped_tracks[track_id]['count'] += 1
            else:
                skipped_tracks[track_id] = {
                    'artist': item['artistName'],
                    'track': item['trackName'],
                    'count': 1
                }
    return skipped_tracks

def analyze_streaming_data(file_path):
    # Load the streaming history from a JSON file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            streaming_data = json.load(f)
    except Exception as e:
        print(f"Error reading streaming data file: {str(e)}")
        return None

    # Parse the streaming data to identify skipped tracks
    skipped_tracks = parse_skipped_tracks(streaming_data)

    # Sort skipped tracks by count
    sorted_skipped_tracks = sorted(skipped_tracks.values(), key=lambda x: x['count'], reverse=True)

    # Return the sorted list of skipped tracks
    return sorted_skipped_tracks
