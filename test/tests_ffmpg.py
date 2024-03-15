import os
import ffmpeg


def convert_to_mp3(input_file, output_file):
    """
    Convert a .webm file to .mp3 using ffmpeg-python.

    Args:
        input_file (str): Chemin du fichier d'entrée .webm.
        output_file (str): Chemin du fichier de sortie .mp3.

    Returns:
        None
    """
    # Définit les paramètres de l'entrée et de la sortie
    input_stream = ffmpeg.input(input_file)
    output_stream = ffmpeg.output(input_stream, output_file, acodec='libmp3lame', ab='192k')

    try:
        # Exécute la commande ffmpeg
        ffmpeg.run(output_stream, overwrite_output=True)
        print(f"Conversion de {input_file} en {output_file} terminée avec succès.")
    except ffmpeg.Error as e:
        print(f"Erreur lors de la conversion de {input_file} en {output_file}: {e}")

directory = r"./audio"
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".webm"):
            input_file = os.path.join(root, file)
            output_file = os.path.join(root, os.path.splitext(file)[0] + ".mp3")
            convert_to_mp3(input_file, output_file)

