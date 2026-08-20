# data.py
# In-memory dashboard data structures for CSV-free runtime

INITIAL_DASHBOARD_DATA = {
    "songs_by_id": {},
    "verses_by_song_id": {},
}


def init_dashboard_data(data):

    # Return a normalized, JSON-serializable dashboard data payload
    if not isinstance(data, dict):
        data = {}

    songs_by_id = data.get("songs_by_id")
    if not isinstance(songs_by_id, dict):
        songs_by_id = {}

    verses_by_song_id = data.get("verses_by_song_id")
    if not isinstance(verses_by_song_id, dict):
        verses_by_song_id = {}

    return {
        "songs_by_id": songs_by_id,
        "verses_by_song_id": verses_by_song_id,
    }
