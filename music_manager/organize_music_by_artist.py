#!/usr/bin/env python3.6
"""
    Purpose:
        Parse Music Files
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
"""

# Python Library Imports
import eyed3
import logging
import os
import re
import shutil
import sys
from argparse import ArgumentParser
from data_structure_helpers import string_helpers
from execution_helpers import function_executors
from logging_helpers import loggers


###
# Main Execution
###


@function_executors.main_executor
def main():
    """
    Purpose:
        Get File Metadata
    """
    logging.info("Starting Process Organize Music By Artist")

    cli_args = get_cli_arguments()

    music_files = find_music_files(cli_args.music_dir, cli_args.music_format)
    if not music_files:
        logging.info("No music files found in the directory, exiting")
        return

    music_by_artist = get_music_by_artist(music_files)
    if len(music_by_artist) == 1:
        logging.info(
            f"Only one artist, not going to organize: {list(music_by_artist.keys())[0]}"
        )
        return

    for artist, artist_details in music_by_artist.items():

        artist_dir = os.path.join(
            cli_args.music_dir, string_helpers.convert_to_title_case(artist)
        )

        try:
            os.mkdir(artist_dir)
        except FileExistsError as file_err:
            # logging.debug(f"{artist_dir} already exists, no need to create")
            pass
        except Exception as err:
            logging.exception(f"Exception Creating Dir: {err}")
            raise err

        for song in artist_details["songs"]:
            shutil.move(song, artist_dir)

    logging.info("Process Organize Music By Artist Complete")


###
# Music Parsing
###


def find_music_files(music_dir, music_format):
    """
    Purpose:
        Find music files in specified dir
    Args:
        music_dir (String): Dir to search for music files
        music_format (String): Format/Extension of music files
    Return:
        music_files (List of Strings): List of music files in the dir (filenames)
    """

    return [
        os.path.join(music_dir, filename)
        for filename in os.listdir(music_dir)
        if os.path.isfile(os.path.join(music_dir, filename))
        and filename.endswith(music_format)
    ]


def get_music_by_artist(music_files):
    """
    Purpose:
        Take list of filenames of music files and organize into a dict
        with the key of the artist name and a list of songs as the value.
    Args:
        music_files (List of Strings): List of music filenames
    Return:
        music_by_artist (Dict): dict with the key of the artist name and
            a list of songs as the value.
    """

    music_by_artist = {}
    for music_file in music_files:

        music_file_metadata = eyed3.load(music_file)

        artist = get_artist_for_music_file(music_file, music_file_metadata)

        music_by_artist.setdefault(artist, {"songs": [], "total_songs": 0})
        music_by_artist[artist]["songs"].append(music_file)
        music_by_artist[artist]["total_songs"] += 1

    return music_by_artist


def get_artist_for_music_file(music_file, music_file_metadata):
    """
    Purpose:
        Get the artist from metadata of a music file
    Args:
        music_file (String): Full name of the music file
        music_file_metadata (EyeD3 Object): Object of EyeD3, which has the metadata of
            the file that can be used to get the artist
    Return:
        artist (String): Artist name, "Unknown" if it is not found
    """

    try:
        artist = music_file_metadata.tag.artist.lower()
    except Exception as err:
        logging.debug(f"No Arist Tag For Music: {music_file}")
        artist = "unknown"

    return artist


###
# Scrpt Configuration Functions
###


def get_cli_arguments():
    """
    Purpose:
        Parse CLI arguments for script
    Args:
        N/A
    Return:
        N/A
    """
    logging.info("Getting and Parsing CLI Arguments")

    parser = ArgumentParser(description="Organize Music Files")
    required = parser.add_argument_group("Required Arguments")
    optional = parser.add_argument_group("Optional Arguments")

    # Required Arguments\
    required.add_argument(
        "--music-dir",
        dest="music_dir",
        help="Dir of Music Files",
        required=True,
        type=str,
    )

    # Optional Arguments
    optional.add_argument(
        "--music-format",
        dest="music_format",
        default=".mp3",
        help="Format of Music Files",
        required=False,
        type=str,
    )

    return parser.parse_args()


if __name__ == "__main__":

    try:
        loggers.get_stdout_logging(
            log_level=logging.INFO,
            log_prefix="[parse_music_files] "
        )
        main()
    except Exception as err:
        logging.exception(f"{os.path.basename(__file__)} failed due to error: {err}")
        raise err
