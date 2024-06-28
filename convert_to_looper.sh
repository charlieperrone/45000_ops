#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 input_directory"
  exit 1
fi

# Directory containing the input files
input_dir="$1"

# Create the output directory if it doesn't exist
mkdir -p "LOOP"

# Loop through all wav files in the input directory
for input_file in "$input_dir"/*.wav; do
  # Extract the base name of the file (without path and extension)
  base_name=$(basename "$input_file" .wav)
  
  # Define the output file path
  output_file="./LOOP/${base_name}.wav"
  
  # Execute the ffmpeg command to convert the file to mono
  ffmpeg -i "$input_file" -ac 1 "$output_file"
done

echo "Conversion completed."

