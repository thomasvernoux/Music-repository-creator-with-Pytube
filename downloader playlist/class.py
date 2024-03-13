from functions import *


class Album:
    def __init__(self, Artist = None):
        self.artist = Artist
        self.name = None
        self.URL = None
        self.has_to_be_downloaded = None
        self.folder_name = None
        return
    
    def download(self):
        """
        Download the album
        """
        
        if self.has_to_be_downloaded :
            self.folder_name = f"{self.artist}/{self.name}"
            try : 
                download_best_audio_playlist(self.URL, self.folder_name)
                self.has_to_be_downloaded = False

            except Exception as e:
                print("Exception error:", e)
            

class Artist:
    def __init__(self):
        self.name = None
        self.albums_list = []
        return

    def print_info(self):
        """
        Print in the terminal all artist info (including albums)
        """
        
        print("Artist name : ", self.name)
        for album in self.albums_list :
            print("Album : ", album.name)

    def download_music(self):

        for album in self.albums_list :
            album.download()
            global MUSIC_DATA
            write_music_data(MUSIC_DATA, path = "URL.txt")




def get_music_data(file):
    """
    Return a list of Artist class
    """

    ARTISTS_LIST = []               # list of Artists objects

    # Open the file 'urls.txt' for reading
    with open(f'downloader playlist/{file}', 'r') as file:
        # Read each line, remove leading/trailing whitespace, and filter out lines starting with '#'
        lines = file.readlines()

    for line_number in range(len(lines)):
        line = lines[line_number]

        # Check if the line describe an artist
        if line.startswith("Artist :") :
            artist_name = line.split(":")[1].strip()
            ARTISTS_LIST.append(Artist())
            ARTISTS_LIST[-1].name = artist_name
            #print(artist_name)
            continue

        if line.startswith(" ") or line.startswith ("\n")  :
            continue
        
        
        
        album = Album(artist_name)
        line_splited = line.replace("#", "").split(' : ', 1)
        album.name, album.URL = line_splited
        last_artist = ARTISTS_LIST[-1]
        album.URL = album.URL.replace("\n", "")
        ARTISTS_LIST[-1].albums_list.append(album)

        """
        Debug
        """
        if album.name.startswith("Complete"):
            a = 3

        # Check if the line start with '#'
        if line[0] == "#":
            album.has_to_be_downloaded = False
        else : 
            album.has_to_be_downloaded = True
    return ARTISTS_LIST

def write_music_data(DATA, path = "URL.txt"):

    file = open(path, 'w')

    for Artist in DATA : 
        file.write(f"Artist : {Artist.name}\n")
        for Album in Artist.albums_list :
            if Album.has_to_be_downloaded == False : 
                file.write("#")
            file.write(f"{Album.name} : {Album.URL}\n")
        file.write(f"\n")
    
    file.close()


path = "urls.txt"

if __name__ == "__main__":

    global MUSIC_DATA
    MUSIC_DATA = get_music_data(path)
    for artist in MUSIC_DATA : 
        artist.download_music()

    write_music_data(MUSIC_DATA, path = f"downloader playlist/{path}")
        

