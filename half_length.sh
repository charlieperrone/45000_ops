#!/bin/bash

# Ensure ffmpeg and ffprobe are installed
if ! command -v ffmpeg &> /dev/null || ! command -v ffprobe &> /dev/null
then
    echo "ffmpeg or ffprobe could not be found. Please install ffmpeg and ffprobe and try again."
    exit
fi

# Check if the folder path is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <folder_path>"
    exit 1
fi

FOLDER_PATH="$1"

# Check if the provided path is a directory
if [ ! -d "$FOLDER_PATH" ]; then
    echo "The provided path is not a directory."
    exit 1
fi

# Create the 'processed' directory if it doesn't exist
PROCESSED_DIR="$FOLDER_PATH/processed"
mkdir -p "$PROCESSED_DIR"

# Loop through all audio files in the folder
for FILE in "$FOLDER_PATH"/*; do
    if [[ "$FILE" == *.mp3 || "$FILE" == *.wav || "$FILE" == *.aac || "$FILE" == *.flac || "$FILE" == *.ogg || "$FILE" == *.m4a ]]; then
        # Get the duration of the audio file in seconds using ffprobe
        DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$FILE")

        # Calculate the half duration
        HALF_DURATION=$(echo "$DURATION / 2" | bc -l)

        # Generate the output file path
        BASENAME=$(basename "$FILE")
        OUTPUT_FILE="$PROCESSED_DIR/$BASENAME"

        # Use ffmpeg to trim the audio file to half its duration
        ffmpeg -i "$FILE" -t "$HALF_DURATION" -c copy "$OUTPUT_FILE"

        echo "Processed $FILE -> $OUTPUT_FILE"
    fi
done
