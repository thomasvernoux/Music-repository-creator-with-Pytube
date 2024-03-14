from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import os
import asyncio
from shazam_api import *

def read_metadata(mp3_file):
    """
    Read metadata from an MP3 file.

    Args:
        mp3_file (str): Path to the MP3 file.

    Returns:
        dict: Dictionary containing the metadata of the MP3 file.
    """
    audiofile = EasyID3(mp3_file)
    return {
        "title": audiofile.get("title", [""])[0],
        "artist": audiofile.get("artist", [""])[0],
        "album": audiofile.get("album", [""])[0],
        "year": audiofile.get("date", [""])[0],
        "genre": audiofile.get("genre", [""])[0]
    }

def write_metadata(mp3_file, metadata):
    """
    Write metadata to an MP3 file.

    Args:
        mp3_file (str): Path to the MP3 file.
        metadata (dict): Dictionary containing the metadata to be written.
    """
    audiofile = EasyID3(mp3_file)
    audiofile["title"] = metadata.get("track_name", "")
    audiofile["artist"] = metadata.get("artist_name", "")
    audiofile["album"] = metadata.get("album_name", "")
    audiofile["date"] = metadata.get("album_year", "")
    audiofile["genre"] = metadata.get("genre", "")
    audiofile.save()

def delete_metadata(mp3_file):
    """
    Delete metadata from an MP3 file.

    Args:
        mp3_file (str): Path to the MP3 file.
    """
    audiofile = MP3(mp3_file)
    audiofile.delete()
    audiofile.save()

def metadata_test(Path):
    """
    Check if an MP3 file contains valid metadata.

    Args:
        Path (str): Path to the MP3 file.

    Returns:
        bool: True if the file contains valid metadata, False otherwise.
    """
    metadata = read_metadata(Path)

    if not metadata:
        return False  # No metadata found

    # Check if any of the required fields (title, artist, album, year) is missing or empty
    required_fields = ["title", "artist", "album", "year"]

    for field in required_fields:
        if not metadata.get(field):
            return False  # Missing or empty required field

    return True

def get_audio_path_list(path):
    """
    Return a list of audio path that need to have a metadata refresh
    """
     

    return_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            # Check if the file has a .mp3 extension
            if file.endswith(".mp3"):

                
                file_path = os.path.join(root, file)
                if not(metadata_test(file_path)):
                    return_paths.append(file_path)
    
    
    return return_paths
  
def metadata_process(Path):

    path_list = get_audio_path_list(Path)

    for Path_song in path_list :
        loop = asyncio.get_event_loop()
        song_info = loop.run_until_complete(get_song_info(Path_song))
        if song_info == None : 
            print(f"song_info == None for : {Path_song}")
            continue
        else :
            write_metadata(Path_song, song_info)

        print("metadata written for : ", Path_song)
    


    
    
    return path_list






"""

directory = "test/Burnin"
for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file has a .mp3 extension
            if file.endswith(".mp3"):
                file_path = os.path.join(root, file)

                metadata = read_metadata(file_path)
                print("Current metadata:", metadata)
                delete_metadata(file_path)
                
                metadata["title"] = "AAA"
                metadata["artist"] = "New Artist"
                metadata["album"] = "New Album"
                metadata["year"] = "2000"
                write_metadata(file_path, metadata)

                delete_metadata(file_path)

"""
