#  n11 Ürün Fiyat Toplayıcı (Selenium ile Web Scraping)

Bu proje, [n11.com](https://www.n11.com) üzerinde istediğiniz ürünleri arayıp, belirli filtrelere göre (fiyat aralığı, satıcı puanı) ürün bilgilerini (isim, fiyat, görsel) toplayan bir Python betiğidir. Toplanan ürünler bir CSV dosyasına kaydedilir ve terminalde en ucuz ve en pahalı ürünler listelenir.

---

# Özellikler

-  Ürün adı ile arama
-  Satıcı puanı filtresi (1–10)
-  Fiyat aralığı belirleme
-  Ürün ismi, fiyatı ve görsel URL’si toplama
-  CSV olarak kayıt
-  Terminalde özet veri gösterimi (en ucuz/pahalı ürünler)

---

# Kurulum

Gerekli kütüphaneleri yüklemek için terminalde:

```bash
pip install selenium pandas webdriver-manager
