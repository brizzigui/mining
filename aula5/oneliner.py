import random
x = [val if i != 5 else None for i, val in enumerate(random.sample(range(0, 30), 30))]
print([item if item != None else sum([item for item in x if item != None]) / len([item for item in x if item != None]) for item in x])