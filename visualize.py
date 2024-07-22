#!/usr/bin/env python3
"""
Module Name: visualize.py

This module provides function to traverse a directory structure and visualize its contents.

Author: Charlie Perrone

Date: 2024
"""

import os
import json

# Directory is hardcoded to the LIVESTRANGE card
PARENT_DIRECTORY = "/Volumes/LIVESTRANGE"
# Song array keeps track of unique song names
song_array = []

def is_not_empty(n):
    """
    Check if a list is not empty.

    Parameters:
    n (list): The list to check.

    Returns:
    bool: True if the list is not empty, False otherwise.
    """
    return n != []

def open_file(file):
    """Wraps OS file method"""
    return open(file, 'r', encoding='utf-8')

def traverse(func, data):
    """
    Traverse directories and apply a function to JSON data.

    Parameters:
    func (callable): A function that takes three arguments: the JSON data, the folder path, 
                     and the additional data.
    data (any): Additional data to be passed to the function `func`.

    Returns:
    list: A list of results returned from the function `func` for each folder.
    """
    # keep track of any returned data from func
    result = []
    # sort folders in alphabetical order
    folders = sorted(os.listdir(PARENT_DIRECTORY))
    for folder in folders:
        folder_path = os.path.join(PARENT_DIRECTORY, folder)
        if os.path.isdir(folder_path):
            # Check if the folder contains NAME.json
            name_file_path = os.path.join(folder_path, "NAME.json")
            if os.path.isfile(name_file_path):
                # Read the content of NAME.json
                with open_file(name_file_path) as name_file:
                    folder_name = name_file.read().strip()
                # Load json data
                json_data = json.loads(folder_name)
                # execute function and append any returned data to the result
                func_data = func(json_data, folder_path, data)
                # append to result list
                result.append(func_data)

    return result

# Loop through each folder in the parent directory
def create_song_array(data, _, s):
    """
    Add a unique song name to the global song_array.

    This function extracts the song name from the provided data dictionary
    and appends it to the global song_array if it's not already present.

    Args:
        data (dict): A dictionary containing song information.
                     Must have a 'song_name' key.
        _ : Placeholder parameter (not used in the function).
        song : Placeholder parameter (overwritten in the function).

    Global Variables:
        song_array (list): A list to store unique song names.

    Returns:
        None

    Side Effects:
        Modifies the global song_array by potentially adding a new song name.

    Raises:
        KeyError: If 'song_name' is not a key in the data dictionary.

    Example:
        >>> song_array = []
        >>> data = {'song_name': 'Bohemian Rhapsody'}
        >>> create_song_array(data, None, None)
        >>> print(song_array)
        ['Bohemian Rhapsody']
    """
    s = data['song_name']
    # Append to song array, if it doesn't already exist
    if s not in song_array:
        song_array.append(data['song_name'])

def render_tracks(data, folder_path, desired_song_name):
    """
    Render track names for a specific song from JSON data.

    This function extracts the `song_name` and `tracks` from the provided JSON data, 
    checks if the `song_name` matches the `desired_song_name`, and if so, formats 
    and returns a string containing the loop number (derived from the folder path) 
    followed by the names of the tracks.

    Parameters:
    data (dict): The JSON data containing the song information.
    folder_path (str): The path of the folder containing the JSON file.
    desired_song_name (str): The name of the song to match against.

    Returns:
    list: A list containing a single formatted string with the loop number and track names 
          if the song name matches; otherwise, an empty list.
    """
    # Extract song_name and tracks from JSON data
    song_name = data.get("song_name")
    tracks = data.get("tracks", {})
    # instantiate result string
    result = []
    # Check if song_name matches the desired song_name
    if song_name == desired_song_name:
        # create track content array
        track_names = []
        # save the loop number
        loop_number = os.path.basename(folder_path)
        # append loop number
        track_names.append(loop_number)

        # loop through all tracks and display
        for track in tracks:
            track_names.append(tracks[track])


        # format array into string
        result.append(', '.join(map(str, track_names)))

    # return result
    return result

# Requires data in the following format
# headers = ["[PERSONAL]"]
# rows = [
#     ["01 PERSONAL COMPUTER MARKET Embroidered Black T-Shirt"],
#     ["02 PERSONAL COMPUTER MARKET Puff Print Navy Hoodie"],
#     ["03 Being Harsh/Acid Angel T-Shirt (Silver Edition)"]
# ]
def create_rounded_corner_table(headers, rows):
    """
    Create a table with rounded corners from the given headers and rows.

    This function generates a table with rounded corners using the provided headers 
    and rows. The table is formatted with a rounded top border, a separator between 
    the header and data rows, and a rounded bottom border.

    Parameters:
    headers (list of str): A list of header strings for the table columns.
    rows (list of list of str): A list of rows, where each row is a list of strings 
                                representing the data for each column.

    Returns:
    str: A string representation of the table with rounded corners.
    """
    # Create the header row
    header_row = '╭' + '-'.join(headers)

    # Create the separator between header and rows
    separator = '│'

    # Create the bottom border
    bottom_border = '╰' + '────'

    # Create all data rows
    data_rows = []
    for row in rows:
        data_row = '│ ' + ' │ '.join(row)
        data_rows.append(data_row)

    # Combine all parts into the final table
    table = [header_row, separator] + data_rows + [bottom_border]
    return '\n'.join(table)

traverse(create_song_array, None)

for song in song_array:
    # build headers and rows
    h = [f"[{song}]"]
    r = traverse(render_tracks, song)
    filtered_rows = list(filter(is_not_empty, r))

    print(create_rounded_corner_table(h, filtered_rows))
    print()
