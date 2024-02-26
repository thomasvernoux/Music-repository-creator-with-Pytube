from pytube import Playlist, YouTube  # Import the Playlist and YouTube classes from the pytube library
from moviepy.editor import AudioFileClip  # Import the AudioFileClip class from the moviepy.editor library
import os  # Import the os module for interacting with the operating system

def download_best_audio(playlist_url, folder_name):
    playlist = Playlist(playlist_url)
    for video in playlist.video_urls:
        yt = YouTube(video)
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        if audio_stream:
            print(f"Downloading {yt.title}...")
            # Create directory if it doesn't exist
            if not os.path.exists('audio'):
                os.makedirs('audio')
            output_dir = os.path.join('audio', folder_name)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # Download the audio stream to the 'audio' directory
            audio_path = audio_stream.download(output_path=output_dir, filename_prefix='audio_')
            print(f"{yt.title} downloaded successfully.")

            # Convert the downloaded audio file to MP3
            mp4_audio = AudioFileClip(audio_path)
            mp3_audio_path = os.path.splitext(audio_path)[0] + '.mp3'
            mp4_audio.write_audiofile(mp3_audio_path)
            mp4_audio.close()

            # Delete the .webm file after conversion
            os.remove(audio_path)
            print(f".webm file deleted for {yt.title}")

            print(f"Conversion to MP3 completed for {yt.title}.")
        else:
            print(f"No audio stream available for {yt.title}.")

if __name__ == "__main__":
    # Open the file 'urls.txt' for reading
    with open('urls.txt', 'r') as file:
        # Read each line, remove leading/trailing whitespace, and filter out lines starting with '#'
        lines = [line.strip() for line in file.readlines() if line.strip() and not line.startswith('#')]
    
    # Iterate through each line in the filtered lines
    for line in lines:
        # Check if the line doesn't start with '#'
        if line[0] != "#":
            # Check if the line contains ':', indicating a playlist with a name
            if ':' in line:
                # Split the line into name and URL
                name, url = line.split(':', 1)
                # Remove leading/trailing whitespace from the name and use it as the folder name
                folder_name = name.strip()
                # Split the URL by ',' if multiple URLs are provided
                playlist_urls = [url.strip() for url in url.split(',')]
                # Iterate through each URL in the playlist_urls list
                for playlist_url in playlist_urls:
                    # Call the download_best_audio function with the playlist URL and folder name
                    download_best_audio(playlist_url, folder_name)
            else:
                # Call the download_best_audio function with the URL and an empty folder name
                download_best_audio(line, '')
