from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import re

def remove_special_characters(input_string):
    # Remplacer les emojis par une chaîne vide
    input_string = input_string.encode('ascii', 'ignore').decode('ascii')

    # Supprimer les caractères spéciaux à l'aide d'une expression régulière
    input_string = re.sub(r'[^\w\s.]', '', input_string)

    return input_string

def download_best_audio(video_url, folder_name):
    yt = YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    if audio_stream:
        # Générer le nom de fichier pour la chanson
        file_name = f'audio_{yt.title}.mp3'
        # Vérifier si le fichier existe déjà dans le répertoire cible
        if os.path.exists(os.path.join('audio', folder_name, file_name)):
            print(f"{file_name} already exists. Skipping...")
            return  # Passer à la prochaine chanson

        print(f"Downloading {yt.title}...")
        
        # Create directory if it doesn't exist
        if not os.path.exists('audio'):
            os.makedirs('audio')
        output_dir = os.path.join('audio', folder_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Download the audio stream to the 'audio' directory
        audio_path = audio_stream.download(output_path=output_dir)
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
    with open('playlists.txt', 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip() and not line.startswith('#')]
    
    playlist_name = "None"
    for line in lines:
        if not(":" in line) :
            playlist_name = line
            print("playlist name : ", playlist_name)
        else:
            song_name, song_url = line.split(':', 1)
            download_best_audio(song_url.strip(), playlist_name)
