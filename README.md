# Project for Managing Music Files

The music-manager project is useful for managing music files on personal computers or storage. It utilizes metadata of files like contributing artist, album, etc that are encoded in music files for organizing the files in a meaningfulway.

## Table of Contents

- [Dependencies](#dependencies)
- [Executables](#executables)
- [Notes](#notes)
- [TODO](#todo)

## Dependencies

### Python Packages

 - ctodd-python-lib-data-structures>=1.0.0
 - ctodd-python-lib-execution>=1.0.0
 - ctodd-python-lib-logging>=1.0.0
 - eyeD3>=0.8.10

## Executables

### [organize_music_by_artist.py](https://github.com/ChristopherHaydenTodd/music-manager/blob/master/music_manager/organize_music_by_artist.py)

```
    Purpose:
        Script responsible for helping organize music files in a
        specified directory and of a specific music filetype
    Steps:
        - Parse Location of Music from CLI
        - Determine Music Extension (Default .mp3)
        - Find all music files in the directory
        - Get the Artist for each File (From metadata, using eyeD3)
        - Create Dir for Each Artist
        - Move each song into the directory

    usage:
        python3.6 organize_music_by_artist.py [-h] --music-dir MUSIC_DIR\
            [--music-format MUSIC_FORMAT]

    example call:
        python3.6 organize_music_by_artist.py --music-dir="~/Music" --music-format=".mp3"
```

## Notes

 - Relies on f-string notation, which is limited to Python3.6.  A refactor to remove these could allow for development with Python3.0.x through 3.5.x

## TODO

 - Unittest framework in place, but lacking tests
