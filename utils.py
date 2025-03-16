import nltk
nltk.download('punkt', download_dir='/root/nltk_data')
nltk.download('stopwords', download_dir='/root/nltk_data')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import joblib
from pydantic import BaseModel
import os


if not os.path.exists('tfidf_vectorizer.pkl') or not os.path.exists('svm.pkl'):
    raise RuntimeError("Missing model files: Ensure 'tfidf_vectorizer.pkl' and 'svm.pkl' are available")

vectorizer = joblib.load('tfidf_vectorizer.pkl')
svm_model = joblib.load('svm.pkl')



class TextInput(BaseModel):
    content: str

def preprocess_text(content: str):
    """Tiền xử lý văn bản: chuyển thành chữ thường, loại bỏ ký tự đặc biệt, tokenization, stopword removal."""
    content = content.lower()
    content = re.sub(r'[^\w\s]', '', content)  # Loại bỏ dấu câu
    content = re.sub(r'\d+', '', content)  # Loại bỏ số

    # Tokenization
    tokens = word_tokenize(content)

    # Loại bỏ stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    return " ".join(tokens)  # Convert list back to string

def classify_text(content: str):
    """Chuyển đổi văn bản thành vector TF-IDF và dự đoán nhãn."""
    processed_text = preprocess_text(content)
    features = vectorizer.transform([processed_text])  # Cần giữ đầu vào là list
    prediction = svm_model.predict(features)
    prediction_proba = svm_model.predict_proba(features)
    classes = svm_model.classes_
    return {
        "prediction": prediction[0],
        "probability": prediction_proba.tolist(),  # Đảm bảo JSON-friendly
        "classes": list(classes)
    }


class_labels = ['business', 'entertainment', 'politics', 'sport', 'tech']
