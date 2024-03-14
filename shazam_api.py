import asyncio
from shazamio import Shazam, Serialize
import os



async def get_song_info(Path):
    """
    Retrieves information about a song from Shazam given its audio file path.

    Args:
        Path (str): The file path of the audio file.

    Returns:
        dict: A dictionary containing information about the song, including
              its name, artist, album name, album year, and genre.
    """
    # Initialize an empty dictionary to store song information
    song_info = {}

    # Create a Shazam instance
    shazam = Shazam()


    # Recognize the song using the audio file path
    out = await shazam.recognize(Path)  # rust version, use this!

    if out["matches"] == []:
        print(f"no resumts for this song : {Path}")
        return None

    # Extract the track ID from the recognition result
    track_id = out['track']['key']

    # Get detailed information about the track using its ID
    about_track = await shazam.track_about(track_id=track_id)

    # Retrieve the album ID from the track information
    album_id = about_track.get("albumadamid")

    # Check if the track information contains sections and metadata
    if about_track and 'sections' in about_track:
        for section in about_track['sections']:
            # Check if the section is of type 'SONG' and contains metadata
            if section.get('type') == 'SONG' and 'metadata' in section:
                for metadata in section['metadata']:
                    # Check each metadata entry for specific information
                    if metadata.get('title') == 'Album':
                        # Extract and store the album name
                        song_info["album_name"] = metadata.get('text')
                    elif metadata.get('title') == 'Released':
                        # Extract and store the album year
                        song_info["album_year"] = metadata.get('text')
                    elif metadata.get('title') == 'Genre':
                        # Extract and store the genre of the song
                        song_info["genre"] = metadata.get('text')

    # Extract and store the name of the song
    song_info["track_name"] = out.get('track', {}).get('title', "")

    # Extract and store the name of the artist
    song_info["artist_name"] = out.get('track', {}).get('subtitle', "")

    return song_info




"""
directory = "test/Burnin"
for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file has a .mp3 extension
            if file.endswith(".mp3"):
                # Construct the full path to the MP3 file
                mp3_path = os.path.join(root, file)
                loop = asyncio.get_event_loop()
                song_info = loop.run_until_complete(get_song_info(mp3_path))
                print(song_info)
                

"""

