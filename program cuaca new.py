import requests
from datetime import datetime

class AplikasiCuaca:
    def __init__(self):
        # Menggunakan wttr.in - layanan cuaca gratis tanpa API key
        self.base_url = "https://wttr.in"
    
    def ambil_cuaca(self, nama_kota):
        """Ambil data cuaca untuk kota tertentu"""
        try:
            # Format URL untuk mendapatkan data JSON 
            url = f"{self.base_url}/{nama_kota}?format=j1&lang=id"
            
            # Kirim request ke API
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error saat mengambil data: {e}")
            return None
    
    def tampilkan_cuaca(self, data_cuaca, nama_kota):
        """Tampilkan informasi cuaca dengan format yang rapi"""
        if not data_cuaca:
            return
        
        try:
            # Ekstrak informasi dari current_condition
            kondisi_sekarang = data_cuaca['current_condition'][0]
            
            suhu = kondisi_sekarang['temp_C']
            feels_like = kondisi_sekarang['FeelsLikeC']
            deskripsi = kondisi_sekarang['lang_id'][0]['value'] if 'lang_id' in kondisi_sekarang else kondisi_sekarang['weatherDesc'][0]['value']
            kelembaban = kondisi_sekarang['humidity']
            tekanan = kondisi_sekarang['pressure']
            kecepatan_angin = kondisi_sekarang['windspeedKmph']
            arah_angin = kondisi_sekarang['winddir16Point']
            visibility = kondisi_sekarang['visibility']
            uv_index = kondisi_sekarang['uvIndex']
            
            # Informasi lokasi
            lokasi = data_cuaca['nearest_area'][0]
            nama_area = lokasi['areaName'][0]['value']
            negara = lokasi['country'][0]['value']
            
            # Tampilkan informasi
            print("\n" + "="*50)
            print(f"🌍 CUACA DI {nama_area.upper()}, {negara}")
            print("="*50)
            print(f"🌡️  Suhu Sekarang    : {suhu}°C")
            print(f"🤔 Terasa Seperti   : {feels_like}°C")
            print(f"☁️  Kondisi          : {deskripsi}")
            print(f"💧 Kelembaban       : {kelembaban}%")
            print(f"📏 Tekanan Udara    : {tekanan} mb")
            print(f"💨 Kecepatan Angin  : {kecepatan_angin} km/jam ({arah_angin})")
            print(f"👁️  Jarak Pandang    : {visibility} km")
            print(f"☀️  Indeks UV        : {uv_index}")
            print("="*50)
            
            # Tampilkan prakiraan 3 hari
            print("\n📅 PRAKIRAAN 3 HARI KE DEPAN:")
            print("-"*50)
            
            for i, hari in enumerate(data_cuaca['weather'][:3], 1):
                tanggal = hari['date']
                suhu_max = hari['maxtempC']
                suhu_min = hari['mintempC']
                deskripsi_hari = hari['lang_id'][0]['value'] if 'lang_id' in hari else hari['hourly'][0]['weatherDesc'][0]['value']
                
                print(f"\nHari {i} ({tanggal}):")
                print(f"  🌡️  Suhu: {suhu_min}°C - {suhu_max}°C")
                print(f"  ☁️  Kondisi: {deskripsi_hari}")
            
            print("\n" + "="*50 + "\n")
            
        except (KeyError, IndexError) as e:
            print(f"❌ Error saat memproses data: {e}")


def main():
    """Fungsi utama program"""
    print("🌦️  SELAMAT DATANG DI WEB CEK CUACA 🌦️")
    print("="*100)
    print("✨ Tanpa API Key - Langsung Bisa Dipakai!")
    print("="*50)
    
    # Inisialisasi aplikasi
    app = AplikasiCuaca()
    
    while True:
        # Input nama kota
        nama_kota = input("\n🏙️  Masukkan nama kota (atau 'keluar' untuk berhenti): ").strip()
        
        if nama_kota.lower() == 'keluar':
            print("\n👋 Terima kasih telah menggunakan WEB ini!")
            break
        
        if not nama_kota:
            print("❌ Nama kota tidak boleh kosong!")
            continue
        
        # Ambil dan tampilkan data cuaca
        print(f"\n🔍 Mencari data cuaca untuk {nama_kota}...")
        data_cuaca = app.ambil_cuaca(nama_kota)
        
        if data_cuaca:
            app.tampilkan_cuaca(data_cuaca, nama_kota)
        else:
            print(f"❌ Tidak bisa mengambil data untuk '{nama_kota}'. Coba lagi!")


if __name__ == "__main__":
    main()