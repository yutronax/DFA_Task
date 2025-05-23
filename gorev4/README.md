# ================================================================
# Ev Değeri Tahmin Projesi
#
# Amaç:
# Bu proje, California'daki evlerle ilgili verileri kullanarak
# ev fiyatlarını tahmin etmeye çalışır. Modelleme için hem
# Doğrusal Regresyon hem de XGBoost kullanılmıştır.
#
# Adımlar:
# 1. Veriyi oku ve genel bilgi ver
# 2. Eksik verileri uygun yöntemlerle doldur
#    - Sayısal: Ortalama
#    - Kategorik: En sık görülen değer
# 3. Kategorik verileri one-hot encoding ile sayısallaştır
# 4. Özellikleri ve hedef değişkeni ayır
# 5. Eğitim ve test setine böl
# 6. Sayısal verileri ölçekle (StandardScaler)
# 7. Doğrusal Regresyon eğitimi ve tahmini
#    - RMSE ve MAPE hesapla
# 8. XGBoost eğitimi ve tahmini
#    - RMSE ve MAPE hesapla
# 9. Her iki model için hiperparametre optimizasyonu (RandomizedSearchCV)
#    - En iyi parametreleri bul
#    - Güncellenmiş modellerle tekrar tahmin yap ve metrikleri ölç
# 10. Tahminleri gerçek değerlerle kıyaslayan scatter plot'lar çiz
#
# Kullanılan Metrikler:
# - RMSE (Root Mean Square Error): Tahminlerin standart sapması
# - MAPE (Mean Absolute Percentage Error): Yüzdelik hata
#
# Gereken Kütüphaneler:
# pip install pandas numpy matplotlib scikit-learn xgboost
