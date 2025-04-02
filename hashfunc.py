import hashlib
import time
import requests
import random


word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
WORDS = response.content.splitlines()
WORDS = [byte_string.decode('utf-8') for byte_string in WORDS]

def generate_hash(text, algorithm):
    hasher = hashlib.new(algorithm)
    hasher.update(text.encode('utf-8'))
    return hasher.hexdigest()


algorithms = [
    "MD5",
    "SHA1",
    "SHA224",
    "SHA256",
    "SHA384",
    "SHA512",
    "SHA3_224",
    "SHA3_256",
    "SHA3_384",
    "SHA3_512",
]

file = open("textfiles/kotek.txt","r",encoding='utf-8')
kotek = file.read()
print(f"Wlazl kotek na plotek length:{len(kotek)}")
file = open("textfiles/berlin.txt","r",encoding='utf-8')
berlin = file.read()
print(f"Berlin wikipedia length:{len(berlin)}")
file = open("textfiles/tadeusz.txt","r",encoding='utf-8')
tadeusz = file.read()
print(f"Whole pan tadeusz book length:{len(tadeusz)}")


print("\nHash results:")
for algorithm in algorithms:
    start = time.time()
    hash_value = generate_hash(kotek, algorithm.lower())
    end = time.time()
    print(f"{algorithm}, kotek\n length of output: {len(hash_value)} time consumed: {end-start}")
    start = time.time()
    hash_value = generate_hash(berlin, algorithm.lower())
    end = time.time()
    print(f"{algorithm}, berlin\n length of output: {len(hash_value)} time consumed: {end - start}")
    start = time.time()
    hash_value = generate_hash(tadeusz, algorithm.lower())
    end = time.time()
    print(f"{algorithm}, tadeusz\n length of output: {len(hash_value)} time consumed: {end - start}")

#all functions are really quick
#every given hashing algorithm produces output of the same size regardless of input length

#/////////////////////////////////////////////////////////////////////////////////////////////

exercise3 = generate_hash("1234","md5")
print("\n1234 in md5:",exercise3)
#https://md5.gromweb.com/?md5=81dc9bdb52d04dc20036dbd8313ed055

#they found my secret password!


#///////////////////////////////////////////////////////////////
for i in range(len(WORDS)):
    hash1Word = random.choice(WORDS)
    hash2Word = random.choice(WORDS)
    if hash1Word == hash2Word:continue
    hash1 = generate_hash(hash1Word,"md5")
    hash2 = generate_hash(hash2Word, "md5")
    if hash1[0:3] == hash2[0:3]:
        print("\n\nPartial collision found!")
        print(hash1,hash2)
        print(hash1Word,hash2Word)

#////////////////////////////////////////////////////////////////

sac1 = "give me 1 dollar"
print("message:",sac1)
sac1 = ''.join(format(ord(x), '08b') for x in sac1)
print(sac1)
sac2='1'+sac1[1:]
print(sac2)

newsac2 = ""
for i in range(0,len(sac2),8):
    newsac2+=chr(int(sac2[i:i+8],2))
print("message after changing first bit:",newsac2)

sac1hash = generate_hash(sac1,"sha1")
sac2hash = generate_hash(sac2,"sha1")

sac1hashbinary = bin(int(sac1hash, 16))[2:].zfill(8)
sac2hashbinary = bin(int(sac2hash, 16))[2:].zfill(8)

print(f"sac1 hash: {sac1hashbinary}")
print(f"sac2 hash: {sac2hashbinary}")

sacresult = xor_result = ''.join(str(int(a) ^ int(b)) for a, b in zip(sac1hashbinary, sac2hashbinary))

print("xored hashes:",sacresult)

sacresultCount = sacresult.count("1")

if 0.45<sacresultCount/len(sacresult)<0.55:
    print("avalanche test passed")