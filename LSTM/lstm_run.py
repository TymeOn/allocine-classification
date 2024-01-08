import sys
import xml.etree.ElementTree as ET
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical, pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import load_model

# Loading the training data
tree = ET.parse(sys.argv[1])
root = tree.getroot()

# Extracting the comments and ratings
comments = []
ratings = []

for comment_element in root.findall('.//comment'):
    comment_text = str(comment_element.find('commentaire').text or "")
    rating_text = comment_element.find('note').text
    comments.append(comment_text)
    ratings.append(rating_text)

# Loading the data to predict
tree_test = ET.parse(sys.argv[2]) 
root_test = tree_test.getroot()

# Extracting the comments to predict
comments_test = []
ids_test = []
for comment_element in root_test.findall('.//comment'):
    comment_text = str(comment_element.find('commentaire').text or "")
    comment_id = str(comment_element.find("review_id").text)
    comments_test.append(comment_text)
    ids_test.append(comment_id)


# Encode the notes to numerical values
label_encoder = LabelEncoder()
ratings_encoded = label_encoder.fit_transform(ratings)
ratings_one_hot = to_categorical(ratings_encoded)

# Comments tokenisation and vectorisation
max_words = 1000
tokenizer = Tokenizer(num_words=max_words, split=" ")
tokenizer.fit_on_texts(comments)
X = tokenizer.texts_to_sequences(comments)
X = pad_sequences(X)

# Comments to predict tokenisation and vectorisation
X_test = tokenizer.texts_to_sequences(comments_test)
X_test = pad_sequences(X_test, maxlen=X.shape[1])

# Loading the best model
model = load_model("checkpoints/comments_model.hdf5")

# Predict
predictions = model.predict(X_test)

# Convertir les prédictions en labels
predicted_labels = label_encoder.inverse_transform(predictions.argmax(axis=1))

# Écrire les prédictions dans un fichier texte
output_file_path = "predictions.txt"  # Chemin du fichier de sortie
with open(output_file_path, 'w') as output_file:
    for i, comment_id in enumerate(ids_test):
        output_file.write(f"{comment_id} {predicted_labels[i]}\n")
