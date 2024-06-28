#!/bin/bash

# Function to extract tempo information using ffprobe
extract_tempo_info() {
    local input_file="$1"
    local ffprobe_output=$(ffprobe -v error -show_entries format_tags=title -of default=noprint_wrappers=1:nokey=1 "$input_file")
    local tempo_info=$(echo "$ffprobe_output" | grep -o 'Tempo: [0-9.]*' | awk '{print $2}')

    if [ -n "$tempo_info" ]; then
        echo "$tempo_info"
    else
        echo "0"  # Default value if tempo information is not found
    fi
}

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 input_directory"
    exit 1
fi

# Directory containing the input files
input_dir="$1"
# Directory to save the output files
output_dir="LOOP"

# Function to clear contents of a directory
clear_directory() {
    local dir="$1"
    if [ -d "$dir" ]; then
        echo "Clearing contents of directory: $dir"
        rm -rf "${dir:?}/"*
    fi
}

# Clear contents of the output directory if it exists
clear_directory "$output_dir"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Count the number of wav files in the input directory
file_count=$(ls "$input_dir"/*.wav 2>/dev/null | wc -l)

# List all wav files in the input directory
wav_files=("$input_dir"/*.wav)

# If there are less than 5 files, prompt the user
if [ "$file_count" -lt 5 ]; then
    echo "Only $file_count files found. Would you like to create a stereo version of the last file in the directory? (yes/no)"
    read response
    
    if [ "$response" == "yes" ]; then
        # Prompt user to select a file for stereo conversion
        echo "Select a file to create a stereo version:"
        select file in "${wav_files[@]}"; do
            if [ -n "$file" ]; then
                # Get the base name of the selected file (without path and extension)
                base_name=$(basename "$file" .wav)
                stereo_output_file="$output_dir/TRACKM.wav"
                
                # Create a stereo version of the selected file
                ffmpeg -i "$file" -ac 2 "$stereo_output_file"
                echo "Stereo version created: $stereo_output_file"
                
                break
            else
                echo "Invalid selection. Please choose a number from the list."
            fi
        done
    fi
fi

# Initialize a variable to store the first found tempo
first_tempo=""

# Initialize a counter for output files
track_counter=1

# Loop through all wav files in the input directory
for input_file in "${wav_files[@]}"; do
    # Define the output file path
    output_file="$output_dir/TRACK${track_counter}.wav"
    
    # Execute the ffmpeg command to convert the file to mono
    ffmpeg -i "$input_file" -ac 1 "$output_file"
    
    # Extract tempo information for the current file
    tempo=$(extract_tempo_info "$input_file")
    echo "Tempo value for $input_file: $tempo"
    
    # Store the first found tempo value
    if [ -z "$first_tempo" ] && [ "$tempo" != "0" ]; then
        first_tempo="$tempo"
    fi
    
    # Increment the track counter
    track_counter=$((track_counter + 1))
done

# Create TEMPO.txt file with specified contents
tempo_file="$output_dir/TEMPO.txt"
cat <<EOF > "$tempo_file"
Record:
  Tempo= ${first_tempo:-138.2011} bpm (Min 59 to max 240)
  QUANTISE= Off (Off or On)
  STEREO= Off   (Off or On)
Last Play:                  
  TEMPO POT= (0 to 127 or blank)
  OCTAVE= Off    (Off or On)
  REVERSE= Off  (Off or On)
  You can use Notepad to edit this file when importing track files. In that case put value in Record Tempo but leave TEMPO POT value blank.
EOF

echo "TEMPO.txt created: $tempo_file"
echo "Conversion completed."
