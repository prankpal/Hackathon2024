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

def analyze_streaming_data(json_files):
    # Consolidate all streaming data from multiple JSON files
    all_streaming_data = []
    try:
        for json_file in json_files:
            streaming_data = json.load(json_file)
            all_streaming_data.extend(streaming_data)
    except Exception as e:
        print(f"Error reading streaming data files: {str(e)}")
        return None

    # Parse the streaming data to identify skipped tracks
    skipped_tracks = parse_skipped_tracks(all_streaming_data)

    # Sort skipped tracks by count
    sorted_skipped_tracks = sorted(skipped_tracks.values(), key=lambda x: x['count'], reverse=True)

    # Return the sorted list of skipped tracks
    return sorted_skipped_tracks


