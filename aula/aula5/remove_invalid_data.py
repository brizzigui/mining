import random

def mean(list):
    clear = [item for item in list if item != None]
    return sum(clear) / len(clear)

x = random.sample(range(0, 30), 30)
x[5] = None
print(x)


x = [item if item != None else mean(x) for item in x]
print(x)