# Instagram Brute Force Script

⚠️ **PENTING: Script ini hanya untuk tujuan edukasi dan pengujian keamanan pada sistem Anda sendiri. Penggunaan script ini untuk mengakses akun Instagram tanpa izin adalah ilegal dan melanggar Terms of Service Instagram.**

## Deskripsi
Script Python untuk melakukan brute force attack pada akun Instagram (hanya untuk tujuan edukasi).

## Persyaratan
- Python 3.x
- requests
- beautifulsoup4

## Instalasi

### Untuk Windows/Linux Standar:
```bash
pip install requests beautifulsoup4
```

### Untuk Kali Linux (Menggunakan Virtual Environment):
Kali Linux menggunakan Python yang dikelola secara eksternal, jadi perlu menggunakan virtual environment:

```bash
# Install pypy3-venv jika belum terinstall
sudo apt install python3-venv

# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Catatan:** Setiap kali membuka terminal baru, aktifkan virtual environment dengan:
```bash
source venv/bin/activate
```

## Penggunaan

### 1. Buat file passwords.txt
Buat file `passwords.txt` di direktori yang sama dengan script, berisi daftar password yang akan dicoba (satu password per baris):

```bash
# Contoh: copy dari file contoh
cp passwords.txt.example passwords.txt

# Atau buat manual
nano passwords.txt
```

**Format file passwords.txt:**
```
password123
12345678
password
admin
qwerty
```

### 2. Edit konfigurasi di bruteforce.py
Buka file `bruteforce.py` dan edit bagian bawah file:

```python
# Contoh penggunaan
username = 'target_username'  # Ganti dengan username target
password_list = 'passwords.txt'  # Nama file password list
brute_force_instagram(username, password_list)
```

### 3. Jalankan script
```bash
python bruteforce.py
```

**Catatan:** 
- File `passwords.txt` harus ada di direktori yang sama dengan script
- File `passwords.txt` tidak akan di-commit ke Git (untuk keamanan)
- Gunakan file `passwords.txt.example` sebagai template

## Peringatan
- Script ini hanya untuk tujuan edukasi
- Jangan gunakan untuk aktivitas ilegal
- Penggunaan yang tidak sah dapat mengakibatkan konsekuensi hukum
- Instagram memiliki sistem keamanan yang dapat mendeteksi dan memblokir aktivitas mencurigakan

## Lisensi
Gunakan dengan tanggung jawab Anda sendiri.
