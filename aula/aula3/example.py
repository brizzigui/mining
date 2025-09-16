names = ["Steve", "Bill", "Martin"]
literature = [8.5, 9, 10]
math = [9, 9.5, 7]

table = [*zip(names, literature, math)]
print(table)

table = [names, literature, math]
print(table)

table = [(name, "Literatura" if k == 0 else "Matemática", literature[i] if k == 0 else math[i]) 
            for i, name in enumerate(names) 
            for k in range(2)]

print(table)