
import re

def remove_special_characters(input_string):
    # Remove emojis
    input_string = input_string.encode('ascii', 'ignore').decode('ascii')

    # Define allowed characters including slashes and periods
    allowed_characters = r'[a-zA-Z0-9\s\\/.-]'

    # Remove special characters using regex
    input_string = re.sub(fr'[^{allowed_characters}]', '', input_string)
    input_string = re.sub("'", '', input_string)

    return input_string


print(remove_special_characters("abc''aabbcc"))