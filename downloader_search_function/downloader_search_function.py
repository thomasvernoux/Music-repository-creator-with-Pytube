from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
from pytube import Search
import re
import traceback


playlist_name = "z footing 32.txt"


def remove_special_characters(input_string):
    # Remplacer les emojis par une chaîne vide
    input_string = input_string.encode('ascii', 'ignore').decode('ascii')

    # Supprimer les caractères spéciaux à l'aide d'une expression régulière
    input_string = re.sub(r'[^\w\s./\\]', '', input_string)

    return input_string

def download_best_audio_from_search(song_name, folder_name):
    results = Search(song_name)

    if len(results.results) == 0:
        print("no clip available")
        return 
    
    yt = results.results[0]    # keep the tube with the best fit according to search

    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

    if audio_stream:
        # Générer le nom de fichier pour la chanson
        file_name = f'{yt.title}.mp3'
        
        # Vérifier si le fichier existe déjà dans le répertoire cible
        if os.path.exists(os.path.join(folder_name, remove_special_characters(file_name))):
            print(f"{file_name} already exists. Skipping...")
            return  # Passer à la prochaine chanson

       
        # download directory
        output_dir = os.path.join(os.getcwd(), f'audio\{folder_name}')
        print("output dir : ", output_dir)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # download the audio
        print(f"Downloading {yt.title}...")
        # Download the audio stream to the 'audio' directory
        audio_path = audio_stream.download(output_path=output_dir, filename=f"{remove_special_characters(yt.title)}.webm")
        print(f"{yt.title} downloaded successfully.")
        print("audio path : ", audio_path)
        
        
        

        # Charger le fichier .webm
        clip = AudioFileClip(audio_path)


        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        # Ajouter l'extension .mp3
        mp3_filename = base_name + ".mp3"
        # Écrire le fichier .mp3
        clip.write_audiofile(f"{output_dir}\{mp3_filename}")

        # Fermer le clip
        clip.close()


        # Delete the .webm file after conversion
        os.remove(audio_path)
        print(f".webm file deleted for {yt.title}")

        print(f"Conversion to MP3 completed for {yt.title}.")
    else:
        print(f"No audio stream available for {yt.title}.")


if __name__ == "__main__":
    with open('downloader_search_function/' + playlist_name, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip() and not line.startswith('#')]

    for line in lines:
        try : 
            foldername = base_name = os.path.splitext(playlist_name)[0]
            download_best_audio_from_search(line, foldername)
        except Exception as e:
            # Capturer l'exception et imprimer la trace
            print("Une exception s'est produite :")
            traceback.print_exc()
















        
