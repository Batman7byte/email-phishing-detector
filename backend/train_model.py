import pickle
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import re

# Load dataset
df = pd.read_csv("../dataset/phishing_emails.csv")  # Ensure this file exists

# Preprocessing function
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    return text

df['text'] = df['text'].apply(clean_text)

# Training data
X = df['text']
y = df['label']

# Model pipeline
model_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('classifier', MultinomialNB())
])

model_pipeline.fit(X, y)

# Save the model correctly
with open("model.pkl", "wb") as f:
    pickle.dump(model_pipeline, f)

print("Model trained and saved successfully as model.pkl!")
