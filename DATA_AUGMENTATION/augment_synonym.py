import sys
import xml.etree.ElementTree as ET
import nlpaug.augmenter.word as naw
import nlpaug.flow as naf
import html
from datetime import datetime

data = {'comments': [], 'ratings': []}
augmentations_per_note = {
    '0,5': 86628,
    '1,0': 94774,
    '1,5': 98051,
    '2,0': 69715,
    '2,5': 66281,
    '3,0': 30897,
    '3,5': 27557,
    '4,0': 344,
    '4,5': 60704,
    '5,0': 49097,
}
# augmentations_per_note = {
#     '0,5': 1,
#     '1,0': 1,
#     '1,5': 1,
#     '2,0': 1,
#     '2,5': 1,
#     '3,0': 1,
#     '3,5': 1,
#     '4,0': 1,
#     '4,5': 1,
#     '5,0': 1,
# }

# Training data
tree = ET.parse(sys.argv[1])
root = tree.getroot()
for comment in root.findall('.//comment'):
    comment_text = str(comment.find('commentaire').text or "")
    rating_text = comment.find('note').text
    data['comments'].append(comment_text)
    data['ratings'].append(rating_text)

# Augmentation par substitution de mots
aug_word = naw.ContextualWordEmbsAug(model_path='camembert-base', action='substitute', device='cuda', batch_size=4)

# Augmentation par insertion de caractères
aug_syno = naw.SynonymAug(aug_src='wordnet', lang='fra')

# Augmentation par backtranslation
# aug_back = naw.BackTranslationAug(from_model_name="Helsinki-NLP/opus-mt-fr-en", to_model_name='Helsinki-NLP/opus-mt-en-fr')

# # Combinaison de plusieurs méthodes
aug_flow = naf.Sometimes([aug_syno])

# Appliquer l'augmentation pour obtenir plus d'échantillons
i = 0
j = 0
running = True

while running:
	
	note = str(data['ratings'][i])
	if augmentations_per_note[note] > 0:
		try:
			augmentations_per_note[note] -= 1
			new_comment = ET.Element("comment")
			ET.SubElement(new_comment, 'note').text = note
			ET.SubElement(new_comment, 'commentaire').text = (str(aug_flow.augment(data['comments'][i]))[2:-2]).replace('\\', '').replace(' \' ', '\'').replace(' ’ ', '’')
			root.append(new_comment)
		except Exception as e: 
			print("------------------------------------------------------------------------------------------------")
			print(e)
			print("Current augmentations : " + str(augmentations_per_note))
			print("Current comment id : " + str(i))
			print("Current comment note : " + str(note))
			print("Current comment text : " + str(data['comments'][i]))
			print("------------------------------------------------------------------------------------------------")
			pass

	# Loop around comments
	i = (i + 1) % len(data['comments'])

	if all(aug == 0 for aug in augmentations_per_note.values()):
		running = False

	if j == 0:
		current_time = datetime.now().strftime("%H:%M:%S")
		print("\033c")
		print(augmentations_per_note)
		print("Current Time =", current_time)
		ET.indent(tree, space="\t", level=0)
		tree.write('input/augmented.xml', encoding="UTF-8")

	j = (j + 1) % 10000

ET.indent(tree, space="\t", level=0)
tree.write('input/augmented.xml', encoding="UTF-8")