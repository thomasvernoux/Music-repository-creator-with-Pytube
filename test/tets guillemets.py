

import re

chaine = 'Ma "chaine" de "caracteres"'
chaine_sans_guillemets = re.sub('"', '', chaine)
print(chaine_sans_guillemets)


