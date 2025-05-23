
Flask Dosya Yükleme Uygulaması

Bu proje, kullanıcıların kayıt olup giriş yapabildiği, kendi dosyalarını yükleyip görebildiği ve silebildiği basit bir Flask uygulamasıdır.

Özellikler

- Kayıt ve giriş sistemi (oturum yönetimi)
- Yalnızca giriş yapan kullanıcıların erişebileceği dosya yükleme sayfası
- Yüklenen dosyaların listelenmesi ve silinebilmesi
- Her kullanıcı sadece kendi dosyalarını görebilir

Kurulum

1. Gerekli kütüphaneleri yükleyin:

pip install flask werkzeug

2. Proje dizininde aşağıdaki klasörü oluşturun:

yuklenen_dosyalar

3. Flask uygulamasını başlatın:

python app.py

Kullanım

1. Tarayıcıda `http://localhost:5000` adresine gidin.
2. Önce kayıt olun, ardından giriş yapın.
3. Dosya yükle sayfasından PDF veya görsel dosyaları yükleyin.
4. Yüklediğiniz dosyaları görebilir, silebilir veya indirebilirsiniz.

Notlar

- Kullanıcı verileri bellekte tutulur. Uygulama yeniden başlatıldığında sıfırlanır.
- Yalnızca `pdf`, `png`, `jpg`, `jpeg` uzantılı dosyalar yüklenebilir.
- Her dosya adının başına kullanıcı adı eklenerek diğer kullanıcılarla çakışması önlenir.
