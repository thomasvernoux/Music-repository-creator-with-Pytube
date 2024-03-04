from pytube import Playlist, YouTube  # Import the Playlist and YouTube classes from the pytube library
from moviepy.editor import AudioFileClip  # Import the AudioFileClip class from the moviepy.editor library
import os  # Import the os module for interacting with the operating system
import re

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

def download_best_audio(playlist_url, folder_name):
    """
    This function is used to download the best audio of a playlist tracks
    input : 
    @playlist URL : Youtube URL of the playlist
    @folder name : download destination
    """

    playlist = Playlist(playlist_url)    # create the playlist object
    for video in playlist.video_urls:  
        yt = YouTube(video)              # create video object
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        if audio_stream:

            # Generate a name for the song
            file_name = f'{yt.title}.mp3'
            
            # Check if the audio file already exist
            test_path = os.path.join('audio', folder_name, remove_special_characters(file_name))
            exist  = os.path.exists(test_path)
            if exist:
                print(f"{file_name} already exists. Skipping...")
                continue  # Go to the next song

            print(f"Downloading {yt.title}...")
            
            # Create directory if it doesn't exist
            if not os.path.exists('audio'):
                os.makedirs('audio')
            output_dir = os.path.join('audio', folder_name)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)


            # Download the audio stream to the 'audio' directory
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

if __name__ == "__main__":

    current_artist = None

    # Open the file 'urls.txt' for reading
    with open('downloader playlist/urls.txt', 'r') as file:
        # Read each line, remove leading/trailing whitespace, and filter out lines starting with '#'
        lines = file.readlines()
    
    # Iterate through each line in the filtered lines
    for line_number in range(len(lines)):
        line = lines[line_number]

        # Check if the line describe an artist
        if line.startswith("Artist :") :
            # this line is the beginning of a new artist section
            current_artist = line.split(":")[1].strip()
            continue

        # Check if the line doesn't start with '#'
        if line[0] == "#":
            # The album has not to be downloaded
            continue
        
        # Check if the line contains ':', indicating a playlist with a name
        if not(':' in line):
            # The line is not an download instruction
            continue


        # Split the line into name and URL
        name, url = line.split(':', 1)
        # Remove leading/trailing whitespace from the name and use it as the folder name
        folder_name = f"{current_artist}/{name.strip()}"
        # Split the URL by ',' if multiple URLs are provided
        playlist_urls = [url.strip() for url in url.split(',')]
        # Iterate through each URL in the playlist_urls list
        for playlist_url in playlist_urls:
            # Call the download_best_audio function with the playlist URL and folder name
            try : 
                download_best_audio(playlist_url, folder_name)
            except Exception as e:
                print("Exception error:", e)
        lines[line_number] = "#" + line[:]

        # Réécrire le fichier avec les lignes modifiées
        with open('downloader playlist/urls.txt', 'w') as file:
            for line in lines:
                file.write(line)

            

    # Réécrire le fichier avec les lignes modifiées
    with open('downloader playlist/urls.txt', 'w') as file:
        for line in lines:
            file.write(line)
                        






            
