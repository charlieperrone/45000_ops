#!/usr/bin/env python3

import json
import os
import sys

name_file = 'NAME.json'

def swap_file_names(file1, file2):
    # Check if both files exist
    if not os.path.isfile(file1):
        print(f"Error: {file1} does not exist.")
        return False
    if not os.path.isfile(file2):
        print(f"Error: {file2} does not exist.")
        return False

    # Get the directory names of the files
    dir1 = os.path.dirname(file1)
    dir2 = os.path.dirname(file2)

    # Create temporary file names
    temp_file1 = os.path.join(dir1, "temp_swap_file1")
    temp_file2 = os.path.join(dir2, "temp_swap_file2")

    try:
        # Rename the files to temporary names
        os.rename(file1, temp_file1)
        os.rename(file2, temp_file2)
        
        # Swap the temporary file names
        os.rename(temp_file1, file2)
        os.rename(temp_file2, file1)

        print(f"Swapped the files {file1} and {file2}")
        return True

    except Exception as e:
        print(f"Error occurred during file swapping: {e}")
        # Restore original names if swapping failed
        if os.path.isfile(temp_file1):
            os.rename(temp_file1, file1)
        if os.path.isfile(temp_file2):
            os.rename(temp_file2, file2)
        
        return False

def swap_dict_entries(d, key1, key2):
    if key1 in d and key2 in d:
        # Use a temporary variable to hold one of the values
        temp = d[key1]
        d[key1] = d[key2]
        d[key2] = temp

        return d
    else:
        print(f"Error: Both {key1} and {key2} must exist in the dictionary")
        return None

def update_name_file(file1, file2):
    if not os.path.isfile(name_file):
        print(f"Error: {name_file} does not exist.")
        return False

    try:
        with open(name_file, 'r') as file:
            data = json.load(file)
            
        updated_tracks = swap_dict_entries(data['tracks'], os.path.splitext(file1)[0], os.path.splitext(file2)[0])
        if updated_tracks is not None:
            data['tracks'] = updated_tracks

            # Write the updated JSON back to the file
            with open(name_file, 'w') as file:
                json.dump(data, file, indent=4)  # Use data, not name_file
                
            print(f"Updated {name_file} with swapped track names.")
            return True
        else:
            return False
    
    except Exception as e:
        print(f"Error occurred during JSON update: {e}")
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
