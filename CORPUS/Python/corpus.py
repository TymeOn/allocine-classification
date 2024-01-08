import sys
import os
import emoji
import statistics
import matplotlib.pyplot as plt
from langdetect import detect_langs
import xml.etree.ElementTree as ET


if len(sys.argv) > 1 and sys.argv[1] != '':
    input_file = sys.argv[1]

    if os.path.exists(input_file):
        try:
            tree = ET.parse(input_file)
            root = tree.getroot()

        except ET.ParseError as err:
            print(f"Error parsing XML file: {err}")
            sys.exit(1)
    else:
        print('File does not exist')
        sys.exit(1)
else:
    print('Input file expected!')
    sys.exit(1)

noteRepartition = {
    '0.5': 0,
    '1.0': 0,
    '1.5': 0,
    '2.0': 0,
    '2.5': 0,
    '3.0': 0,
    '3.5': 0,
    '4.0': 0,
    '4.5': 0,
    '5.0': 0
}

groupedNoteRepartition = {
    '0.5-1.5': 0,
    '2.0-3.0': 0,
    '3.5-5.0': 0
}

# USER Comment Count Grouped
user_com_count_grouped = {
    '1-50': 0,
    '51-100': 0,
    '101-150': 0,
    '151-200': 0,
    '201-250': 0,
    '251-300': 0,
    '301-350': 0,
    '351-400': 0,
    '401-450': 0,

    # Ajoute d'autres tranches selon tes besoins
}

# MOVIE Comment Count Grouped
movie_com_count_grouped = {
    '1-50': 0,
    '51-100': 0,
    '101-150': 0,
    '151-200': 0,
    '201-250': 0,
    '251-300': 0,
    '301-350': 0,
    '351-400': 0,
    '401-450': 0,
    # Ajoute d'autres tranches selon tes besoins
}

comStorage = {
    'charCount': {},
    'wordCount': {},
    'languageCount': {},
    'emojiCount': {},
}

movieStorage = {}
userStorage = {}
generalResults = ''

movieDistribStorage = {
    'avgNote': {}
}
userDistribStorage = {
    'avgNote': {}
}

for comment in root.findall('comment'):

    # COM CHAR COUNT
    commentaire = comment.find('commentaire').text

    if commentaire is not None:

        commentaire_length = len(commentaire)

        if commentaire_length not in comStorage['charCount']:
            comStorage['charCount'][commentaire_length] = 1
        else:
            comStorage['charCount'][commentaire_length] += 1

        # COM WORD COUNT
        words = commentaire.strip().split()
        wordCount = len(words)

        if wordCount not in comStorage['wordCount']:
            comStorage['wordCount'][wordCount] = 1
        else:
            comStorage['wordCount'][wordCount] += 1

        # COM EMOJI COUNT
        emojiCount = len([c for c in commentaire if c in emoji.EMOJI_DATA])
        if emojiCount not in comStorage['emojiCount']:
            comStorage['emojiCount'][emojiCount] = 1
        else:
            comStorage['emojiCount'][emojiCount] += 1

        # LANGUAGE DETECTION
        try:
            langs = detect_langs(commentaire)

            if langs[0].prob > 0.98:
                lang = langs[0].lang
            else:
                lang = 'fr'

            if lang != 'fr':
                if lang not in comStorage['languageCount']:
                    comStorage['languageCount'][lang] = 1
                else:
                    comStorage['languageCount'][lang] += 1
        except Exception as e:
            print(f"Error detecting language: {e}")
            continue

    note = comment.find('note').text

    if note is not None:

        noteStr = note.replace(',', '.')

        try:
            note = float(noteStr)
        except ValueError:
            print(f"Warning: Invalid note value: {noteStr} in a comment. Skipping.")
            continue

        # MOVIE UNIQUE COUNT & AVERAGE NOTE
        movieId = comment.find('movie').text

        if movieId is not None:
            if movieId not in movieStorage:
                movieStorage[movieId] = {'commentCount': 1, 'totalNote': note, 'notes': [note]}
            else:
                movieStorage[movieId]['commentCount'] += 1
                movieStorage[movieId]['totalNote'] += note
                movieStorage[movieId]['notes'].append(note)

        # USER UNIQUE COUNT & AVERAGE NOTE
        userId = comment.find('user_id').text

        if userId is not None:
            if userId not in userStorage:
                userStorage[userId] = {'commentCount': 1, 'totalNote': note, 'notes': [note]}
            else:
                userStorage[userId]['commentCount'] += 1
                userStorage[userId]['totalNote'] += note
                userStorage[userId]['notes'].append(note)

        noteRepartition[str(note)] += 1

        if 0.5 <= note <= 1.5:
            groupedNoteRepartition['0.5-1.5'] += 1
        elif 2.0 <= note <= 3.0:
            groupedNoteRepartition['2.0-3.0'] += 1
        elif 3.5 <= note <= 5.0:
            groupedNoteRepartition['3.5-5.0'] += 1

for movie_data in movieStorage.values():
    count = movie_data['commentCount']
    if 1 <= count <= 50:
        movie_com_count_grouped['1-50'] += 1
    elif 51 <= count <= 100:
        movie_com_count_grouped['51-100'] += 1
    elif 101 <= count <= 150:
        movie_com_count_grouped['101-150'] += 1
    elif 151 <= count <= 200:
        movie_com_count_grouped['151-200'] += 1
    elif 201 <= count <= 250:
        movie_com_count_grouped['201-250'] += 1
    elif 251 <= count <= 300:
        movie_com_count_grouped['251-300'] += 1
    elif 301 <= count <= 350:
        movie_com_count_grouped['301-350'] += 1
    elif 351 <= count <= 400:
        movie_com_count_grouped['351-400'] += 1
    else:
        movie_com_count_grouped['401-450'] += 1

for user_data in userStorage.values():
    count = user_data['commentCount']
    if 1 <= count <= 50:
        user_com_count_grouped['1-50'] += 1
    elif 51 <= count <= 100:
        user_com_count_grouped['51-100'] += 1
    elif 101 <= count <= 150:
        user_com_count_grouped['101-150'] += 1
    elif 151 <= count <= 200:
        user_com_count_grouped['151-200'] += 1
    elif 201 <= count <= 250:
        user_com_count_grouped['201-250'] += 1
    elif 251 <= count <= 300:
        user_com_count_grouped['251-300'] += 1
    elif 301 <= count <= 350:
        user_com_count_grouped['301-350'] += 1
    elif 351 <= count <= 400:
        user_com_count_grouped['351-400'] += 1
    else:
        user_com_count_grouped['401-450'] += 1
# Process movieStorage
for ms in movieStorage.values():
    average = round(ms['totalNote'] / ms['commentCount'], 1)
    if average not in movieDistribStorage['avgNote']:
        movieDistribStorage['avgNote'][average] = 1
    else:
        movieDistribStorage['avgNote'][average] += 1

# Sort movieDistribStorage by keys
movieDistribStorage['avgNote'] = dict(sorted(movieDistribStorage['avgNote'].items()))

# Process userStorage
for us in userStorage.values():
    average = round(us['totalNote'] / us['commentCount'], 1)
    if average not in userDistribStorage['avgNote']:
        userDistribStorage['avgNote'][average] = 1
    else:
        userDistribStorage['avgNote'][average] += 1

# Général
general_results = f"Nombre de notes : {len(root.findall('comment'))}\n"
general_results += f"Nombre de films uniques : {len(movieStorage)}\n"
general_results += f"Nombre d'utilisateurs uniques : {len(userStorage)}\n"

with open('output/general_results.txt', 'w') as file:
    file.write(general_results)

# Note Répartition
note_repartition_labels = list(noteRepartition.keys())
note_repartition_values = list(noteRepartition.values())

plt.bar(sorted(note_repartition_labels), note_repartition_values)
plt.xlabel('Note')
plt.ylabel('Nombre de commentaires')
plt.title('Répartition des notes')
plt.savefig('output/note_repartition.png')
plt.close()

grouped_note_repartition_labels = list(groupedNoteRepartition.keys())
grouped_note_repartition_values = list(groupedNoteRepartition.values())

plt.bar(grouped_note_repartition_labels, grouped_note_repartition_values)
plt.xlabel('Plage de notes')
plt.ylabel('Nombre de commentaires')
plt.title('Répartition des notes par groupes')
plt.savefig('output/note_repartition_grouped.png')
plt.close()

# COM Char Count
comStorage['charCount'] = dict(sorted(comStorage['charCount'].items(), key=lambda item: item[0]))
com_char_count_labels = list(map(str, comStorage['charCount'].keys()))
com_char_count_values = list(comStorage['charCount'].values())

plt.bar(com_char_count_labels, com_char_count_values)
plt.xlabel('Nombre de caractères')
plt.ylabel('Nombre de commentaires')
plt.title('Répartition du nombre de caractères dans les commentaires')
plt.savefig('output/com_char_count.png')
plt.close()

# COM Word Count
comStorage['wordCount'] = dict(sorted(comStorage['wordCount'].items(), key=lambda item: item[0]))
com_word_count_labels = list(map(str, comStorage['wordCount'].keys()))
com_word_count_values = list(comStorage['wordCount'].values())

plt.bar(com_word_count_labels, com_word_count_values)
plt.xlabel('Nombre de mots')
plt.ylabel('Nombre de commentaires')
plt.title('Répartition du nombre de mots dans les commentaires')
plt.savefig('output/com_word_count.png')
plt.close()

# COM Emoji Count
comStorage['emojiCount'] = dict(sorted(comStorage['emojiCount'].items(), key=lambda item: item[0]))
com_emoji_count_labels = list(map(str, comStorage['emojiCount'].keys()))
com_emoji_count_values = list(comStorage['emojiCount'].values())

plt.bar(com_emoji_count_labels, com_emoji_count_values)
plt.xlabel('Nombre d\'emojis')
plt.ylabel('Nombre de commentaires')
plt.title('Répartition du nombre d\'emojis dans les commentaires')
plt.savefig('output/com_emoji_count.png')
plt.close()

# MOVIE Comment Count
movieStorage = dict(sorted(movieStorage.items(), key=lambda item: item[0]))
movie_com_count_labels = list(map(str, movieStorage.keys()))
movie_com_count_values = [m['commentCount'] for m in movieStorage.values()]

plt.bar(movie_com_count_labels, movie_com_count_values)
plt.xlabel('ID du film')
plt.ylabel('Nombre de commentaires')
plt.title('Nombre de commentaires par film')
plt.savefig('output/movie_com_count.png')
plt.close()

# MOVIE Average Note
movie_avg_note_labels = list(map(str, movieStorage.keys()))
movie_avg_note_values = [round(m['totalNote'] / m['commentCount'], 2) for m in movieStorage.values()]

plt.bar(movie_avg_note_labels, movie_avg_note_values)
plt.xlabel('ID du film')
plt.ylabel('Note moyenne')
plt.title('Note moyenne par film')
plt.savefig('output/movie_avg_note.png')
plt.close()

# USER Comment Count
userStorage = dict(sorted(userStorage.items(), key=lambda item: item[0]))
user_com_count_labels = list(map(str, userStorage.keys()))
user_com_count_values = [u['commentCount'] for u in userStorage.values()]

plt.bar(user_com_count_labels, user_com_count_values)
plt.xlabel('ID de l\'utilisateur')
plt.ylabel('Nombre de commentaires')
plt.title('Nombre de commentaires par utilisateur')
plt.savefig('output/user_com_count.png')
plt.close()

# USER Average Note
user_avg_note_labels = list(map(str, userStorage.keys()))
user_avg_note_values = [round(u['totalNote'] / u['commentCount'], 2) for u in userStorage.values()]

plt.bar(user_avg_note_labels, user_avg_note_values)
plt.xlabel('ID de l\'utilisateur')
plt.ylabel('Note moyenne')
plt.title('Note moyenne par utilisateur')
plt.savefig('output/user_avg_note.png')
plt.close()

# Language Count
com_language_count_labels = list(map(str, comStorage['languageCount'].keys()))
com_language_count_values = list(comStorage['languageCount'].values())

plt.bar(com_language_count_labels, com_language_count_values)
plt.xlabel('Langue')
plt.ylabel('Nombre de commentaires')
plt.title('Répartition des langues dans les commentaires')
plt.savefig('output/com_language_count.png')
plt.close()

# MOVIE Standard Deviation
movie_std_dev_labels = list(map(str, movieStorage.keys()))
movie_std_dev_values = [statistics.pstdev(movie['notes']) for movie in movieStorage.values()]

plt.bar(movie_std_dev_labels, movie_std_dev_values)
plt.xlabel('ID du film')
plt.ylabel('Écart-type des notes')
plt.title('Écart-type des notes par film')
plt.savefig('output/movie_std_dev.png')
plt.close()

# USER Standard Deviation
user_std_dev_labels = list(map(str, userStorage.keys()))
user_std_dev_values = [statistics.pstdev(user['notes']) for user in userStorage.values()]

plt.bar(user_std_dev_labels, user_std_dev_values)
plt.xlabel('ID de l\'utilisateur')
plt.ylabel('Écart-type des notes')
plt.title('Écart-type des notes par utilisateur')
plt.savefig('output/user_std_dev.png')
plt.close()

userDistribStorage['avgNote'] = dict(sorted(userDistribStorage['avgNote'].items()))

movie_avg_note_distrib_labels = list(map(str, movieDistribStorage['avgNote'].keys()))
movie_avg_note_distrib_values = list(movieDistribStorage['avgNote'].values())

plt.bar(movie_avg_note_distrib_labels, movie_avg_note_distrib_values)
plt.xlabel('Note moyenne')
plt.ylabel('Nombre de films')
plt.title('Distribution des notes moyennes par film')
plt.savefig('output/movie_avg_note_distrib.png')
plt.close()

user_avg_note_distrib_labels = list(map(str, userDistribStorage['avgNote'].keys()))
user_avg_note_distrib_values = list(userDistribStorage['avgNote'].values())

plt.bar(user_avg_note_distrib_labels, user_avg_note_distrib_values)
plt.xlabel('Note moyenne')
plt.ylabel('Nombre d\'utilisateurs')
plt.title('Distribution des notes moyennes par utilisateur')
plt.savefig('output/user_avg_note_distrib.png')
plt.close()


# USER Standard Deviation Distribution
user_std_dev_distrib_labels = list(map(str, userStorage.keys()))
user_std_dev_distrib_values = [statistics.pstdev(user['notes']) for user in userStorage.values()]

plt.bar(user_std_dev_distrib_labels, user_std_dev_distrib_values)
plt.xlabel('Écart-type des notes')
plt.ylabel('Nombre d\'utilisateurs')
plt.title('Distribution des écart-types des notes par utilisateur')
plt.savefig('output/user_std_dev_distrib.png')
plt.close()

# MOVIE Standard Deviation Distribution
movie_std_dev_distrib_labels = list(map(str, movieStorage.keys()))
movie_std_dev_distrib_values = [statistics.pstdev(movie['notes']) for movie in movieStorage.values()]

plt.bar(movie_std_dev_distrib_labels, movie_std_dev_distrib_values)
plt.xlabel('Écart-type des notes')
plt.ylabel('Nombre de films')
plt.title('Distribution des écart-types des notes par film')
plt.savefig('output/movie_std_dev_distrib.png')
plt.close()

# COM Word Count
comStorage['wordCount'] = dict(sorted(comStorage['wordCount'].items(), key=lambda item: item[0]))
com_word_count_labels = list(map(str, comStorage['wordCount'].keys()))
com_word_count_values = list(comStorage['wordCount'].values())

plt.hist(com_word_count_values, bins=20, color='orange', alpha=0.7, log=True)
plt.xlabel('Nombre de mots')
plt.ylabel('Nombre de commentaires (échelle logarithmique)')
plt.title('Répartition du nombre de mots dans les commentaires')
plt.savefig('output/com_word_count_log.png')
plt.close()

# COM Word Count (avec échelle logarithmique)
plt.hist(com_word_count_values, bins=20, color='green', alpha=0.7, log=True)
plt.xlabel('Nombre de mots')
plt.ylabel('Nombre de commentaires (échelle logarithmique)')
plt.title('Répartition du nombre de mots dans les commentaires')
plt.savefig('output/com_word_count_log.png')
plt.close()

# USER Comment Count (avec échelle logarithmique)
plt.hist(user_com_count_values, bins=20, color='purple', alpha=0.7, log=True)
plt.xlabel('ID de l\'utilisateur')
plt.ylabel('Nombre de commentaires (échelle logarithmique)')
plt.title('Nombre de commentaires par utilisateur')
plt.savefig('output/user_com_count_log.png')
plt.close()

# MOVIE Standard Deviation (avec échelle logarithmique)
plt.hist(movie_std_dev_values, bins=20, color='blue', alpha=0.7, log=True)
plt.xlabel('ID du film')
plt.ylabel('Écart-type des notes (échelle logarithmique)')
plt.title('Écart-type des notes par film')
plt.savefig('output/movie_std_dev_log.png')
plt.close()

# USER Standard Deviation (avec échelle logarithmique)
plt.hist(user_std_dev_values, bins=20, color='red', alpha=0.7, log=True)
plt.xlabel('ID de l\'utilisateur')
plt.ylabel('Écart-type des notes (échelle logarithmique)')
plt.title('Écart-type des notes par utilisateur')
plt.savefig('output/user_std_dev_log.png')
plt.close()

# USER Average Note Distribution (avec échelle logarithmique)
user_avg_note_distrib_values = list(userDistribStorage['avgNote'].values())

plt.hist(user_avg_note_distrib_values, bins=20, color='orange', alpha=0.7, log=True)
plt.xlabel('Note moyenne')
plt.ylabel('Nombre d\'utilisateurs (échelle logarithmique)')
plt.title('Distribution des notes moyennes par utilisateur')
plt.savefig('output/user_avg_note_distrib_log.png')
plt.close()

# MOVIE Comment Count (avec échelle logarithmique)
plt.hist(movie_com_count_values, bins=20, color='pink', alpha=0.7, log=True)
plt.xlabel('ID du film')
plt.ylabel('Nombre de commentaires (échelle logarithmique)')
plt.title('Nombre de commentaires par film')
plt.savefig('output/movie_com_count_log.png')
plt.close()

# MOVIE Average Note Distribution (avec échelle logarithmique)
movie_avg_note_distrib_values = list(movieDistribStorage['avgNote'].values())

plt.hist(movie_avg_note_distrib_values, bins=20, color='cyan', alpha=0.7, log=True)
plt.xlabel('Note moyenne')
plt.ylabel('Nombre de films (échelle logarithmique)')
plt.title('Distribution des notes moyennes par film')
plt.savefig('output/movie_avg_note_distrib_log.png')
plt.close()

# COM Char Count (avec échelle logarithmique)
com_char_count_values = list(comStorage['charCount'].values())

plt.hist(com_char_count_values, bins=20, color='brown', alpha=0.7, log=True)
plt.xlabel('Nombre de caractères')
plt.ylabel('Nombre de commentaires (échelle logarithmique)')
plt.title('Répartition du nombre de caractères dans les commentaires')
plt.savefig('output/com_char_count_log.png')
plt.close()

# COM Emoji Count (avec échelle logarithmique)
com_emoji_count_values = list(comStorage['emojiCount'].values())

plt.hist(com_emoji_count_values, bins=20, color='gray', alpha=0.7, log=True)
plt.xlabel('Nombre d\'emojis')
plt.ylabel('Nombre de commentaires (échelle logarithmique)')
plt.title('Répartition du nombre d\'emojis dans les commentaires')
plt.savefig('output/com_emoji_count_log.png')
plt.close()

# MOVIE Comment Count Grouped (avec échelle logarithmique)
movie_com_count_grouped_labels =  list(map(str, movie_com_count_grouped.keys()))
movie_com_count_grouped_values = list(movie_com_count_grouped.values())

plt.bar(movie_com_count_grouped_labels, movie_com_count_grouped_values)
plt.xlabel('Nombre de commentaires par film (tranches de 50)')
plt.ylabel('Nombre de films')
plt.title('Répartition du nombre de commentaires par film (groupé)')
plt.savefig('output/movie_com_count_grouped.png')
plt.close()

# USER Comment Count Grouped (avec échelle logarithmique)
user_com_count_grouped_labels = list(map(str, user_com_count_grouped.keys()))
user_com_count_grouped_values = list(user_com_count_grouped.values())

plt.bar(user_com_count_grouped_labels, user_com_count_grouped_values)
plt.xlabel('Nombre de commentaires par utilisateur (tranches de 50)')
plt.ylabel('Nombre d\'utilisateurs')
plt.title('Répartition du nombre de commentaires par utilisateur (groupé)')
plt.savefig('output/user_com_count_grouped.png')
plt.close()
print(noteRepartition)
sys.exit(0)

