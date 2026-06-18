import json
import string 
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer 
from sklearn.metrics.pairwise import cosine_similarity


import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    tokens = [w for w in tokens if w not in stop_words]
    return " ".join(tokens)

with open(resource_path("Ecommerce_FAQ_Chatbot_dataset.json"), "r", encoding="utf-8") as f:
    faq_data = json.load(f)

model = SentenceTransformer('all-MiniLM-L6-v2')

faq_questions = []
faq_answers = []

for item in faq_data["questions"]:
    faq_questions.append(preprocess(item["question"]))
    faq_answers.append(item["answer"])

faq_vectors = model.encode(faq_questions)

def get_answer(user_question):
    processed = preprocess(user_question)
    user_vector = model.encode([processed])
    similarities = cosine_similarity(user_vector, faq_vectors)[0]
    best_match = similarities.argmax()
    if similarities[best_match] > 0.4:
        return faq_answers[best_match]
    else:
        return "Sorry, I don't have an answer for that."

if __name__ == "__main__":
    print("Running in terminal mode...")