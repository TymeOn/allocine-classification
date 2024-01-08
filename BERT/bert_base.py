import sys
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from transformers import TFCamembertForSequenceClassification, TFAutoModelForSequenceClassification, CamembertTokenizer, AutoTokenizer
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.metrics import SparseCategoricalAccuracy
from keras.callbacks import ModelCheckpoint
from keras.models import load_model

# Data lists
training_data = {'comments': [], 'ratings': []}
validation_data = {'comments': [], 'ratings': []}
prediction_data = {'comments': [], 'ids': []}

# Training data
tree = ET.parse(sys.argv[1])
root = tree.getroot()
for comment in root.findall('.//comment'):
    comment_text = str(comment.find('commentaire').text or "")
    rating_text = comment.find('note').text
    training_data['comments'].append(comment_text)
    training_data['ratings'].append(rating_text)

# Validation data
tree = ET.parse(sys.argv[2])
root = tree.getroot()
for comment in root.findall('.//comment'):
    comment_text = str(comment.find('commentaire').text or "")
    rating_text = comment.find('note').text
    validation_data['comments'].append(comment_text)
    validation_data['ratings'].append(rating_text)

# Prediction data
tree = ET.parse(sys.argv[3])
root = tree.getroot()
for comment in root.findall('.//comment'):
    comment_text = str(comment.find('commentaire').text or "")
    comment_id = str(comment.find("review_id").text)
    prediction_data['comments'].append(comment_text)
    prediction_data['ids'].append(comment_id)

# Create DataFrames from the extracted data
training_data = pd.DataFrame(training_data)
validation_data = pd.DataFrame(validation_data)
prediction_data = pd.DataFrame(prediction_data)

# Convert rating values to numerical format
label_encoder = LabelEncoder()
training_data['ratings'] = label_encoder.fit_transform(training_data['ratings'])
validation_data['ratings'] = label_encoder.fit_transform(validation_data['ratings'])

# Tokenize and encode the comments
tokenizer = CamembertTokenizer.from_pretrained('camembert-base', do_lower_case=True)
training_encoded = tokenizer(list(training_data['comments']), padding=True, truncation=True, max_length=512, return_tensors="tf")
validation_encoded = tokenizer(list(validation_data['comments']), padding=True, truncation=True, max_length=512, return_tensors="tf")
prediction_encoded = tokenizer(list(prediction_data['comments']), padding=True, truncation=True, max_length=512, return_tensors="tf")

# Load CamemBERT model
model = TFCamembertForSequenceClassification.from_pretrained('camembert-base', num_labels=len(label_encoder.classes_))

# Compile the model
model.compile(
    optimizer=Adam(learning_rate=1e-5, epsilon=1e-8),
    loss=SparseCategoricalCrossentropy(from_logits=True),
    metrics=[SparseCategoricalAccuracy(name="accuracy")]
)

# Train the model
model.fit(training_encoded['input_ids'].numpy(), training_data['ratings'], epochs=1, batch_size=12, validation_data=(validation_encoded['input_ids'].numpy(), validation_data['ratings']), shuffle=True)

model.save_pretrained("checkpoints/comments_pretrained")

# Faire des prédictions
predictions = model.predict(prediction_encoded['input_ids'].numpy())

# Convertir les prédictions en classes
predicted_classes = np.argmax(predictions.logits, axis=1)

# Décoder les classes en notes originales
predicted_ratings = label_encoder.inverse_transform(predicted_classes)

# Écrire les prédictions dans un fichier texte
output_file_path = "predictions.txt"  # Chemin du fichier de sortie
with open(output_file_path, 'w') as output_file:
    for i, comment_id in enumerate(prediction_data['ids']):
        output_file.write(f"{comment_id} {predicted_ratings[i]}\n")