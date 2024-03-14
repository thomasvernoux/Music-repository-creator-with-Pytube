"""
Main downloader program

"""



from class_album_artist import *
from functions import *
from clean_url_base import *

from metadata_finder import *

import sys

from downloader_search_function import *



path = "urls.txt"



if __name__ == "__main__":

    clean_URL_database(path)

    

    
    MUSIC_DATA = get_music_data(path)
    for artist in MUSIC_DATA : 
        artist.download_music()
        write_music_data(MUSIC_DATA)


    playlist_names = ["coups de coeur deezer.txt"]
    for playlist in playlist_names:
        downloader_search_process(playlist)

    update_all_playlists_m3u()

    Path = "audio"
    metadata_process(Path)  

    