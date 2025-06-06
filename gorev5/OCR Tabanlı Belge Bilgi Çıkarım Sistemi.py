import os
import cv2
import pytesseract
import csv
import re

# Windows kullanıyorsak, Tesseract'ın kurulu olduğu yolu belirtmemiz gerekiyor
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# OCR işlemini yapacağımız görseli okuyoruz
gorsel_yolu = "fatura1.jpg"  # Görselin yolu
gorsel = cv2.imread(gorsel_yolu)

# Görseli griye çeviriyoruz çünkü OCR, gri görsellerde daha iyi sonuç verir
gri_gorsel = cv2.cvtColor(gorsel, cv2.COLOR_BGR2GRAY)

# Görseldeki gürültüyü azaltmak için median blur uyguluyoruz
bulanık_gorsel = cv2.medianBlur(gri_gorsel, 3)

# Görseli siyah-beyaz hale getirerek metinlerin daha belirgin olmasını sağlıyoruz
net_gorsel = cv2.adaptiveThreshold(
    bulanık_gorsel, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, 11, 2
)

# OCR ayarları: hem Türkçe tanıyabilmesi için dil seçeneklerini belirtiyoruz

ocr_metni = pytesseract.image_to_string(net_gorsel, lang="tur")

# Elde edilen metni satırlara bölüyoruz ve boş satırları temizliyoruz
satirlar = ocr_metni.split('\n')
satirlar = [satir.strip() for satir in satirlar if satir.strip() != '']

# Fatura bilgilerini bulmak için kullanacağımız anahtar kelimeleri tanımlıyoruz
anahtarlar = {
    "tarih": ["date", "tarih","tarıh", "sipariş tarihi", "fatura tarihi", "düzenleme tarihi", "order date", "invoice date", "issue date"],
    "tutar": ["amount", "tutar", "nakit", "cash", "kart", "ödeme", "bank", "payment", "paid", "toplam","top"],
    "fatura_no": ["invoice", "fatura", "approval", "onay", "fatura no", "invoice no", "belge no", "document no"],
    "genel_toplam": ["total", "toplam", "genel toplam", "overall total"]
}

# Çıkarılacak bilgiler için başlangıçta boş değişkenler tanımlıyoruz
bulunan_tarih = None
bulunan_tutar = None
bulunan_fatura_no = None
bulunan_toplam = None

# Tüm satırları tarayıp ilgili bilgileri arıyoruz
for satir in satirlar:
    kucuk_satir = satir.lower()
    print(f"İşlenen Satır: {kucuk_satir}")

    # Tarih bilgisi içerip içermediğini kontrol ediyoruz
    if any(anahtar in kucuk_satir for anahtar in anahtarlar["tarih"]):
        eslesen_tarih = re.search(r'\d{2}[-:./]\d{2}[-:./]?\d{2,4}', satir)
        if eslesen_tarih:
            bulunan_tarih = eslesen_tarih.group()

    # Genel toplam bilgisi içerip içermediğini kontrol ediyoruz
    elif any(anahtar in kucuk_satir for anahtar in anahtarlar["genel_toplam"]):
        sayilar = re.findall(r'\d+[.,]?\d*', satir)
        if sayilar:
            bulunan_toplam = sayilar[-1].replace(',', '.')

    # Fatura numarasını arıyoruz
    elif any(anahtar in kucuk_satir for anahtar in anahtarlar["fatura_no"]):
        fatura_no_eslesme = re.search(r'#?\s?(\d{4,})', satir)
        if fatura_no_eslesme:
            bulunan_fatura_no = fatura_no_eslesme.group(1)

    # Tutarla ilgili bir bilgi varsa onu da alıyoruz (toplamdan farklı olabilir)
    elif any(anahtar in kucuk_satir for anahtar in anahtarlar["tutar"]):
        sayilar = re.findall(r'\d+[.,]?\d*', satir)
        if sayilar:
            bulunan_tutar = sayilar[-1].replace(',', '.')

# Sonuçları ekrana yazdırıyoruz
print("\nFatura Bilgileri:")
print(f"Tarih      : {bulunan_tarih}")
print(f"Tutar      : {bulunan_tutar}")
print(f"Fatura No  : {bulunan_fatura_no}")
print(f"Toplam     : {bulunan_toplam}")
dosya_adi = "fatura_verisi_tesseract.csv"
# CSV dosyasının var olup olmadığını kontrol ediyoruz
dosya_var = os.path.exists(dosya_adi)
dosya_bos = os.path.getsize(dosya_adi) == 0 if dosya_var else True
# Sonuçları CSV dosyasına kaydediyoruz
with open(dosya_adi, "a", newline="") as dosya:
    yazici = csv.writer(dosya)
    if dosya_bos:
        # Dosya boşsa başlık satırını yazıyoruz
        yazici.writerow(["Tarih", "Tutar", "Fatura No", "Toplam"])
    yazici.writerow([bulunan_tarih, bulunan_tutar, bulunan_fatura_no, bulunan_toplam])
