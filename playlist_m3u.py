
import os



def create_playlist_m3u(directory_path, playlist_name):
    # Vérifier si le répertoire existe
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        print(f"Le répertoire {directory_path} n'existe pas.")
        return

    # Créer la playlist M3U
    playlist_path = os.path.join(directory_path, playlist_name, playlist_name + '.m3u')
    with open(playlist_path, 'w') as playlist_file:
        # Parcourir le répertoire et ses sous-répertoires
        for file in os.listdir(f"{directory_path}/{playlist_name}"):
            if file.endswith(".mp3"):
                playlist_file.write(f"{file}\n")

    print(f"Playlist M3U créée avec succès : {playlist_path}")


def update_playlists_m3u_in_directory(directory):
    dir_list = os.listdir(directory)
    for playlist in dir_list :
        create_playlist_m3u(directory, playlist)


    return 

def update_all_playlists_m3u():
    Directories = ["audio/Playlists"
                    ]

    for directory in Directories : 
        update_playlists_m3u_in_directory(directory)

