

 # Makine Öğrenmesi ile Metin Sınıflandırma Projesi

 ## Bu proje, BBC haber metinlerini kategorilere ayırmak için
 Naive Bayes ve Lojistik Regresyon modellerini kullanan basit
 bir metin sınıflandırma uygulamasıdır.

 ## Özellikler:
 - Hugging Face üzerinden veya CSV dosyalarından veri seti yükleme
 - Metin temizleme (küçük harf, rakam ve noktalama temizleme)
 - TF-IDF ile metin vektörleştirme
 - Naive Bayes ve Lojistik Regresyon modelleri ile eğitim ve test
 - Performans değerlendirmesi ve karışıklık matrisi görselleştirme
 - Örnek cümlelerle model tahminleri

 ## Kurulum:
 pip install pandas numpy scikit-learn matplotlib seaborn datasets

 Veri Setini Hugging Face'ten İndirmek İçin (İstersen):
 from datasets import load_dataset
 ds = load_dataset("SetFit/bbc-news")
 ds["train"].to_csv("train.csv", index=False)
 ds["test"].to_csv("test.csv", index=False)


 ## Ana Adımlar:
 - 'train.csv' ve 'test.csv' dosyalarını yükle
 - Metinleri temizle (küçük harf, rakam ve noktalama temizleme)
 - TF-IDF ile metni sayısal vektöre çevir
 - Naive Bayes ve Lojistik Regresyon modellerini eğit ve test et
 - Performans sonuçlarını ve karışıklık matrislerini göster
 - Örnek cümlelerle modelleri test et

 ## Örnek Tahminler:
 Script çalışınca terminalde örnek cümleler için tahminler gösterilecek.


