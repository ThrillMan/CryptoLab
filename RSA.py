from sympy import *
import random
import math

minPrime = 999
maxPrime = 99999
cached_primes = [i for i in range(minPrime,maxPrime) if isprime(i)]
print(cached_primes)
# p = random.choice([i for i in cached_primes])
# q = random.choice([i for i in cached_primes])

# p=4253
# q=9973

#values taken from internet
p = 983531983579983617983777983791983819
q = 999998727899999


print("p,q",p,q)

n = p * q
print("n",n)

phi = (p-1)*(q-1)
print("phi",phi)

e=0

for i in cached_primes:
    if math.gcd(i,phi)==1:
        e=i
        break
print("e",e)

d = pow(e,-1,phi)

print("d",d)

m = "abcde"*10
print("original message",m)

#c = (m**e)%n

#minus 97 so that values are smaller. in this code we only use <a,e> letters
m_arr = [ord(i)-97 for i in m]
print("m_arr",m_arr)
#1 at the leftmost part so to be sure that no leading zeroes will be lost in decryption
m_binary = "1"
for i in m_arr:
    #3 bits available for encoding!
    m_binary+="{0:03b}".format(i)
print("og msg in binary",m_binary)
print("message numerical value",int(m_binary,2),"\n")
c = pow(int(m_binary,2),e,n)
print("encrypted message num val",c,"\n")

m=pow(c, d, n)
m_binary = bin(m)
m_binary = m_binary[2:]

print("decrypted message in binary",m_binary)
print("decrypted message numerical val",m,"\n")
print("decrypted message in plaintext:")
for i in range(1,len(m_binary)-2,3):
    letter_in_ascii = int(m_binary[i:i+3],2)+97
    print(chr(letter_in_ascii),end="")