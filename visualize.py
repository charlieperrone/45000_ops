#!/usr/bin/env python3

import os
import json

# Directory is hardcoded to the LIVESTRANGE card
parent_directory = "/Volumes/LIVESTRANGE"
# Song array keeps track of unique song names
song_array = []

def traverse(func, data):
    folders = sorted(os.listdir(parent_directory))
    for folder in folders:
        folder_path = os.path.join(parent_directory, folder)
        if os.path.isdir(folder_path):
            # Check if the folder contains NAME.json
            name_file_path = os.path.join(folder_path, "NAME.json")
            if os.path.isfile(name_file_path):
                # Read the content of NAME.json
                with open(name_file_path, 'r') as name_file:
                    folder_name = name_file.read().strip()
                # Load json data
                json_data = json.loads(folder_name)
                # execute function
                func(json_data, folder_path, data)

# Loop through each folder in the parent directory
def create_song_array(data, _, song):
    song = data['song_name']
    # Append to song array, if it doesn't already exist
    if song not in song_array:
        song_array.append(data['song_name'])

def render_tracks(data, folder_path, desired_song_name):
    # Extract song_name and tracks from JSON data
    song_name = data.get("song_name")
    tracks = data.get("tracks", [])
    
    # Check if song_name matches the desired song_name
    if song_name == desired_song_name:
        # save the loop number
        loop_number = os.path.basename(folder_path)
        # create track content array
        track_names = []

        # loop through all tracks and display
        for track in tracks:
            track_name = track.get("name")
            track_names.append(track_name)
        print(f"| {loop_number} {track_names}")

def create_rounded_corner_table(headers, rows):
    # Calculate column widths
    col_widths = [max(len(str(item)) for item in column) for column in zip(headers, *rows)]
    
    # Create the top border
    # top_border = '╭' + '┬'.join('─' * (width + 2) for width in col_widths) + '╮'
    
    # Create the header row
    header_row = '╭' + '-'.join(headers)
    
    # Create the separator between header and rows
    separator = '│'
    
    # Create the bottom border
    bottom_border = '╰' + '──────────'
    
    # Create all data rows
    data_rows = []
    for row in rows:
        data_row = '│ ' + ' │ '.join(row)
        data_rows.append(data_row)
    
    # Combine all parts into the final table
    table = [header_row, separator] + data_rows + [bottom_border]
    return '\n'.join(table)

headers = ["[PERSONAL]"]
rows = [
    ["01 PERSONAL COMPUTER MARKET Embroidered Black T-Shirt"],
    ["02 PERSONAL COMPUTER MARKET Puff Print Navy Hoodie"],
    ["03 Being Harsh/Acid Angel T-Shirt (Silver Edition)"]
]

print(create_rounded_corner_table(headers, rows))


traverse(create_song_array, None)

for song in song_array:
    # print song title
    print(f'---[{song}]')
    # print all of the relevant loops for each song
    traverse(render_tracks, song)
    # print empty line
    print()