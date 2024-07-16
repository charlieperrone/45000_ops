#!/usr/bin/env python3
"""
Module Name: help_update_json_to_dict.py

This module provides a function to move a specific json structure to a specific dictionary structure.

Author: Charlie Perrone

Date: 2024
"""

import json
import sys

def update_json_structure(file):
    """
    Update the structure of a JSON file containing track information.

    This function reads a JSON file, updates the structure of the 'tracks' field 
    by renaming each track using a formatted string 'TRACK{number}', and writes 
    the updated JSON back to the file.

    Parameters:
    file (str): Path to the JSON file to be updated.

    Returns:
    None
    """
    # Read the JSON file
    with open(file, 'r', encoding="utf-8") as f:
        data = json.load(f)

    # Update the structure of the 'tracks' field
    updated_tracks = {f'TRACK{track['number']}': track['name'] for track in data['tracks']}
    data['tracks'] = updated_tracks

    # Write the updated JSON back to the file
    with open(file, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Updated JSON has been written to {file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_json.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    update_json_structure(input_file)
