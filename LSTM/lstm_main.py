import sys
import xml.etree.ElementTree as ET
import keras.models as models
import keras.layers as layers
import keras.optimizers as optimizers
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical, pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split

# Callbacks : ModelCheckpoint
callbacks = [
    ModelCheckpoint(
        "checkpoints/comments_model.hdf5",
        monitor="categorical_accuracy",
        mode="max",
        save_best_only=True,
    ),
]

# Loading the data
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

# Dividing the data
X_train, X_test, y_train, y_test = train_test_split(X, ratings_one_hot, test_size=0.2, random_state=42)

# Creating the model
model = models.Sequential()
model.add(layers.Embedding(max_words, 128, input_length=X.shape[1]))
model.add(layers.LSTM(100))
model.add(layers.Dense(10, activation='softmax'))

# Building the model
model.compile(optimizer=optimizers.Adam(), loss="categorical_crossentropy", metrics=["categorical_accuracy"])

# Training model
model.fit(X_train, y_train, epochs=10, batch_size=10, verbose=1, validation_data=(X_test, y_test), callbacks=[callbacks])

# Loading the best model
model = load_model("checkpoints/comments_model.hdf5")

# Evaluating the model
loss, categorical_accuracy = model.evaluate(X_test, y_test)
print(f'Loss: {loss}, Categorical accuracy: {categorical_accuracy}')
