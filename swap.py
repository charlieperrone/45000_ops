#!/usr/bin/env python3
"""Module providing functions that swap two given filepaths
   and updates NAME.json data model accordingly."""

import json
import os
import sys

NAME_FILE = 'NAME.json'

def swap_file_names(f1, f2):
    """Function that swaps the names of two given filepaths."""
    # Check if both files exist
    if not os.path.isfile(f1):
        print(f"Error: {f1} does not exist.")
        return False
    if not os.path.isfile(f2):
        print(f"Error: {f2} does not exist.")
        return False

    # Get the directory names of the files
    dir1 = os.path.dirname(f1)
    dir2 = os.path.dirname(f2)

    # Create temporary file names
    temp_file1 = os.path.join(dir1, "temp_swap_file1")
    temp_file2 = os.path.join(dir2, "temp_swap_file2")

    try:
        # Rename the files to temporary names
        os.rename(f1, temp_file1)
        os.rename(f2, temp_file2)
        # Swap the temporary file names
        os.rename(temp_file1, f2)
        os.rename(temp_file2, f1)

        print(f"Swapped the files {f1} and {f2}")
        return True

    except FileNotFoundError as e:
        print(f"File not found error: {e}")
        return False
    except OSError as e:
        print(f"OS error occurred during file swapping: {e}")
        # Restore original names if swapping failed
        if os.path.isfile(temp_file1):
            os.rename(temp_file1, f1)
        if os.path.isfile(temp_file2):
            os.rename(temp_file2, f2)
        return False

def swap_dict_entries(d, key1, key2):
    """Function that swaps two given dictionary keys"""
    if key1 in d and key2 in d:
        # Use a temporary variable to hold one of the values
        temp = d[key1]
        d[key1] = d[key2]
        d[key2] = temp

        return d

    print(f"Error: Both {key1} and {key2} must exist in the dictionary")
    return None

def update_name_file(f1, f2):
    """Function updating NAME.json according to swap operation."""
    if not os.path.isfile(NAME_FILE):
        print(f"Error: {NAME_FILE} does not exist.")
        return False

    try:
        with open(NAME_FILE, 'r', encoding="utf-8") as file:
            data = json.load(file)

        updated_tracks = swap_dict_entries(data['tracks'],
                                            os.path.splitext(f1)[0],
                                            os.path.splitext(f2)[0])
        if updated_tracks is not None:
            data['tracks'] = updated_tracks

            # Write the updated JSON back to the file
            with open(NAME_FILE, 'w', encoding="utf-8") as file:
                json.dump(data, file, indent=4)  # Use data, not name_file
            print(f"Updated {NAME_FILE} with swapped track names.")
            return True
        return False
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
        return False

    except json.JSONDecodeError as e:
        print(f"JSON decoding error occurred: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: swap_files.py <file1> <file2>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    if swap_file_names(file1, file2):
        if not update_name_file(file1, file2):
            print("Reverting file names due to update failure.")
            swap_file_names(file1, file2)  # Revert file names if update failed
    else:
        print("File swapping failed, update aborted.")
