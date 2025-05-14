from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import time
import os


# Funkcja do pomiaru czasu szyfrowania i deszyfrowania
def measure_cipher_performance(file_path, mode, key, iv=None):
    # Wczytanie pliku
    with open(file_path, 'rb') as f:
        plaintext = f.read()

    # Inicjalizacja szyfru w odpowiednim trybie
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, AES.MODE_ECB)
    elif mode == AES.MODE_CBC:
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    elif mode == AES.MODE_CTR:
        cipher = AES.new(key, AES.MODE_CTR, nonce=iv[:8])  # CTR używa nonce zamiast IV

    # Pomiar czasu szyfrowania
    start_encrypt = time.time()
    if mode == AES.MODE_ECB:
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    elif mode == AES.MODE_CBC:
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    elif mode == AES.MODE_CTR:
        ciphertext = cipher.encrypt(plaintext)  # CTR nie wymaga paddingu
    encrypt_time = time.time() - start_encrypt

    # Pomiar czasu deszyfrowania
    start_decrypt = time.time()
    if mode == AES.MODE_ECB:
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    elif mode == AES.MODE_CBC:
        # Musimy stworzyć nowy obiekt szyfru do deszyfrowania
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    elif mode == AES.MODE_CTR:
        # CTR używa tego samego obiektu do deszyfrowania
        cipher = AES.new(key, AES.MODE_CTR, nonce=iv[:8])
        decrypted = cipher.decrypt(ciphertext)
    decrypt_time = time.time() - start_decrypt

    # Sprawdzenie poprawności
    assert decrypted == plaintext, "Deszyfrowanie nie powiodło się!"

    return encrypt_time, decrypt_time


# Pliki do testowania
files = [
    ('textfiles/tadeusz.txt', 'Mały plik (kilkadziesiat KB)'),
    ('textfiles/mobydick.txt', 'Średni plik (kilkaset KB)'),
    ('textfiles/bible.txt', 'Duży plik (kilkaset MB)')
]

# Sprawdzenie czy pliki istnieją
for file, _ in files:
    if not os.path.exists(file):
        print(f"Błąd: Plik {file} nie istnieje!")
        exit(1)

# Generowanie klucza i IV
key = get_random_bytes(16)  # AES-128
iv = get_random_bytes(16)  # IV dla CBC i CTR
print(key,iv,iv[:8])

# Tryby do przetestowania
modes = [
    ('ECB', AES.MODE_ECB),
    ('CBC', AES.MODE_CBC),
    ('CTR', AES.MODE_CTR)
]

# Przeprowadzenie testów
results = {}
for file, desc in files:
    file_results = {}
    for mode_name, mode in modes:
        encrypt_time, decrypt_time = measure_cipher_performance(file, mode, key, iv)
        file_results[mode_name] = {
            'encrypt': encrypt_time,
            'decrypt': decrypt_time,
            'total': encrypt_time + decrypt_time
        }
    results[desc] = file_results

# Wyświetlenie wyników
print("\nWyniki pomiarów czasu szyfrowania i deszyfrowania:")
print("=" * 70)
for file_desc, file_modes in results.items():
    print(f"\nPlik: {file_desc}")
    print("-" * 70)
    print("{:<10} {:<15} {:<15} {:<15}".format(
        "Tryb", "Czas szyfrowania", "Czas deszyfrowania", "Całkowity czas"))
    for mode, times in file_modes.items():
        print("{:<10} {:<15.6f} {:<15.6f} {:<15.6f}".format(
            mode, times['encrypt'], times['decrypt'], times['total']))