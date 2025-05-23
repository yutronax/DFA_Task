from datasets import load_dataset
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# veri setini Hugging Face'ten  çekiyoruz:

# ds = load_dataset("SetFit/bbc-news")
# ds["train"].to_csv("train.csv", index=False)
# ds["test"].to_csv("test.csv", index=False)

# Kaydedilmiş csv dosyalarından veriyi yüklüyoruz
egitim_verisi = pd.read_csv('train.csv') 
test_verisi = pd.read_csv('test.csv')

print("Eğitim verisi sütunları:", egitim_verisi.columns)

# Metin temizleme fonksiyonu: küçük harfe çevirir, rakamları ve noktalama işaretlerini temizler
def temizle(metin):
    metin = metin.lower()
    metin = re.sub(r'\d+', '', metin)               # Rakamları kaldır
    metin = re.sub(r'[^\w\s]', '', metin)           # Harf ve boşluk dışı karakterleri temizle
    return metin

egitim_verisi['text'] = egitim_verisi['text'].astype(str).apply(temizle)
test_verisi['text'] = test_verisi['text'].astype(str).apply(temizle)

# TF-IDF ile metinleri sayısal vektörlere çeviriyoruz
tfidf = TfidfVectorizer(stop_words='english', max_df=0.7)
X_train = tfidf.fit_transform(egitim_verisi['text'])
X_test = tfidf.transform(test_verisi['text'])

y_train = egitim_verisi['label_text']
y_test = test_verisi['label_text']

# Naive Bayes Modelini Eğitip Test Ediyoruz
nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)
y_pred_nb = nb_model.predict(X_test)

print("\n--- Naive Bayes Sonuçları ---")
print("Doğruluk:", accuracy_score(y_test, y_pred_nb))
print(classification_report(y_test, y_pred_nb))

plt.figure(figsize=(6,4))
sns.heatmap(confusion_matrix(y_test, y_pred_nb), annot=True, fmt='d', cmap='Blues')
plt.title("Naive Bayes - Karışıklık Matrisi")
plt.xlabel("Tahmin")
plt.ylabel("Gerçek")
plt.show()

# Lojistik Regresyon Modelini Eğitip Test Ediyoruz
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)

print("\n--- Lojistik Regresyon Sonuçları ---")
print("Doğruluk:", accuracy_score(y_test, y_pred_lr))
print(classification_report(y_test, y_pred_lr))

plt.figure(figsize=(6,4))
sns.heatmap(confusion_matrix(y_test, y_pred_lr), annot=True, fmt='d', cmap='Greens')
plt.title("Lojistik Regresyon - Karışıklık Matrisi")
plt.xlabel("Tahmin")
plt.ylabel("Gerçek")
plt.show()

# Modellerin genel doğruluklarını karşılaştıralım
print("\n--- Modellerin Doğruluk Karşılaştırması ---")
print(f"Naive Bayes Doğruluk: {accuracy_score(y_test, y_pred_nb):.4f}")
print(f"Lojistik Regresyon Doğruluk: {accuracy_score(y_test, y_pred_lr):.4f}")

# Örnek cümlelerle modelleri test edelim
ornek_cumleler = [
    "The stock market saw a significant increase today after the Federal Reserve's announcement.",
    "Manchester United won their match with an incredible last-minute goal.",
    "The new Marvel movie has broken all box office records.",
    "The Prime Minister met with foreign leaders to discuss climate change.",
    "Apple unveiled its latest tech gadget at the annual conference."
]

# Örnek cümleleri temizleyip vektöre dönüştürüyoruz
ornek_cumleler_temiz = [temizle(cumle) for cumle in ornek_cumleler]
ornek_cumleler_tfidf = tfidf.transform(ornek_cumleler_temiz)

print("\n--- Örnek Cümleler Tahmin Sonuçları ---")
for i, cumle in enumerate(ornek_cumleler):
    tahmin_nb = nb_model.predict(ornek_cumleler_tfidf[i])
    tahmin_lr = lr_model.predict(ornek_cumleler_tfidf[i])
    print(f"\nCümle: {cumle}")
    print(f"Naive Bayes Tahmini: {tahmin_nb[0]}")
    print(f"Lojistik Regresyon Tahmini: {tahmin_lr[0]}")
