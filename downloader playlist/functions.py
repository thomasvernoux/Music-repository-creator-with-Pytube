

from pytube import Playlist, YouTube  # Import the Playlist and YouTube classes from the pytube library
from moviepy.editor import AudioFileClip  # Import the AudioFileClip class from the moviepy.editor library
import os  # Import the os module for interacting with the operating system
import re

from multiprocessing import Pool

def remove_special_characters(input_string):
    """
    This function is used to transform a input string into output string without specials caracters
    
    """

    # Remove emojis
    input_string = input_string.encode('ascii', 'ignore').decode('ascii')

    # Define allowed characters including slashes and periods
    allowed_characters = r'[a-zA-Z0-9\s\\/.-]'

    # Remove special characters using regex
    input_string = re.sub(fr'[^{allowed_characters}]', '', input_string)

    # remove '
    input_string = re.sub("'", '', input_string)
    
    return input_string

def download_and_convert(video_url_folder_name):
    """
    Downloads and converts the audio of a video given its URL and destination folder name.

    Args:
        video_url_folder_name (tuple): A tuple containing the video URL and the folder name.

    Returns:
        None
    """
    # Unpack the tuple into video URL and folder name
    video_url, folder_name = video_url_folder_name
    
    try:
        # Create a YouTube object from the video URL
        yt = YouTube(video_url)
        
        # Get the best audio stream available for the video
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

        if audio_stream:
            # Generate a name for the audio file
            file_name = f'{yt.title}.mp3'
            
            # Check if the audio file already exists
            test_path = os.path.join('audio', folder_name, remove_special_characters(file_name))
            if os.path.exists(test_path):
                print(f"{file_name} already exists. Skipping...")
                return

            print(f"Downloading {yt.title}...")

            # Create necessary directories if they don't exist
            if not os.path.exists('audio'):
                os.makedirs('audio')
            output_dir = os.path.join('audio', folder_name)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Download the audio stream to the specified directory
            audio_path = audio_stream.download(output_path=output_dir)
            print("audio path : ", audio_path)
            print(f"{yt.title} downloaded successfully.")

            # Convert the downloaded audio file to MP3
            mp4_audio = AudioFileClip(audio_path)
            mp3_audio_path = remove_special_characters(os.path.splitext(audio_path)[0] + '.mp3')
            mp4_audio.write_audiofile(mp3_audio_path)
            mp4_audio.close()

            # Delete the .webm file after conversion
            os.remove(audio_path)
            print(f".webm file deleted for {yt.title}")
            print(f"Conversion to MP3 completed for {yt.title}.")
        else:
            print(f"No audio stream available for {yt.title}.")
    except Exception as e:
        print(f"Error processing video URL {video_url}: {e}")

def download_best_audio_playlist(playlist_url, folder_name):
    """
    Downloads the best available audio for each video in the given playlist.

    Args:
        playlist_url (str): The URL of the YouTube playlist.
        folder_name (str): The name of the folder where the audio files will be saved.

    Returns:
        None
    """
    # Create a Playlist object from the playlist URL
    playlist = Playlist(playlist_url)
    
    # Create a list of tuples containing video URL and folder name for each video in the playlist
    video_url_folder_name_list = [(video, folder_name) for video in playlist.video_urls]

    # Use multiprocessing to parallelize the downloading and conversion process
    with Pool() as pool:
        # Map the download_and_convert function to each tuple in the list
        pool.map(download_and_convert, video_url_folder_name_list)






