# Fatura OCR ve Veri Çıkarımı

Bu Python projesi, fatura görselleri üzerinden Tarih, Tutar, Fatura No ve Toplam gibi temel bilgileri otomatik olarak ayıklar. Veriler bir CSV dosyasına kaydedilir.

## Gereksinimler

- Python 3
- opencv-python
- pytesseract
- Tesseract OCR 

## Kurulum

### Gerekli Python kütüphanelerini yüklemek için:

pip install opencv-python pytesseract

### Tesseract OCR'ı indirin ve kurun:
https://github.com/tesseract-ocr/tesseract

Windows için kodda tesseract yolu belirtilmelidir:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

## Kullanım

1. 'fatura2.png' adlı fatura görselini proje klasörüne ekleyin.
2. Python dosyasını çalıştırın.
3. Elde edilen bilgiler 'fatura_verisi_tesseract.csv' dosyasına kaydedilecektir.

## Notlar

- OCR işlemi öncesi görsel iyileştirme adımları uygulanır (grileştirme, bulanıklaştırma, eşikleme).
- Türkçe metin tanıma desteği kullanılır.
- Tarih ve tutar bilgileri düzenli ifadelerle ayıklanır.
