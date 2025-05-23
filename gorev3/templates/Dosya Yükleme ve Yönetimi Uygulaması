import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, abort
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Gerçek ortamda daha güçlü ve gizli bir anahtar kullanılmalı

# Yüklenen dosyaların tutulacağı klasörü oluşturuyoruz
yukleme_klasoru = 'uploaded_files'
if not os.path.exists(yukleme_klasoru):
    os.makedirs(yukleme_klasoru)  # Klasör yoksa oluşturuyoruz

app.config['UPLOAD_FOLDER'] = yukleme_klasoru

# İzin verilen dosya uzantıları tanımlanıyor
izinli_uzantilar = {'pdf', 'png', 'jpg', 'jpeg'}

# Basit bir kullanıcı veritabanı simülasyonu (kullanici_adi: sifre)
kullanici_veritabani = {}

# Dosyanın uzantısının izinli olup olmadığını kontrol ediyoruz
def uzanti_gecerli_mi(dosya_adi):
    return '.' in dosya_adi and dosya_adi.rsplit('.', 1)[1].lower() in izinli_uzantilar

# Giriş yapılmadan erişilmesini istemediğimiz yerleri korumak için bir dekoratör
def giris_gerekli(view_fonksiyonu):
    @wraps(view_fonksiyonu)
    def sarici_fonksiyon(*args, **kwargs):
        if 'username' not in session:
            flash('Bu sayfaya erişmek için giriş yapmalısınız.', 'warning')
            return redirect(url_for('login', next=request.url))
        return view_fonksiyonu(*args, **kwargs)
    return sarici_fonksiyon

@app.route('/')
def home():
    # Kullanıcı giriş yapmışsa dosyalar sayfasına yönlendiriyoruz, yoksa giriş sayfasına
    if 'username' in session:
        return redirect(url_for('files'))
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Giriş yapan bir kullanıcı tekrar kayıt olmaya çalışmasın
    if 'username' in session:
        return redirect(url_for('files'))

    if request.method == 'POST':
        kullanici_adi = request.form.get('username', '').strip()
        sifre = request.form.get('password', '').strip()

        if not kullanici_adi or not sifre:
            flash('Kullanıcı adı ve şifre gerekli.', 'danger')
            return render_template('register.html')

        if kullanici_adi in kullanici_veritabani:
            flash('Bu kullanıcı adı zaten mevcut.', 'danger')
            return render_template('register.html')

        kullanici_veritabani[kullanici_adi] = sifre
        flash('Kayıt başarılı, şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Giriş yapılmışsa tekrar giriş yapmaya gerek yok
    if 'username' in session:
        return redirect(url_for('files'))

    if request.method == 'POST':
        kullanici_adi = request.form.get('username', '').strip()
        sifre = request.form.get('password', '').strip()

        if not kullanici_adi or not sifre:
            flash('Kullanıcı adı ve şifre gerekli.', 'danger')
            return render_template('login.html')

        kayitli_sifre = kullanici_veritabani.get(kullanici_adi)
        if kayitli_sifre and kayitli_sifre == sifre:
            session['username'] = kullanici_adi
            flash(f'Hoş geldin, {kullanici_adi}!', 'success')
            sonraki_sayfa = request.args.get('next')
            return redirect(sonraki_sayfa or url_for('files'))
        else:
            flash('Hatalı kullanıcı adı veya şifre.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@giris_gerekli
def logout():
    session.pop('username', None)
    flash('Başarıyla çıkış yaptınız.', 'info')
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
@giris_gerekli
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Dosya bilgisi bulunamadı.', 'danger')
            return redirect(request.url)

        yuklenecek_dosya = request.files['file']

        if yuklenecek_dosya.filename == '':
            flash('Seçili dosya yok.', 'danger')
            return redirect(request.url)

        if yuklenecek_dosya and uzanti_gecerli_mi(yuklenecek_dosya.filename):
            temiz_dosya_adi = secure_filename(yuklenecek_dosya.filename)
            # Kullanıcı adı ile birlikte dosya adını benzersiz hale getiriyoruz
            kaydedilecek_dosya_adi = f"{session['username']}_{temiz_dosya_adi}"
            yukleme_yolu = os.path.join(app.config['UPLOAD_FOLDER'], kaydedilecek_dosya_adi)
            yuklenecek_dosya.save(yukleme_yolu)
            flash('Dosya başarıyla yüklendi.', 'success')
            return redirect(url_for('files'))
        else:
            flash('İzin verilen dosya türleri: pdf, png, jpg, jpeg.', 'danger')
            return redirect(request.url)

    return render_template('upload.html')

@app.route('/files')
@giris_gerekli
def files():
    giris_yapan_kullanici = session['username']
    mevcut_dosyalar = os.listdir(app.config['UPLOAD_FOLDER'])
    kullaniciya_ait_dosyalar = [dosya for dosya in mevcut_dosyalar if dosya.startswith(giris_yapan_kullanici + '_')]
    return render_template('files.html', files=kullaniciya_ait_dosyalar)

@app.route('/files/<filename>/delete', methods=['POST'])
@giris_gerekli
def delete_file(filename):
    giris_yapan_kullanici = session['username']

    # Kullanıcının kendi dosyasını silmeye çalıştığından emin oluyoruz
    if not filename.startswith(giris_yapan_kullanici + '_'):
        abort(403)

    silinecek_dosya_yolu = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(silinecek_dosya_yolu):
        os.remove(silinecek_dosya_yolu)
        flash('Dosya silindi.', 'success')
    else:
        flash('Dosya bulunamadı.', 'danger')

    return redirect(url_for('files'))

@app.route('/uploads/<filename>')
@giris_gerekli
def uploaded_file(filename):
    giris_yapan_kullanici = session['username']

    # Kullanıcının kendi dosyasına eriştiğinden emin oluyoruz
    if not filename.startswith(giris_yapan_kullanici + '_'):
        abort(403)

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
