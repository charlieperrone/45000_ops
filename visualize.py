#!/usr/bin/env python3

import os
import json

# Directory is hardcoded to the LIVESTRANGE card
parent_directory = "/Volumes/LIVESTRANGE"
# Song array keeps track of unique song names
song_array = []

def traverse(func, data):
    for folder in os.listdir(parent_directory):
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
        print(f"{os.path.basename(folder_path)}:")
        for track in tracks:
            track_number = track.get("number")
            track_name = track.get("name")
            print(f"Track {track_number}: {track_name}")
        print()  # Empty line for separation if needed

traverse(create_song_array, None)

for song in song_array:
    print(f'---[{song}]')
    traverse(render_tracks, song)