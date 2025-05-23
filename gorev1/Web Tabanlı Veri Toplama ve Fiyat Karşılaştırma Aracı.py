from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Ürün bilgilerini saklamak için boş DataFrame oluşturuyoruz
sutunlar = ["urun_adi", "fiyat", "resim_url"]
urunler_df = pd.DataFrame(columns=sutunlar)

# Chrome driver başlatılıyor
tarayici = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# n11 ana sayfası açılıyor
tarayici.get("https://www.n11.com/")
time.sleep(2)

# Kullanıcıdan aramak istediği ürün ismi alınıyor
aranan_urun = input("Lütfen ürün adını yazınız: ")

# Arama kutusu bulunup, ürün ismi giriliyor ve Enter ile arama başlatılıyor
arama_kutusu = WebDriverWait(tarayici, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//input[@id="searchData"]'))
)
arama_kutusu.click()
time.sleep(0.4)
arama_kutusu.send_keys(aranan_urun, Keys.ENTER)

time.sleep(1)

# Kullanıcıdan rating filtresi için 1-10 arasında değer alınıyor
secilen_rating = int(input("1 ile 10 arasında bir rating seçiniz: "))

# Satıcı puanı filtresi sayfası açılıyor ve seçilen puana tıklanıyor
puan_filtresi = WebDriverWait(tarayici, 10).until(
    EC.presence_of_element_located((By.XPATH, '//section[@data-tag-name="Merchant Rate"]'))
)
puan_secimi = WebDriverWait(puan_filtresi, 10).until(
    EC.presence_of_element_located((By.XPATH, f'//div[@class="track"]/span[{secilen_rating}]'))
)
tarayici.execute_script("arguments[0].click();", puan_secimi)
time.sleep(1)

# Fiyat filtresi sayfası açılıyor, kullanıcıdan min ve max fiyat bilgisi alınıyor
fiyat_filtresi = WebDriverWait(tarayici, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//section[@class="filter filterPrice" and @data-tag-name="Price"]'))
)
min_fiyat = input("Minimum fiyatı giriniz: ")
max_fiyat = input("Maksimum fiyatı giriniz: ")

# Min ve max fiyat kutularına girilen değerler yazılıyor ve Enter ile filtre uygulanıyor
min_fiyat_kutusu = WebDriverWait(fiyat_filtresi, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//input[@id="minPrice"]'))
)
min_fiyat_kutusu.send_keys(min_fiyat)

max_fiyat_kutusu = WebDriverWait(fiyat_filtresi, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//input[@id="maxPrice"]'))
)
max_fiyat_kutusu.send_keys(max_fiyat, Keys.ENTER)

time.sleep(1)

# Ürünleri sayfa sayfa çekip DataFrame'e ekleyen fonksiyon
def urunleri_topla(urun_listesi):
    try:
        sayac = 0
        for urun in urun_listesi:
            sayac += 1
            isim = WebDriverWait(urun, 10).until(
                EC.presence_of_element_located((By.XPATH, './/h3[@class="productName"]'))
            ).text

            fiyat = WebDriverWait(urun, 10).until(
                EC.presence_of_element_located((By.XPATH, f'.//span[@title="{isim}"]'))
            ).text

            resim = WebDriverWait(urun, 10).until(
                EC.presence_of_element_located((By.XPATH, './/img[@class="lazy cardImage"]'))
            ).get_attribute("src")

            urunler_df.loc[len(urunler_df)] = [isim, fiyat, resim]

            # Eğer son ürüne geldiysek kullanıcıya devam edip etmeyeceğini soruyoruz
            if sayac == len(urun_listesi):
                devam = input("Başka sayfa için devam etmek ister misiniz? (e/h): ")
                if devam.lower() == "h":
                    break
                else:
                    sonraki_sayfa_linki = WebDriverWait(tarayici, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//a[@class="next navigation"]'))
                    ).get_attribute("href")

                    tarayici.get(sonraki_sayfa_linki)
                    time.sleep(2)

                    yeni_urunler = WebDriverWait(tarayici, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//li[@class="column "]'))
                    )
                    return urunleri_topla(yeni_urunler)
    except Exception as e:
        print("Hata oluştu:", e)
    finally:
        return

# İlk sayfadaki ürünler çekiliyor
ilk_urunler = WebDriverWait(tarayici, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//li[@class="column "]'))
)

# Ürünler toplanıyor
urunleri_topla(ilk_urunler)

tarayici.close()
tarayici.quit()

# Veri temizleme işlemleri
urunler_df = urunler_df[urunler_df["urun_adi"].notna() & urunler_df["fiyat"].notna()]

# Fiyat sütunundaki "TL" ibaresi ve noktalama işaretleri temizlenip sayıya çevriliyor
urunler_df["fiyat"] = urunler_df["fiyat"].str.replace("TL", "").str.replace(".", "").str.replace(",", ".").str.strip()
urunler_df["fiyat"] = pd.to_numeric(urunler_df["fiyat"], errors="coerce")

# Fiyat sütununa göre artan şekilde sıralanıyor
urunler_df = urunler_df.sort_values(by="fiyat", ascending=True, ignore_index=True)

print("En ucuz ürünler:")
print(urunler_df.head(10))

print("En pahalı ürünler:")
print(urunler_df.tail(10))

# Sonuç CSV dosyasına kaydediliyor
urunler_df.to_csv(f"{aranan_urun}_urunler.csv", index=False)
