import requests
import json
import os
from datetime import datetime

class AplikasiCuaca:
    def __init__(self):
        # Menggunakan wttr.in - layanan cuaca gratis tanpa API key
        self.base_url = "https://wttr.in"
        self.history_file = "riwayat_pencarian.json"
        self.max_history = 8
        self.history = []
        self.load_history()
    
    def load_history(self):
        """Load riwayat pencarian dari file JSON"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"⚠️  Error saat load riwayat: {e}")
            self.history = []
    
    def save_history(self):
        """Simpan riwayat pencarian ke file JSON"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  Error saat simpan riwayat: {e}")
    
    def add_to_history(self, nama_kota):
        """Tambahkan kota ke riwayat pencarian"""
        # Hapus duplikat jika ada (case-insensitive)
        self.history = [kota for kota in self.history if kota.lower() != nama_kota.lower()]
        
        # Tambahkan di awal list
        self.history.insert(0, nama_kota)
        
        # Batasi maksimal riwayat
        if len(self.history) > self.max_history:
            self.history = self.history[:self.max_history]
        
        # Simpan ke file
        self.save_history()
    
    def tampilkan_riwayat(self):
        """Tampilkan riwayat pencarian"""
        if not self.history:
            print("\n📜 Riwayat Pencarian: Belum ada riwayat")
            return False
        
        print("\n" + "="*50)
        print("📜 RIWAYAT PENCARIAN")
        print("="*50)
        for i, kota in enumerate(self.history, 1):
            print(f"{i}. 📍 {kota}")
        print("="*50)
        return True
    
    def clear_history(self):
        """Hapus semua riwayat pencarian"""
        self.history = []
        self.save_history()
        print("\n✅ Riwayat pencarian berhasil dihapus!")
    
    def ambil_cuaca(self, nama_kota):
        """Ambil data cuaca untuk kota tertentu"""
        try:
            # Bersihkan input dari karakter yang tidak valid
            nama_kota_clean = nama_kota.strip().replace('&', '').replace('?', '')
            
            # Format URL untuk mendapatkan data JSON
            url = f"{self.base_url}/{nama_kota_clean}?format=j1&lang=id"
            
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
    print("🌦️  SELAMAT DATANG DI APLIKASI CEK CUACA 🌦️")
    print("="*50)
    print("✨ Tanpa API Key - Langsung Bisa Dipakai!")
    print("="*50)
    
    # Inisialisasi aplikasi
    app = AplikasiCuaca()
    
    while True:
        # Tampilkan menu
        print("\n" + "-"*50)
        print("MENU:")
        print("1. 🔍 Cari cuaca kota")
        print("2. 📜 Lihat riwayat pencarian")
        print("3. 🗑️  Hapus riwayat")
        print("4. 🚪 Keluar")
        print("-"*50)
        
        pilihan = input("Pilih menu (1-4): ").strip()
        
        if pilihan == '1':
            # Input nama kota
            nama_kota = input("\n🏙️  Masukkan nama kota: ").strip()
            
            if not nama_kota:
                print("❌ Nama kota tidak boleh kosong!")
                continue
            
            # Ambil dan tampilkan data cuaca
            print(f"\n🔍 Mencari data cuaca untuk {nama_kota}...")
            data_cuaca = app.ambil_cuaca(nama_kota)
            
            if data_cuaca:
                app.tampilkan_cuaca(data_cuaca, nama_kota)
                app.add_to_history(nama_kota)
                print("✅ Kota telah ditambahkan ke riwayat!")
            else:
                print(f"❌ Tidak bisa mengambil data untuk '{nama_kota}'. Coba lagi!")
        
        elif pilihan == '2':
            # Tampilkan riwayat
            if app.tampilkan_riwayat():
                # Opsi untuk cari ulang dari riwayat
                cari_ulang = input("\nIngin mencari cuaca dari riwayat? (ketik nomor atau 'tidak'): ").strip()
                
                if cari_ulang.isdigit():
                    idx = int(cari_ulang) - 1
                    if 0 <= idx < len(app.history):
                        nama_kota = app.history[idx]
                        print(f"\n🔍 Mencari data cuaca untuk {nama_kota}...")
                        data_cuaca = app.ambil_cuaca(nama_kota)
                        
                        if data_cuaca:
                            app.tampilkan_cuaca(data_cuaca, nama_kota)
                            app.add_to_history(nama_kota)
                    else:
                        print("❌ Nomor tidak valid!")
        
        elif pilihan == '3':
            # Hapus riwayat
            if app.history:
                konfirmasi = input("Yakin ingin menghapus semua riwayat? (ya/tidak): ").strip().lower()
                if konfirmasi == 'ya':
                    app.clear_history()
            else:
                print("\n📜 Riwayat kosong, tidak ada yang perlu dihapus.")
        
        elif pilihan == '4':
            # Keluar
            print("\n👋 Terima kasih telah menggunakan aplikasi ini!")
            break
        
        else:
            print("❌ Pilihan tidak valid! Silakan pilih 1-4.")


if __name__ == "__main__":
    main() 