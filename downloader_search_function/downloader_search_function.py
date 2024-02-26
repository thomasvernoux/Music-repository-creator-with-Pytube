from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
from pytube import Search

playlist_name = "coups de coeur deezer avec search.txt"

def download_best_audio_from_search(song_name, folder_name):
    results = Search(song_name)
    if len(results.results) > 0:
        yt = results.results[0]
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
            mp3_audio_path = os.path.splitext(audio_path)[0] + '.mp3'
            mp4_audio.write_audiofile(mp3_audio_path)
            mp4_audio.close()

            # Delete the .webm file after conversion
            os.remove(audio_path)
            print(f".webm file deleted for {yt.title}")

            print(f"Conversion to MP3 completed for {yt.title}.")
        else:
            print(f"No audio stream available for {yt.title}.")
    else:
        print(f"No results found for '{song_name}'.")

if __name__ == "__main__":
    with open('downloader_search_function/' + playlist_name, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip() and not line.startswith('#')]
    
    for line in lines:
        download_best_audio_from_search(line, playlist_name)
