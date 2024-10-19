import json

THRESHOLD = 3000  # time in milliseconds to determine a 'skip'
SKIP_THRESHOLD = 5

def parse_skipped_tracks(json_files):
    data = {}
    for json_file in json_files:
        items = json.load(json_file)

        for item in items:
            if item['msPlayed'] < THRESHOLD:
                slug = item['artistName'] + item['trackName']
                if slug in data:
                    data[slug]['count'] += 1
                else:
                    data[slug] = {
                        'artist': item['artistName'],
                        'track': item['trackName'],
                        'count': 1
                    }

    to_remove = [v for v in data.values() if v['count'] >= SKIP_THRESHOLD]
    return to_remove
