from functions import load_model ,detect_explicit, get_structured_lyrics, split_verses ,clean_verses ,get_model_output
from spotify_functions import get_access_token, get_song_details
from csv_functions import add_nonexplicit_song, add_explicit_song, check_song_exists, retrieve_song_info, update_clean_verse, update_song_label, update_song_info, get_ovrlabel

classifier = load_model()
token = get_access_token()

song = get_song_details(
    song_title="Good Luck babe",
    artist_name="Chappel Roan",
    access_token=token
)

print(song)
if song is None:
    raise SystemExit("Spotify search returned no match.")

SONG_ID = song["song_id"]
ARTIST = song["artist"]
TITLE = song["title"]

explicit = detect_explicit(song)
if explicit:
    CSV_FILE = "explicit.csv"
else:
    CSV_FILE = "nonexplicit.csv"

exists = check_song_exists(SONG_ID, CSV_FILE)


def non_explicit_pipeline(title, artist):
    full_song = get_structured_lyrics(artist, title)
    print(full_song[:100])

    split_verses(SONG_ID, full_song)
    
    text = clean_verses(SONG_ID)
    print(text[:100])

    get_model_output(classifier, SONG_ID, "verselabels.csv")
    # ovr_label = get_ovrlabel()
    # update_song_label(SONG_ID, ovr_label, CSV_FILE)


if not exists:
    if explicit:
        add_explicit_song(SONG_ID, TITLE, ARTIST, CSV_FILE)
    else:
        add_nonexplicit_song(SONG_ID, TITLE, ARTIST, CSV_FILE)
        non_explicit_pipeline(TITLE, ARTIST)
else:
    print(f"Song ID {SONG_ID} already exists in {CSV_FILE}.")
    retrieve = retrieve_song_info(SONG_ID, CSV_FILE)
    print(retrieve)

# update_song_label(SONG_ID, "UNSAFE", CSV_FILE)