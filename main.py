"""
Main downloader program

"""



from class_album_artist import *
from functions import *
from clean_url_base import *

from metadata_finder import *

import sys

from downloader_search_function import *
from clean_web_files import *
from globales_variables import *



path = "urls.txt"
thread_number = 10




set_variable_thread_number(thread_number)



if __name__ == "__main__":

    # Utilisation de la fonction
    repertoire_a_purger = 'audio'
    
    # supprimer_fichiers_web(repertoire_a_purger)

    # clean_URL_database(path)

    

    
    # MUSIC_DATA = get_music_data(path)
    # for artist in MUSIC_DATA : 
    #     artist.download_music()
    #     write_music_data(MUSIC_DATA)


    playlist_names = os.listdir("playlists_txt")
    for playlist in playlist_names:
        downloader_search_process(f"playlists_txt/{playlist}")

    update_all_playlists_m3u()

    Path = "audio"
    metadata_process(Path)  


    # Utilisation de la fonction
    repertoire_a_purger = 'audio'
    supprimer_fichiers_web(repertoire_a_purger)

    