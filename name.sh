#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 output_directory"
    exit 1
fi

# Directory containing the input files
output_dir="$1"
# Song name argument
song_name="$2"

# Create NAME.txt file with specified song name
name_file="$output_dir/NAME.txt"
cat <<EOF > "$name_file"
$song_name
EOF