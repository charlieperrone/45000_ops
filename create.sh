#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 input_directory output_directory song_name"
    exit 1
fi

# Directory containing the input files
input_dir="$1"
# Directory to save the output files
output_dir="$2"
# Song name
song_name="$3"

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
wav_files=("$input_dir"/*.wav)
file_count=${#wav_files[@]}

# Function to create silent audio files
create_silent_files() {
    local original_file="$1"
    local output_dir="$2"
    local count="$3"
    local start_index="$4"
    local duration
    duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$original_file")

    for i in $(seq 1 "$count"); do
        ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t "$duration" "$output_dir/TRACK$(($start_index + $i)).wav"
    done
}

# Function to create a silent stereo file
create_silent_stereo_file() {
    local original_file="$1"
    local output_dir="$2"
    local duration
    duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$original_file")
    ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t "$duration" "$output_dir/TRACKM.wav"
}

# Determine the number of silent files and if a silent stereo file is needed
case "$file_count" in
    1)
        create_silent_files "${wav_files[0]}" "$output_dir" 3 "$file_count"
        create_silent_stereo_file "${wav_files[0]}" "$output_dir"
        ;;
    2)
        create_silent_files "${wav_files[0]}" "$output_dir" 2 "$file_count"
        create_silent_stereo_file "${wav_files[0]}" "$output_dir"
        ;;
    3)
        create_silent_files "${wav_files[0]}" "$output_dir" 1 "$file_count"
        create_silent_stereo_file "${wav_files[0]}" "$output_dir"
        ;;
    4)
        create_silent_stereo_file "${wav_files[0]}" "$output_dir"
        ;;
    5)
        # Do nothing
        ;;
    *)
        echo "Invalid number of files"
        exit 1
        ;;
esac

# Initialize a counter for output files
track_counter=1

# Loop through all wav files in the input directory
for input_file in "${wav_files[@]}"; do
    # Define the output file path
    output_file="$output_dir/TRACK${track_counter}.wav"
    
    # Execute the ffmpeg command to convert the file to mono
    ffmpeg -i "$input_file" -ac 1 "$output_file"
    
    # Increment the track counter
    track_counter=$((track_counter + 1))
done

# Create TEMPO.txt file with specified contents
tempo_file="$output_dir/TEMPO.txt"
cat <<EOF > "$tempo_file"
Record:
  Tempo= 138.2011 bpm (Min 59 to max 240)
  QUANTISE= Off (Off or On)
  STEREO= Off   (Off or On)
Last Play:                  
  TEMPO POT= (0 to 127 or blank)
  OCTAVE= Off    (Off or On)
  REVERSE= Off  (Off or On)
  You can use Notepad to edit this file when importing track files. In that case put value in Record Tempo but leave TEMPO POT value blank.
EOF

# Create NAME.txt file with specified song name
name_file="$output_dir/NAME.txt"
cat <<EOF > "$name_file"
$song_name
EOF



echo "TEMPO.txt created: $tempo_file"
echo "Conversion completed."
