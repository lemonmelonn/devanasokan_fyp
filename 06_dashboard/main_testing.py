from functions import get_llm_explanation, load_model ,detect_explicit, get_structured_lyrics, split_verses ,clean_verses ,get_model_output
from spotify_functions import get_access_token, get_song_details
from csv_functions import add_nonexplicit_song, add_explicit_song, check_song_exists, retrieve_song_info, retrieve_verse_info, update_clean_verse, update_song_label, update_song_info

classifier = load_model()
token = get_access_token()

def non_explicit_pipeline(title, artist, CSV_FILE):
    full_song = get_structured_lyrics(artist, title)
    # print(full_song[:100])

    split_verses(SONG_ID, full_song)
    
    text = clean_verses(SONG_ID)
    print(text[:100])

    ovr_label = get_model_output(classifier, SONG_ID, "verselabels.csv")
    print(f"\nOverall label for the song: {ovr_label}")

    update_song_label(SONG_ID, ovr_label, CSV_FILE)

# ------------------- MAIN PIPELINE -----------------

song = get_song_details(
    song_title="DEBUT",
    artist_name="KATSEYE",
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


# Check if song exists in respective CSV file
# If no record, add song details
if not exists:
    if explicit:
        add_explicit_song(SONG_ID, TITLE, ARTIST, CSV_FILE)
        
    else:
        add_nonexplicit_song(SONG_ID, TITLE, ARTIST, CSV_FILE)
        non_explicit_pipeline(TITLE, ARTIST, CSV_FILE)
        verse_info = retrieve_verse_info(SONG_ID, "verselabels.csv")
    
    maininfo = retrieve_song_info(SONG_ID, CSV_FILE)
    print(maininfo)
        
# If record exists, retrieve and print details
else:
    print(f"Song ID {SONG_ID} already exists in {CSV_FILE}.")
    maininfo = retrieve_song_info(SONG_ID, CSV_FILE)
    
    if explicit:
        print(maininfo)
    else:
        verse_info = retrieve_verse_info(SONG_ID, "verselabels.csv")
        print(verse_info)
        print(maininfo)


# ----------------- LLM INFO -----------------
llm_info = get_llm_explanation(SONG_ID, CSV_FILE)
print(f"LLM Explanation for Song ID {SONG_ID}: {llm_info}")