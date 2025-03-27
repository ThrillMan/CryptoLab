from sympy import *
import secrets


bits = 512
p = randprime(2**(bits-1), 2**bits)
g = 5
print("p",p)

bits = 2048

#2048 bits
a = secrets.randbits(bits)
print("a",a)
A= pow(g,a,p)
#2048 bits
b = secrets.randbits(bits)
print("b",b)
B = pow(g,b,p)

keyA = pow(B,a,p)

keyB = pow(A,b,p)

print("keyA",keyA)
print("keyB",keyB)

if keyA == keyB:
    print("key successfully exchanged!")