from pytube import Playlist, YouTube  # Import the Playlist and YouTube classes from the pytube library
from moviepy.editor import AudioFileClip  # Import the AudioFileClip class from the moviepy.editor library
import os  # Import the os module for interacting with the operating system
import re

def remove_special_characters(input_string):
    # Remove emojis
    input_string = input_string.encode('ascii', 'ignore').decode('ascii')

    # Define allowed characters including slashes and periods
    allowed_characters = r'[a-zA-Z0-9\s\\/.-]'

    # Remove special characters using regex
    input_string = re.sub(fr'[^{allowed_characters}]', '', input_string)

    return input_string

def download_best_audio(playlist_url, folder_name):
    playlist = Playlist(playlist_url)
    for video in playlist.video_urls:
        yt = YouTube(video)
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        if audio_stream:

            # Générer le nom de fichier pour la chanson
            file_name = f'audio_{yt.title}.mp3'
            print("Songname without special charracters : ", remove_special_characters(yt.title))
            
            # Vérifier si le fichier existe déjà dans le répertoire cible
            if os.path.exists(os.path.join('audio', folder_name, file_name)):
                print(f"{file_name} already exists. Skipping...")
                continue  # Passer à la prochaine chanson

            print(f"Downloading {yt.title}...")
            
            # Create directory if it doesn't exist
            if not os.path.exists('audio'):
                os.makedirs('audio')
            output_dir = os.path.join('audio', folder_name)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)



            # Check if the audio file already exists in the target directory or any subdirectories
            mp3_file_found = False
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    if file.endswith('.mp3') and file.startswith(yt.title):
                        mp3_file_found = True
                        break
                if mp3_file_found:
                    break
            
            if mp3_file_found:
                print(f"{yt.title} is already downloaded. Skipping...")
                continue


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

    # Créer une liste pour stocker les lignes modifiées
    modified_lines = []


    # Open the file 'urls.txt' for reading
    with open('downloader playlist/urls.txt', 'r') as file:
        # Read each line, remove leading/trailing whitespace, and filter out lines starting with '#'
        lines = file.readlines()
    
    # Iterate through each line in the filtered lines
    for line_number in range(len(lines)):
        line = lines[line_number]
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
                    try : 
                        download_best_audio(playlist_url, folder_name)
                    except Exception as e:
                        print("Exception error:", e)
                lines[line_number] = "#" + line[:]
            print("lines : ", lines)

        # Réécrire le fichier avec les lignes modifiées
        with open('downloader playlist/urls.txt', 'w') as file:
            for line in lines:
                file.write(line)

            

    # Réécrire le fichier avec les lignes modifiées
    with open('downloader playlist/urls.txt', 'w') as file:
        for line in modified_lines:
            file.write(line)
                        






            
