
import os



def create_playlist_m3u(directory_path, playlist_name):
    # Vérifier si le répertoire existe
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        print(f"Le répertoire {directory_path} n'existe pas.")
        return

    # Créer la playlist M3U
    playlist_path = os.path.join(directory_path, playlist_name + '.m3u')
    with open(playlist_path, 'w') as playlist_file:
        # Parcourir le répertoire et ses sous-répertoires
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                # Vérifier si le fichier est une musique (extension MP3, WAV, etc.)
                if file.endswith(('.mp3', '.wav', '.flac', '.aac', '.ogg')):
                    # Écrire le chemin relatif de la musique dans la playlist M3U
                    relative_path = os.path.relpath(os.path.join(root, file), directory_path)
                    playlist_file.write(relative_path + '\n')

    print(f"Playlist M3U créée avec succès : {playlist_path}")


