from flask import Flask, render_template, request, jsonify
import hashlib
import datetime
import os

app = Flask(__name__, static_folder='static', template_folder='templates2')

# Hafızada tutulan hash kayıtları
kayitli_hashler = {}

@app.route("/")
def anasayfa():
    # Ana sayfa olarak gorev6.html dosyasını gösteriyoruz
    return render_template("gorev6.html")

@app.route("/hash", methods=["POST"])
def hash_uret():
    gelen_veri = request.json.get("data", "")
    # Gelen verinin SHA256 hash'ini hesaplıyoruz
    hash_nesnesi = hashlib.sha256(gelen_veri.encode("utf-8"))
    hex_deger = hash_nesnesi.hexdigest()
    # Hesaplanan hash'i JSON olarak dönüyoruz
    return jsonify({"hash": hex_deger})

@app.route("/save", methods=["POST"])
def hash_kaydet():
    gelen_hash = request.json.get("hash", "")
    # Eğer hash zaten varsa kullanıcıyı uyarıyoruz
    if gelen_hash in kayitli_hashler:
        return jsonify({"message": "Hash zaten kayıtlı."})
    # Yoksa mevcut UTC zaman damgası ile kaydediyoruz
    zaman = datetime.datetime.utcnow().isoformat() + "Z"
    kayitli_hashler[gelen_hash] = zaman
    return jsonify({"message": f"Hash başarıyla kaydedildi. Zaman damgası: {zaman}"})

@app.route("/verify", methods=["POST"])
def hash_dogrula():
    gelen_hash = request.json.get("hash", "")
    # Kaydı varsa doğrulama mesajı dönüyoruz
    zaman = kayitli_hashler.get(gelen_hash)
    if zaman:
        return jsonify({"message": f"Hash doğrulandı! Kaydedilme zamanı: {zaman}"})
    else:
        
        return jsonify({"message": "Hash kaydı bulunamadı, dosya değiştirilmiş olabilir."})

if __name__ == "__main__":
    
    calisma_portu = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=calisma_portu)

