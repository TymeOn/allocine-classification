```python
import xml.etree.ElementTree as ET
import sys
import os

# Charger le XML
tree = ET.parse('input/train.xml')
root = tree.getroot()

# Compteur pour suivre le nombre de commentaires ajoutés
comments_added_4_5 = 0
comments_added_2_5 = 0
comments_added_2_0 = 0
comments_added_5_0 = 0

# Parcourir les commentaires
for comment in root.findall('.//comment'):

    # Récupérer la note du commentaire
    note = comment.find('note').text

    noteStr = note.replace(',', '.')

    try:
        note = float(noteStr)
    except ValueError:
        print(f"Warning: Invalid note value: {noteStr} in a comment. Skipping.")
        continue

    # Dupliquer les commentaires avec une note de 0.5
    if note == 0.5 or note == 1.0 or note == 1.5:
        new_comment = ET.Element('comment')
        new_comment.extend(comment)
        root.append(new_comment)

    # Ajouter un tiers des commentaires avec une note de 4.5
    if note == 4.5 and comments_added_4_5 < 21432:  # 1/3 de 64296
        new_comment = ET.Element('comment')
        new_comment.extend(comment)
        root.append(new_comment)
        comments_added_4_5 += 1

    # Ajouter un tiers des commentaires avec une note de 4.5
    if note == 5.0 and comments_added_5_0 < 25301:  # 1/3 de 64296
        new_comment = ET.Element('comment')
        new_comment.extend(comment)
        root.append(new_comment)
        comments_added_5_0 += 1

    # Ajouter un tiers des commentaires avec une note de 4.5
    if note == 2.0 and comments_added_2_0 < 18428:  # 1/3 de 64296
        new_comment = ET.Element('comment')
        new_comment.extend(comment)
        root.append(new_comment)
        comments_added_2_0 += 1

    # Ajouter un tiers des commentaires avec une note de 4.5
    if note == 2.5 and comments_added_2_5 < 19573:  # 1/3 de 64296
        new_comment = ET.Element('comment')
        new_comment.extend(comment)
        root.append(new_comment)
        comments_added_2_5 += 1

# Enregistrer le nouveau XML
tree.write('input/train_duplicate.xml')
```