
import eyed3
import os

def read_metadata(mp3_file):
    """
    Read metadata from an MP3 file.

    Args:
        mp3_file (str): Path to the MP3 file.

    Returns:
        dict: Dictionary containing the metadata of the MP3 file.
    """
    audiofile = eyed3.load(mp3_file)
    if audiofile.tag is None:
        return {}
    return {
        "title": audiofile.tag.title,
        "artist": audiofile.tag.artist,
        "album": audiofile.tag.album,
        "year": audiofile.tag.getBestDate(),
        "genre": audiofile.tag.genre.name if audiofile.tag.genre else None
    }

def write_metadata(mp3_file, metadata):
    """
    Write metadata to an MP3 file.

    Args:
        mp3_file (str): Path to the MP3 file.
        metadata (dict): Dictionary containing the metadata to be written.
    """
    audiofile = eyed3.load(mp3_file)
    if audiofile.tag is None:
        audiofile.initTag()
    audiofile.tag.title = metadata.get("title")
    audiofile.tag.artist = metadata.get("artist")
    audiofile.tag.album = metadata.get("album")
    audiofile.tag.release_date = metadata.get("year")
    audiofile.tag.genre = metadata.get("genre")
    audiofile.tag.save()

def delete_metadata(mp3_file):
    """
    Delete metadata from an MP3 file.

    Args:
        mp3_file (str): Path to the MP3 file.
    """
    audiofile = eyed3.load(mp3_file)
    if audiofile.tag is not None:
        audiofile.tag.clear()
        audiofile.tag.save()




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
metadata = read_metadata(mp3_file)
print("Current metadata:", metadata)

# Modify metadata
metadata["title"] = "New Title"
metadata["artist"] = "New Artist"
write_metadata(mp3_file, metadata)
print("Modified metadata:", read_metadata(mp3_file))

# Delete metadata
delete_metadata(mp3_file)
print("Metadata after deletion:", read_metadata(mp3_file))


# Modify metadata
metadata["title"] = "New Title"
metadata["artist"] = "New Artist"
metadata["album"] = "New Album"
metadata["year"] = "0000"
write_metadata(mp3_file, metadata)
print("Modified metadata:", read_metadata(mp3_file))

"""
