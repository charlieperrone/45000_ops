#!/bin/bash

# Directory is hardcoded to the LIVESTRANGE card
parent_directory="/Volumes/LIVESTRANGE"

# Loop through each folder in the parent directory
for folder in "$parent_directory"/*/; do
    # Check if the folder contains NAME.txt
    if [ -f "$folder/NAME.txt" ]; then
        # Read the content of NAME.txt
        folder_name=$(<"$folder/NAME.txt")
        # Extract the parent folder name
        parent_folder=$(basename "$folder")
        # Print the parent folder name and folder name
        echo "$parent_folder -> $folder_name"
    else
        echo "No NAME.txt found in $folder"
    fi
done
