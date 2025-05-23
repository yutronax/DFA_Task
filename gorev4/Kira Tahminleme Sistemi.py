import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from xgboost import XGBRegressor

#Veriyi okuyalım
veri = pd.read_csv("housing.csv")

# İlk bakış
print("Genel Bilgi:")
print(veri.info())
print("\nİstatistikler:")
print(veri.describe())
print("\nİlk 5 Satır:")
print(veri.head())
print("\nEksik Veri Sayısı:")
print(veri.isnull().sum())

#Eksik verileri dolduralım

# Sayısal kolonlar için ortalama ile doldurma
sayi_doldur = SimpleImputer(strategy='mean')
veri[['total_bedrooms']] = sayi_doldur.fit_transform(veri[['total_bedrooms']])

# Kategorik kolonlar için en sık geçen değerle doldurma
kategori_doldur = SimpleImputer(strategy='most_frequent')
veri[['ocean_proximity']] = kategori_doldur.fit_transform(veri[['ocean_proximity']])

# Kategorik kolonları sayısallaştıralım (one-hot)
veri = pd.get_dummies(veri, columns=['ocean_proximity'], drop_first=True)

# Hedef ve özellikleri ayıralım
hedef = veri["median_house_value"]
ozellikler = veri.drop("median_house_value", axis=1)

# Eğitim ve test seti oluştur
x_egitim, x_test, y_egitim, y_test = train_test_split(ozellikler, hedef, test_size=0.3, random_state=42)

# Ölçekleme işlemi
olcek = StandardScaler()
x_egitim_scaled = olcek.fit_transform(x_egitim)
x_test_scaled = olcek.transform(x_test)

# Doğrusal regresyon modeli
model_dogrusal = LinearRegression()
model_dogrusal.fit(x_egitim_scaled, y_egitim)
tahmin_dogrusal = model_dogrusal.predict(x_test_scaled)

rmse_dogrusal = np.sqrt(mean_squared_error(y_test, tahmin_dogrusal))
mape_dogrusal = mean_absolute_percentage_error(y_test, tahmin_dogrusal) * 100

print("\n--- Doğrusal Regresyon ---")
print(f"RMSE: {rmse_dogrusal:.2f}")
print(f"MAPE: %{mape_dogrusal:.2f}")

# XGBoost modeli
model_xgb = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model_xgb.fit(x_egitim_scaled, y_egitim)
tahmin_xgb = model_xgb.predict(x_test_scaled)

rmse_xgb = np.sqrt(mean_squared_error(y_test, tahmin_xgb))
mape_xgb = mean_absolute_percentage_error(y_test, tahmin_xgb) * 100

print("\n--- XGBoost ---")
print(f"RMSE: {rmse_xgb:.2f}")
print(f"MAPE: %{mape_xgb:.2f}")

# Doğrusal regresyon için parametre araması
dogrusal_ayarlar = {
    'fit_intercept': [True, False],
    'positive': [True, False]
}

arama_dogrusal = RandomizedSearchCV(
    LinearRegression(),
    param_distributions=dogrusal_ayarlar,
    n_iter=4,
    cv=5,
    scoring='neg_mean_squared_error',
    random_state=42,
    n_jobs=-1,
    verbose=1
)

arama_dogrusal.fit(x_egitim_scaled, y_egitim)
en_iyi_dogrusal = arama_dogrusal.best_estimator_

print("\nEn iyi doğrusal model ayarları:", arama_dogrusal.best_params_)

tahmin_dogrusal_eniyi = en_iyi_dogrusal.predict(x_test_scaled)
rmse_dogrusal_eniyi = np.sqrt(mean_squared_error(y_test, tahmin_dogrusal_eniyi))
mape_dogrusal_eniyi = mean_absolute_percentage_error(y_test, tahmin_dogrusal_eniyi) * 100

print(f"RMSE (Opt): {rmse_dogrusal_eniyi:.2f}")
print(f"MAPE (Opt): %{mape_dogrusal_eniyi:.2f}")

# XGBoost için parametre araması
xgb_ayarlar = {
    'n_estimators': [50, 100, 200, 300],
    'max_depth': [3, 5, 7, 9],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'subsample': [0.6, 0.8, 1.0],
    'colsample_bytree': [0.6, 0.8, 1.0]
}

arama_xgb = RandomizedSearchCV(
    XGBRegressor(random_state=42),
    param_distributions=xgb_ayarlar,
    n_iter=20,
    cv=5,
    scoring='neg_mean_squared_error',
    random_state=42,
    n_jobs=-1,
    verbose=1
)

arama_xgb.fit(x_egitim_scaled, y_egitim)
en_iyi_xgb = arama_xgb.best_estimator_

print("\nEn iyi XGBoost ayarları:", arama_xgb.best_params_)

tahmin_xgb_eniyi = en_iyi_xgb.predict(x_test_scaled)
rmse_xgb_eniyi = np.sqrt(mean_squared_error(y_test, tahmin_xgb_eniyi))
mape_xgb_eniyi = mean_absolute_percentage_error(y_test, tahmin_xgb_eniyi) * 100

print(f"RMSE (XGB Opt): {rmse_xgb_eniyi:.2f}")
print(f"MAPE (XGB Opt): %{mape_xgb_eniyi:.2f}")

# Görselleştirme
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.scatter(y_test, tahmin_dogrusal_eniyi, alpha=0.5, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("Gerçek Değer")
plt.ylabel("Tahmin")
plt.title("Doğrusal Regresyon Tahminleri")

plt.subplot(1, 2, 2)
plt.scatter(y_test, tahmin_xgb_eniyi, alpha=0.5, color='green')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("Gerçek Değer")
plt.ylabel("Tahmin")
plt.title("XGBoost Tahminleri")

plt.tight_layout()
plt.show()
