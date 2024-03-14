



from class_album_artist import *


def clean_URL_database(database_path) :

    DATA = get_music_data(database_path)

    print(DATA)


    ArtistName__artist_class_object = []
    for A in DATA : 
        ArtistName__artist_class_object.append([A.name, A])



    print(ArtistName__artist_class_object)
    ArtistName__artist_class_object = sorted(ArtistName__artist_class_object)
    print("SORT : ", ArtistName__artist_class_object)


    sorted_DATA = []
    for D in ArtistName__artist_class_object:
        sorted_DATA.append(D[1])


    write_music_data(sorted_DATA)

    return 
