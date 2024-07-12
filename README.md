## Background

The Electro Harmonix 45000 looper is a fabulous multitrack looper which allows a musician to record sounds into one of 4 tracks and mix them together. As a live looper, it works quite seamlessly for a user. One dimension of its use that I want to explore is as a 4 track playback device. I want to load the 45000 with stems and play them back for live performance, taking advantage of its performance functions, memory and immediacy.

To do this requires alot of tedious folder management and precise operations. I would like to streamline this process by creating a set of tools that can spin up a properly formatted loop entries that can be put on an SD card and played back.

## Function 1: Create Looper Directory

Creates a new looper directory with proper file formatting and directory structure

## Usage
create.sh input_directory output_directory song_name

input_directory  - specifies the files which will be used for the looper directory
output_directory - specifies where the directory should be created
song_name        - specifies what song this loop is associated with

## Function 2: Visualize Looper Directory (In Progress)

Visualizes the entire looper card and displays the relevant song and track structure for each loop

## Usage
visualize.sh

## Dependencies

This is a python based project, with some bash scripting as well.

## Next Features

- Silencing or enabling the console output from ffmpeg
- some tool to manage the naming and ordering of output files in the directory
- improved batch processing that specifies a range of input and output files [raw1...raw2] [LOOP02...LOOP03]
