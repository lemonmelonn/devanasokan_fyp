import pandas as pd
import re

# Load dataset
df = pd.read_csv("C:/Users/User/Documents/devanasokan_fyp/storage/geniuslyrics.csv", encoding='utf-8-sig')
print("Initial shape:", df.shape)

# Remove missing / empty lyrics
# df = df.dropna(subset=['genius_lyrics'])
# df = df[df['genius_lyrics'].str.strip() != ""]

print("Shape after clean:", df.shape)

def fix_multiline_brackets(text):
    if not isinstance(text, str):
        return text
    
    # Replace newlines inside square brackets with spaces
    fixed_text = re.sub(
        r'\[(.*?)\]',
        lambda match: '[' + re.sub(r'\s*\n\s*', ' ', match.group(1)).strip() + ']',
        text,
        flags=re.DOTALL
    )
    
    return fixed_text

df['genius_lyrics'] = df['genius_lyrics'].apply(fix_multiline_brackets)


def split_lyrics_sections(lyrics):
    if not isinstance(lyrics, str):
        return []
    
    # Split based on [Section ...]
    parts = re.split(r'\[(.*?)\]', lyrics)
    
    sections = []
    
    # parts structure: [text_before, label1, text1, label2, text2, ...]
    for i in range(1, len(parts), 2):
        section_name = parts[i]
        section_text = parts[i+1].strip()
        
        if section_text:  # avoid empty sections
            sections.append((section_name, section_text))
    
    return sections

new_rows = []

for _, row in df.iterrows():
    sections = split_lyrics_sections(row['genius_lyrics'])
    
    for section_name, section_text in sections:
        new_row = row.to_dict()
        new_row['section'] = section_name
        new_row['genius_lyrics'] = section_text
        
        new_rows.append(new_row)

# Create new dataframe
verse_df = pd.DataFrame(new_rows)

# Format verses into a single line (separated by commas)
verse_df['genius_lyrics'] = verse_df['genius_lyrics'].apply(lambda x: ', '.join(x.splitlines()))

# Insert a new column 'verse_id' at the first position
verse_df.insert(0, 'verse_id', range(1, len(verse_df) + 1))

# Save output
print("After splitting:", verse_df.shape)
verse_df.to_csv('./storage/splitverses.csv', index=False, encoding='utf-8-sig')