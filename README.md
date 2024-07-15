## Background

The Electro Harmonix 45000 looper is a fabulous multitrack looper which allows a musician to record sounds into one of 4 tracks and mix them together. As a live looper, it works quite seamlessly for a user. One dimension of its use that I want to explore is as a 4 track playback device. I want to load the 45000 with stems and play them back for live performance, taking advantage of its performance functions, memory and immediacy.

To do this requires alot of tedious folder management and precise operations. I would like to streamline this process by creating a set of tools that can spin up a properly formatted loop entries that can be put on an SD card and played back.

### Functions

#### Create

Creates a new looper directory with proper file formatting and directory structure. It also creates a file called NAME.json which gives information about the loop like the song name and the original filenames which gives more information about what is contained in each track.

```create.py input_directory output_directory song_name```

where create.py takes three arguments:

- ```input_directory```  - specifies the files which will be used to create the loop directory
- ```output_directory``` - specifies where the loop directory should be created
- ```song_name```        - specifies what song this loop is associated with

#### Visualize

Visualizes the entire looper directory and displays the relevant song and track structure for each loop

```visualize.py```

currently hardcoded to my personal drive, but could be configured to operate anywhere. Produces results in the following format:

<img width="568" alt="Screen Shot 2024-07-15 at 12 57 38 PM" src="https://github.com/user-attachments/assets/999a6dc9-9b3c-4901-8e8e-1d74f7c64374">

#### Swap

Swaps the names of the two given files. Also reflects this change in the NAME.json file.

```swap.py file1 file2```

This function is useful for reorganizing a loop entry. Say you want all of your drums on TRACK1. This function can help you do that.

## Next Features

- Silencing or enabling the console output from ffmpeg
- some tool to manage the naming and ordering of output files in the directory
- improved batch processing that specifies a range of input and output files [raw1...raw2] [LOOP02...LOOP03]
- implement a swap function that would be a rudimentary way to manipulate the ordering of tracks in a looper entry by swapping the positions of two specified loops
