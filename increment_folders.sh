#!/bin/bash

# Iterate over all folders matching "LOOP[0-9][0-9]" in the current directory
for dir in LOOP[0-9][0-9]
do
  # Extract the numeric part of the folder name
  num=${dir//[^0-9]/}
  
  # Increment the number
  new_num=$((10#$num + 1))
  
  # Format the new number to be two digits, e.g., 01, 02, etc.
  new_num=$(printf "%02d" $new_num)
  
  # Construct the new folder name
  new_dir="LOOP$new_num"
  
  # Check if the new folder name already exists
  if [ -d "$new_dir" ]; then
    echo "Skipping $dir: $new_dir already exists"
  else
    # Rename the folder
    mv "$dir" "$new_dir"
    echo "Renamed $dir to $new_dir"
  fi
done
