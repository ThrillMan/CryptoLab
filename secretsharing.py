import random
from sympy import *
# Wartość liczbowa określająca rozmiar przestrzeni liczbowej
k = 1000
# Liczba wszystkich udziałów
n = 3
# Liczba udziałów wymaganych do odtworzenia sekretu
t = n
# Sekret reprezentowany za pomocą liczby całkowitej z zakresu 0 do k-1
s = 33

print("----------------------Trivial------------------------")
udzialy = [random.randint(0,k-1) for _ in range(n-1)]
udzialy.append((s - sum(udzialy)) % k)
print("wartości udziałów:",udzialy)

s_rozszyfrowane = (sum(udzialy)) % k

print("odkryty sekret:",s_rozszyfrowane)


#ODPOWIEDZI
# Dla jakich wartości metoda nie jest bezpieczna:
# Jeśli znasz n-1 udziałów, możesz dokładnie obliczyć ostatni udział, czyli sekret.

# Wady trywialnego podziału sekretu:
# a)Trzeba mieć wszystkie udziały — nie działa częściowa odbudowa.
# b) Każdy udział wpływa liniowo na sekret — ujawnienie dowolnych n-1 udziałów wystarcza do poznania sekretu.
# c) Brak matematycznej ochrony jak w Shamirze (brak interpolacji, krzywych, ciał skończonych).

# --------------------------------------------------------------------------------
# -----------------------------------SHAMIR---------------------------------------
# --------------------------------------------------------------------------------
print("----------------------Shamir------------------------")
# Sekret reprezentowany za pomocą liczby całkowitej z zakresu 0 do p-1
s = 33
# Liczba wszystkich udziałów
n = 3
# Liczba udziałów wymaganych do odtworzenia sekretu
t = n
# Duża liczba pierwsza taka, że p > s i p > n
p = randprime(max(s,n)+1, max(s,n)**2)

print("Wartość p:",p)
a = [random.randint(0,1000) for _ in range(t-1)]
print("a:",a)
udzialy = []
for i in range(1 , n+1):
    suma = s
    for j in range(1,t):
        suma += a[j - 1] * (i ** j)
    si = suma % p
    udzialy.append((i, si))

print("Wartości udziałów",udzialy)

s_rozszyfrowane = 0
suma = 0
for i in range(t):
    xi, yi = udzialy[i]
    iloczyn = 1
    for j in range(t):
        if j == i:
            continue
        else:
            xj, _ = udzialy[j]
            iloczyn *= (xj * pow(xj - xi, -1, p)) % p
    suma += yi* iloczyn
    suma %= p
s_rozszyfrowane = suma
print("Odkryty sekret:",s_rozszyfrowane)

