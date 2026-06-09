import requests
import pandas as pd
import time

artist_name = "TWICE"

# Search artist
url = "https://musicbrainz.org/ws/2/artist/"
params = {
    "query": artist_name,
    "fmt": "json"
}

response = requests.get(
    url,
    params=params,
    headers={"User-Agent": "SongDatasetBuilder/1.0"}
)

artist_data = response.json()

artist_id = artist_data["artists"][0]["id"]

print("Artist ID:", artist_id)

# Retrieve recordings
songs = []
offset = 0
limit = 100

while True:
    recording_url = f"https://musicbrainz.org/ws/2/recording"

    params = {
        "artist": artist_id,
        "fmt": "json",
        "limit": limit,
        "offset": offset
    }

    response = requests.get(
        recording_url,
        params=params,
        headers={"User-Agent": "SongDatasetBuilder/1.0"}
    )

    data = response.json()

    recordings = data.get("recordings", [])

    if not recordings:
        break

    for rec in recordings:
        songs.append(rec["title"])

    offset += limit

    print(f"Retrieved {len(songs)} songs...")

    time.sleep(1)

# Remove duplicates
songs = sorted(set(songs))

# Save CSV
df = pd.DataFrame({"song_title": songs})

csv_name = f"{artist_name.replace(' ', '_')}_songs.csv"

df.to_csv(csv_name, index=False)

print(f"Saved {len(df)} songs to {csv_name}")