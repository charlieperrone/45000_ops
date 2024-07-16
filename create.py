#!/usr/bin/env python3
"""
Module Name: create.py

This module provides functions for performing audio file creation using FFmpeg.

Author: Charlie Perrone

Date: 2024
"""

import os
import shutil
import sys
import subprocess
import json

def open_file(file, mode):
    """Wraps OS file method"""
    return open(file, mode, encoding='utf-8')

def clear_directory(dir_path):
    """
    Clear all contents of a specified directory.

    This function removes all files, links, and subdirectories within the specified 
    directory. If the directory exists, it prints a message indicating the directory 
    being cleared.

    Parameters:
    dir_path (str): The path to the directory to be cleared.

    Returns:
    None
    """
    if os.path.exists(dir_path):
        print(f"Clearing contents of directory: {dir_path}")
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

def create_silent_files(original_file, output_dir, count, start_index):
    """
    Create silent audio files based on the duration of an original file.

    This function generates a specified number of silent audio files with the same 
    duration as the original audio file. The silent files are named sequentially 
    starting from the provided start index and saved in the specified output directory.

    Parameters:
    original_file (str): The path to the original audio file to determine the duration.
    output_dir (str): The directory where the silent audio files will be saved.
    count (int): The number of silent audio files to create.
    start_index (int): The starting index for naming the silent audio files.

    Returns:
    None
    """
    duration = float(subprocess.check_output([
        'ffprobe',
        '-v',
        'error',
        '-show_entries',
        'format=duration',
        '-of',
        'default=noprint_wrappers=1:nokey=1',
        original_file]).strip())
    for i in range(1, count + 1):
        output_file = os.path.join(output_dir, f'TRACK{start_index + i}.wav')
        subprocess.run([
            'ffmpeg',
            '-f', 
            'lavfi',
            '-i', 
            'anullsrc=r=44100:cl=mono',
            '-t', 
            str(duration),
            output_file],
            check=False)

def create_silent_stereo_file(original_file, output_dir):
    """
    Create a silent stereo audio file with the same duration as the original file.

    This function generates a silent stereo audio file with the same duration as 
    the specified original audio file. The silent file is saved in the specified 
    output directory with the name 'TRACKM.wav'.

    Parameters:
    original_file (str): The path to the original audio file to determine the duration.
    output_dir (str): The directory where the silent stereo audio file will be saved.

    Returns:
    None
    """
    duration = float(subprocess.check_output([
        'ffprobe',
        '-v', 
        'error',
        '-show_entries',
        'format=duration',
        '-of',
        'default=noprint_wrappers=1:nokey=1', 
        original_file])
        .strip())
    output_file = os.path.join(output_dir, 'TRACKM.wav')
    subprocess.run([
        'ffmpeg',
        '-f', 
        'lavfi', 
        '-i', 
        'anullsrc=r=44100:cl=stereo', 
        '-t',
        str(duration),
        output_file],
        check=False)

def main(input_dir, output_dir, s_name):
    """
    Main function to process WAV files and create a silent audio file, tempo file, and metadata 
    file.

    This function checks the validity of the input directory, clears and prepares the output 
    directory, processes WAV files from the input directory to create silent audio files, 
    generates a tempo text file, and creates a JSON metadata file with track information 
    and the specified song name.

    Parameters:
    input_dir (str): The directory containing the input WAV files.
    output_dir (str): The directory where the processed files will be saved.
    s_name (str): The name of the song to be included in the metadata.

    Returns:
    None
    """
    if not os.path.isdir(input_dir):
        print(f"Input directory '{input_dir}' does not exist")
        sys.exit(1)

    clear_directory(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    wav_files = [f for f in os.listdir(input_dir) if f.endswith('.wav')]
    file_count = len(wav_files)

    if file_count == 0:
        print("No wav files found in the input directory.")
        sys.exit(1)

    wav_files = [os.path.join(input_dir, f) for f in wav_files]

    if file_count == 1:
        create_silent_files(wav_files[0], output_dir, 3, file_count)
        create_silent_stereo_file(wav_files[0], output_dir)
    elif file_count == 2:
        create_silent_files(wav_files[0], output_dir, 2, file_count)
        create_silent_stereo_file(wav_files[0], output_dir)
    elif file_count == 3:
        create_silent_files(wav_files[0], output_dir, 1, file_count)
        create_silent_stereo_file(wav_files[0], output_dir)
    elif file_count == 4:
        create_silent_stereo_file(wav_files[0], output_dir)
    elif file_count == 5:
        pass
    else:
        print("Invalid number of files")
        sys.exit(1)

    track_counter = 1
    file_tracker = {}

    for input_file in wav_files:
        output_file = os.path.join(output_dir, f'TRACK{track_counter}.wav')
        subprocess.run(['ffmpeg', '-i', input_file, '-ac', '1', output_file], check=True)
        file_tracker[f'TRACK{track_counter}']=os.path.basename(input_file)
        track_counter += 1

    tempo_file = os.path.join(output_dir, 'TEMPO.txt')
    with open_file(tempo_file, 'w') as f:
        f.write("""Record:
        Tempo= 138.2011 bpm (Min 59 to max 240)
        QUANTISE= Off (Off or On)
        STEREO= Off   (Off or On)
        Last Play:                  
        TEMPO POT= (0 to 127 or blank)
        OCTAVE= Off    (Off or On)
        REVERSE= Off  (Off or On)
        You can use Notepad to edit this file when importing track files. In that case put value in Record Tempo but leave TEMPO POT value blank.
        """)

    name_file = os.path.join(output_dir, 'NAME.json')
    with open_file(name_file, 'w') as f:
        json.dump({
            "tracks": file_tracker,
            "song_name": s_name
        }, f, indent=4)

    print(f"TEMPO.txt created: {tempo_file}")
    print("Conversion completed.")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python script.py input_directory output_directory song_name")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    song_name = sys.argv[3]

    main(input_directory, output_directory, song_name)
