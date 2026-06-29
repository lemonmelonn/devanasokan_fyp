import pandas as pd
import os


def _clean_text_value(value):
    if pd.isna(value):
        return ""

    text = str(value)
    if text.endswith(".0"):
        text = text[:-2]

    return text

def add_nonexplicit_song(song_id, title, artist, CSV_FILE):
    """
    Add a song to the CSV file.

    Columns:
    song_id, title, artist, ovr_label, llm_info
    """

    # Create CSV if it doesn't exist
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(
            columns=[
                "song_id",
                "title",
                "artist",
                "ovr_label",
                "llm_info"
            ]
        )
        df.to_csv(CSV_FILE, index=False)

    # Load existing data
    df = pd.read_csv(CSV_FILE)

    # Create new row
    new_row = {
        "song_id": song_id,
        "title": title,
        "artist": artist,
        "ovr_label": "",
        "llm_info": ""
    }

    # Append row
    df.loc[len(df)] = new_row

    # Save
    df.to_csv(CSV_FILE, index=False)

    print(f"Added: [{song_id}] {title} - {artist}")

    return song_id


def add_explicit_song(song_id, title, artist, CSV_FILE):
    """
    Add a song to the CSV file.

    Columns:
    song_id, title, artist, lyrics, ovr_label, llm_info
    """

    # Create CSV if it doesn't exist
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(
            columns=[
                "song_id",
                "title",
                "artist",
                "lyrics",
                "ovr_label",
                "llm_info"
            ]
        )
        df.to_csv(CSV_FILE, index=False)

    # Load existing data
    df = pd.read_csv(CSV_FILE)

    # Create new row
    new_row = {
        "song_id": song_id,
        "title": title,
        "artist": artist,
        "lyrics": "",
        "ovr_label": "UNSAFE",
        "llm_info": ""
    }

    # Append row
    df.loc[len(df)] = new_row

    # Save
    df.to_csv(CSV_FILE, index=False)

    print(f"Added: [{song_id}] {title} - {artist}")

    return song_id

def check_song_exists(song_id, CSV_FILE):
    """
    Check if a song with the given ID exists in the CSV file.

    Returns:
        True if the song exists, False otherwise.
    """

    if not os.path.exists(CSV_FILE):
        return False
    
    print(f"Checking if song ID {song_id} exists in {CSV_FILE}...")

    df = pd.read_csv(CSV_FILE, keep_default_na=False)
    exists = str(song_id) in df["song_id"].astype(str).values
    print(f"Does the song exist? {exists}")
    return exists


def add_verses(song_id, verse_id, section, verse, CSV_FILE):
    """
    Add verse to a song in the CSV file.

    Args:
        song_id: The ID of the song to update.
        verse_id: The ID of the verse to add.
        section: The section name for the verse.
        verse: The verse text to add.
    """

    if not os.path.exists(CSV_FILE):
        print(f"CSV file {CSV_FILE} does not exist.")
        return False

    df = pd.read_csv(CSV_FILE, dtype={"song_id": "str"}, keep_default_na=False)

    song_id = str(song_id)

    # Add new row
    new_row = {
        "song_id": song_id,
        "verse_id": verse_id,
        "section": section,
        "ori_verse": verse
    }
    df.loc[len(df)] = new_row

    # Save changes
    df.to_csv(CSV_FILE, index=False)

    print(f"Added verses for Song ID {song_id}")
    return True


def update_clean_verse(song_id, verse_id, clean_verse, CSV_FILE):

    # Load CSV
    df = pd.read_csv(
        CSV_FILE,
        dtype={"song_id": str, "verse_id": str},
        keep_default_na=False
    )

    # Clean IDs
    song_id = str(song_id).strip()
    verse_id = str(verse_id).strip()

    # Clean dataframe IDs
    df["song_id"] = df["song_id"].astype(str).str.strip()
    df["verse_id"] = df["verse_id"].astype(str).str.strip()

    # Find matching row
    mask = (
        (df["song_id"] == song_id) &
        (df["verse_id"] == verse_id)
    )

    if not mask.any():
        print(f"Song ID {song_id} with Verse ID {verse_id} not found.")

        # Debug information
        print("\nMatching song rows:")
        print(df[df["song_id"] == song_id][["song_id", "verse_id"]])

        return False

    # Update value
    df.loc[mask, "clean_verse"] = clean_verse

    # Save CSV
    df.to_csv(CSV_FILE, index=False)

    print(f"Updated Song ID {song_id}, Verse ID {verse_id}")
    return True


# Update the ovr_label for a specific song.
def update_song_label(song_id, ovr_label, CSV_FILE):

    # Load CSV
    df = pd.read_csv(CSV_FILE, dtype={"song_id": "str"}, keep_default_na=False)

    if "ovr_label" in df.columns:
        df["ovr_label"] = df["ovr_label"].map(_clean_text_value)

    song_id = str(song_id)

    # Check if song exists
    if song_id not in df["song_id"].values:
        print(f"Song ID {song_id} not found.")
        return False

    # Update values
    df.loc[df["song_id"] == song_id, "ovr_label"] = _clean_text_value(ovr_label)

    # Save changes
    df.to_csv(CSV_FILE, index=False)

    print(f"Updated label for Song ID {song_id}")
    return True

# Update the label and score for a specific verse
def update_verse_label_score(song_id, verse_id, verse_label, verse_score, CSV_FILE):

    # Load CSV
    df = pd.read_csv(CSV_FILE, dtype={"song_id": "str"}, keep_default_na=False)

    if "label" in df.columns:
        df["label"] = df["label"].map(_clean_text_value)

    song_id = str(song_id)
    verse_id = str(verse_id)

    # Check if song exists
    if song_id not in df["song_id"].values:
        print(f"Song ID {song_id} not found.")
        return False

    # Update values
    df.loc[(df["song_id"] == song_id) & (df["verse_id"] == verse_id), "label"] = _clean_text_value(verse_label)
    df.loc[(df["song_id"] == song_id) & (df["verse_id"] == verse_id), "score"] = verse_score

    # Save changes
    df.to_csv(CSV_FILE, index=False)

    print(f"Updated label for Song ID {song_id}, Verse ID {verse_id}")
    return True


# Update the llm_info for a specific song.
def update_song_info(song_id, llm_info, CSV_FILE):
   
    # Load CSV
    df = pd.read_csv(CSV_FILE, dtype={"song_id": "str"}, keep_default_na=False)

    if "llm_info" in df.columns:
        df["llm_info"] = df["llm_info"].map(_clean_text_value)

    song_id = str(song_id)

    # Check if song exists
    if song_id not in df["song_id"].values:
        print(f"Song ID {song_id} not found.")
        return False

    # Update values
    df.loc[df["song_id"] == song_id, "llm_info"] = _clean_text_value(llm_info)

    # Save changes
    df.to_csv(CSV_FILE, index=False)

    print(f"Updated info for Song ID {song_id}")
    return True


def retrieve_song_info(song_id, CSV_FILE):
    """
    Retrieve a song's details from the CSV file based on its ID.

    Returns:
        dict containing song details, or None if not found.
    """

    if not os.path.exists(CSV_FILE):
        print(f"CSV file {CSV_FILE} does not exist.")
        return None

    df = pd.read_csv(CSV_FILE, dtype={"song_id": "str"}, keep_default_na=False)

    song_id = str(song_id)

    # Check if song exists
    if song_id not in df["song_id"].values:
        print(f"Song ID {song_id} not found.")
        return None

    # Retrieve the row
    row = df[df["song_id"] == song_id].iloc[0]

    if CSV_FILE == "explicit.csv":
        return {
            "song_id": row["song_id"],
            "title": row["title"],
            "artist": row["artist"],
            "lyrics": row.get("lyrics", ""),
            "ovr_label": row.get("ovr_label", ""),
            "llm_info": row.get("llm_info", "")
        }
    else:
        return {
            "song_id": row["song_id"],
            "title": row["title"],
            "artist": row["artist"],
            "ovr_label": row.get("ovr_label", ""),
            "llm_info": row.get("llm_info", "")
        }
    

def retrieve_verse_info(song_id, CSV_FILE):
    """
    Retrieve a song's verses from the CSV file based on its ID.

    Returns:
        list of dicts containing verse details, or None if not found.
    """

    if not os.path.exists(CSV_FILE):
        print(f"CSV file {CSV_FILE} does not exist.")
        return None

    df = pd.read_csv(CSV_FILE, dtype={"song_id": "str"}, keep_default_na=False)

    song_id = str(song_id)

    # Check if song exists
    if song_id not in df["song_id"].values:
        print(f"Song ID {song_id} not found.")
        return None

    # Retrieve all rows for the song
    verses_df = df[df["song_id"] == song_id]

    return verses_df

