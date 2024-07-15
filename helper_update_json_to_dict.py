#!/usr/bin/env python3

import json
import sys

def update_json_structure(input_file):
    # Read the JSON file
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    # Update the structure of the 'tracks' field
    updated_tracks = {f'TRACK{track['number']}': track['name'] for track in data['tracks']}
    data['tracks'] = updated_tracks
    
    # Write the updated JSON back to the file
    with open(input_file, 'w') as file:
        json.dump(data, file, indent=4)
    
    print(f"Updated JSON has been written to {input_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_json.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    update_json_structure(input_file)
