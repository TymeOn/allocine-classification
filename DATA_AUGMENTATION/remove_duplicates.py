import xml.etree.ElementTree as ET

# Fichier train_modified.xml
train_modified_tree = ET.parse("input/train_save.xml")
train_modified_root = train_modified_tree.getroot()

# Dictionnaire pour stocker les commentaires en fonction de leur contenu
commentaires_doublons = {}

# Parcourir les commentaires dans le fichier train_modified.xml
for commentaire in train_modified_root.findall("./comment"):
    commentaire_texte = commentaire.find("commentaire").text
    key = f"{commentaire_texte}"

    # Si la clé existe déjà, le commentaire est un doublon, l'ajouter au dictionnaire
    if key in commentaires_doublons:
        commentaires_doublons[key].append(commentaire)
        train_modified_root.remove(commentaire)
    else:
        commentaires_doublons[key] = [commentaire]

# # Créer un fichier pour stocker les commentaires identiques
# fichier_doublons = open("input/commentaires_doublons.xml", "w",  encoding="UTF-8")
# fichier_doublons.write('<?xml version="1.0"?>\n<comments>\n')
#
# # Parcourir les clés dans le dictionnaire
# for key, commentaires in commentaires_doublons.items():
#     # Si le commentaire a des doublons, les écrire dans le fichier dédié
#     if len(commentaires) > 1:
#         for commentaire in commentaires:
#             commentaire_str = ET.tostring(commentaire, encoding="unicode")
#             fichier_doublons.write(commentaire_str)
#
# # Fermer le fichier des commentaires identiques
# fichier_doublons.write('</comments>')
# fichier_doublons.close()
# train_modified_tree.write("input/train_sans_doublons_2.xml")