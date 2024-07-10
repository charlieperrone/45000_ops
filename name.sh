#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 output_directory file_tracker song_name"
    exit 1
fi

# Directory containing the input files
output_dir="$1"
# File tracker argument
file_tracker="$2"
# Song name argument
song_name="$3"

# Create JSON structure using variables
json_string=$(jq -n \
                  --arg name "$song_name" \
                  --argjson tracks "$(printf '%s\n' "${file_tracker[@]}" | jq -R . | jq -s .)" \
                  '{
                    name: $name,
                    tracks: $tracks,
                  }')

# Create NAME.txt file with specified song name
name_file="$output_dir/NAME.txt"
cat <<EOF > "$name_file"
$json_string
EOF