


from class_album_artist import *
from functions import *
from clean_url_base import *

import sys
sys.path.append('./downloader_search_function')
from playlist_m3u import *


path = "urls.txt"



if __name__ == "__main__":

    clean_URL_database(path)

    

    
    MUSIC_DATA = get_music_data(path)
    for artist in MUSIC_DATA : 
        artist.download_music()
        write_music_data(MUSIC_DATA)

    update_all_playlists_m3u()

    