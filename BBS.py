from sympy import *
import random

# state = (1 << 127)
# print(bin(state))
# print(state)

minPrime = 10000
maxPrime = 100000000
cached_primes = [i for i in range(minPrime,maxPrime) if isprime(i) and i % 4 == 3]

p = random.choice([i for i in cached_primes])
q = random.choice([i for i in cached_primes])
print("p,q",p,q)

n = p * q

print("n",n)

cached_primes = [i for i in range(minPrime,maxPrime) if isprime(i)]
x  = random.choice([i for i in cached_primes])
print("x",x)
state = (x**2) % n

#used for cycles
cycles = []

#single bit test
n_1_count = 0

#series test
series_1 = 0
series_2 = 0
series_3 = 0
series_4 = 0
series_5 = 0
series_6 = 0
series_current_count = 0

#long series test
longest_series = 0

#poker test
poker_arr = [0 for i in range(16)]
poker_temp = ''

for i in range(1,20000):
    new_state = (state**2) % n
    output = bin(new_state)[-1]

    #series test

    #all the values in the table are times 2, something is off
    # if output==bin(state)[-1]:
    #     series_current_count+=1
    # else:
    #     series_current_count=0
    # if series_current_count==1:
    #     series_1+=1
    # if series_current_count==2:
    #     series_2+=1
    # if series_current_count==3:
    #     series_3+=1
    # if series_current_count==4:
    #     series_4+=1
    # if series_current_count==5:
    #     series_5+=1
    # if series_current_count>=6:
    #     series_6+=1
    #     longest_series = max(longest_series,series_current_count)

    if output==bin(state)[-1]:
        series_current_count+=1
    else:
        series_current_count=0
    if series_current_count==2:
        series_1+=1
    if series_current_count==3:
        series_2+=1
    if series_current_count==4:
        series_3+=1
    if series_current_count==5:
        series_4+=1
    if series_current_count==6:
        series_5+=1
    if series_current_count>=7:
        series_6+=1
        longest_series = max(longest_series,series_current_count)

    #poker test
    poker_temp+=output
    if len(poker_temp)>=4:
        poker_val = int(poker_temp,2)
        poker_arr[poker_val]+=1
        poker_temp=''

    state = new_state

    #test for cycles
    cycles.append(state)

    #single bit test
    if output=='1':n_1_count+=1

    print(output,end = "")
print('\n')

#test for cycles
cycles_result = [i for i, x in enumerate(cycles) if x == cycles[0]]
print(cycles_result)
if len(cycles_result)>1:
    print("there is a cycle in the series\n")
else:
    print("no cycle\n")

#single bit test
print(n_1_count)
if 9725<n_1_count<10275:
    print("single bit test passed")
else:
    print("single bit test NOT passed")

#series test
print("\nseries length")
print("1",series_1)
print("2",series_2)
print("3",series_3)
print("4",series_4)
print("5",series_5)
print("6",series_6)

if 2315<series_1<2685 and 1114<series_2<1386 and 527<series_3<723\
    and 240<series_4<384 and 103<series_5<209 and 103<series_6<209:
    print("series test passed")
else:
    print("series test NOT passed")

#longest series test:
print("\nseries len",longest_series)
if longest_series>=26:
    print("longest series NOT passed")
else:
    print("longest series passed")

#print(poker_arr)
poker_result = (16/5000)*sum(i*i for i in poker_arr)-5000
print("\npoker test:",poker_result)
if 2.16<poker_result<46.17:
    print("poker test passed")
else:
    print("poker test NOT passed")