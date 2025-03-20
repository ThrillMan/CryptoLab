state = 0b1001
for i in range(20):
    print("{:04b}".format(state))
    newbit = (state ^ (state >> 1)) & 0b1
    state = (state >> 1 ) | (newbit << 3)