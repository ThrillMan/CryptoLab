from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os


class CBCCipher:
    def __init__(self, key, iv=None):
        self.key = key
        self.block_size = AES.block_size

        if iv is None:
            self.iv = get_random_bytes(self.block_size)
        else:
            if len(iv) != self.block_size:
                raise ValueError(f"IV musi mieć długość {self.block_size} bajtów")
            self.iv = iv

        # Inicjalizacja podstawowego szyfru ECB
        self.ecb_cipher = AES.new(self.key, AES.MODE_ECB)

    def encrypt(self, plaintext):
        # Szyfrowanie w trybie CBC

        plaintext = pad(plaintext, self.block_size)
        ciphertext = bytearray()
        previous_block = self.iv

        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i + self.block_size]

            # XOR z poprzednim blokiem szyfrogramu (lub IV dla pierwszego bloku)
            xored_block = bytes(a ^ b for a, b in zip(block, previous_block))

            # Szyfrowanie bloku w trybie ECB
            encrypted_block = self.ecb_cipher.encrypt(xored_block)
            ciphertext.extend(encrypted_block)

            # Aktualizacja poprzedniego bloku dla następnej iteracji
            previous_block = encrypted_block

        # Zwracamy IV razem z zaszyfrowanym tekstem (standardowa praktyka)
        return self.iv + ciphertext

    def decrypt(self, ciphertext):
        # Deszyfrowanie w trybie CBC

        if len(ciphertext) < 2 * self.block_size:
            raise ValueError("Ciphertext jest zbyt krótki")

        # Wydzielenie IV i właściwego szyfrogramu
        iv = ciphertext[:self.block_size]
        ciphertext = ciphertext[self.block_size:]

        plaintext = bytearray()
        previous_block = iv

        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]

            # Odszyfrowanie bloku w trybie ECB
            decrypted_block = self.ecb_cipher.decrypt(block)

            # XOR z poprzednim blokiem szyfrogramu (lub IV dla pierwszego bloku)
            xored_block = bytes(a ^ b for a, b in zip(decrypted_block, previous_block))
            plaintext.extend(xored_block)

            # Aktualizacja poprzedniego bloku dla następnej iteracji
            previous_block = block

        # Usunięcie paddingu
        return unpad(plaintext, self.block_size)


if __name__ == "__main__":
    # Generowanie klucza i testowego IV
    key = get_random_bytes(16)  # AES-128
    iv = get_random_bytes(16)

    # Inicjalizacja naszego szyfru CBC
    cbc = CBCCipher(key, iv)

    # Testowy tekst do zaszyfrowania
    plaintext = b"To jest przykladowy tekst do zaszyfrowania w trybie CBC z uzyciem ECB"

    # Szyfrowanie
    ciphertext = cbc.encrypt(plaintext)
    print(f"Zaszyfrowany tekst (IV + ciphertext): {ciphertext.hex()}")

    # Deszyfrowanie
    decrypted = cbc.decrypt(ciphertext)
    print(f"Odszyfrowany tekst: {decrypted.decode('utf-8')}")

    # Weryfikacja
    assert decrypted == plaintext, "Deszyfrowanie nie powiodlo sie!"
    print("Weryfikacja pomyslna - tekst odszyfrowany poprawnie")