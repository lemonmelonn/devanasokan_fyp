import pandas as pd
import re
import contractions

# Load dataset
df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/geniuslyrics.csv", encoding='utf-8-sig')

# Drop old column and rename
df = df.drop(columns=['lyrics'])
df.rename(columns={'structured_lyrics': 'lyrics'}, inplace=True)

# Remove missing / empty lyrics
df = df.dropna(subset=['lyrics'])
df = df[df['lyrics'].str.strip() != ""]

print("Initial shape:", df.shape)


def clean_lyrics(text):
    if not isinstance(text, str):
        return ""

    # 1. Remove square brackets and contents
    text = re.sub(r"\[.*?\]", "", text, flags=re.DOTALL)

    # 2. Normalize apostrophes
    text = text.replace("’", "'")

    # 3. Convert adlibs: (adlib) → , adlib,
    text = re.sub(r"\s*\((.*?)\)", r", \1,", text)

    # 4. Fix merged words
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

    # 5. Split into verses (chunks)
    verses = re.split(r"\n\s*\n", text)

    cleaned_verses = []

    for verse in verses:
        verse = verse.strip()
        if not verse:
            continue

        # Split into lines
        lines = verse.split("\n")

        processed_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Normalize spacing around commas
            line = re.sub(r"\s*,\s*", ", ", line)

            # Remove extra commas at start
            line = re.sub(r"^,\s*", "", line)

            processed_lines.append(line)

        # Join lines within a verse using commas
        verse_text = ", ".join(processed_lines)

        cleaned_verses.append(verse_text)

    # 6. Join verses with double line breaks
    text = "\n\n".join(cleaned_verses)

    # 7. Apply contractions
    try:
        text = contractions.fix(text)
    except:
        pass

    # 8. Lowercase everything
    text = text.lower()

    # 9. Remove double commas
    text = re.sub(r",\s*,+", ", ", text)

    # 10. Clean spaces around commas
    text = re.sub(r"\s+,", ",", text)
    text = re.sub(r",\s+", ", ", text)

    # 11. Remove trailing commas in each line
    text = re.sub(r",\s*$", "", text, flags=re.MULTILINE)

    return text.strip()


# Apply cleaning
df['lyrics'] = df['lyrics'].apply(clean_lyrics)

print("After cleaning:", df.shape)

# Save output
df.to_csv('./storage/cleanlyrics.csv', index=False, encoding='utf-8-sig')