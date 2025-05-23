# Bu klasör, Flask uygulamasında kullanılan HTML şablonlarını içerir. Kullanıcı arayüzünü oluşturmak için Bootstrap tabanlı görünümler kullanılmıştır.

## Kullanılan şablon dosyaları:

- `base.html`: Sayfalar arasında ortak kullanılan yapıyı (bootstrap, başlık, gövde düzeni) barındırır. 

- `upload.html`: Giriş yapmış kullanıcıların dosya yükleyebileceği formu içerir. Sayfa düzeni için `base.html`'i kullanır.

- `files.html`: Kullanıcının yüklediği dosyaları listeler, indirme ve silme işlemleri yapılabilir. `base.html` üzerine kuruludur.

- `login.html`: Kullanıcının giriş yapabileceği formu içerir. 

- `register.html`: Yeni kullanıcı kayıt formunu içerir. `login.html` gibi kendi içinde tasarlanmıştır.

## Not: `base.html` şablonu sadece `upload.html` ve `files.html` dosyalarında kullanılmaktadır.

