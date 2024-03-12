
class Album:
    def __init__(self):
        self.name = None
        self.URL = None
        self.has_to_be_downloaded = None
        return

class Artist:
    def __init__(self):
        self.artist_name = None
        self.albums_list = []
        return

    
def get_data(file):

    ARTISTS_LIST = []               # list of Artists objects

    # Open the file 'urls.txt' for reading
    with open(f'downloader playlist/{file}', 'r') as file:
        # Read each line, remove leading/trailing whitespace, and filter out lines starting with '#'
        lines = file.readlines()

    for line_number in range(len(lines)):
        line = lines[line_number]

        # Check if the line describe an artist
        if line.startswith("Artist :") :
            ARTISTS_LIST.append(Artist())
            ARTISTS_LIST[-1].artist_name = line.split(":")[1].strip()
            continue

        if line.startswith(" ") or line.startswith ("\n")  :
            continue
        
        
        # The album has not to be downloaded
        album = Album()
        line_splited = line.replace("#", "").split(':', 1)
        album.name, album.URL = line_splited
        last_artist = ARTISTS_LIST[-1]
        ARTISTS_LIST[-1].albums_list.append(album)

        # Check if the line start with '#'
        if line[0] == "#":
            album.has_to_be_downloaded = False
        else : 
            album.has_to_be_downloaded = True

    return ARTISTS_LIST

a = get_data("urls copy 2.txt")

b = 3