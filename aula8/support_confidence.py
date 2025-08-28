A = [0, 1, 0, 1, 0, 0, 1, 0, 0, 0]
target = [0, 1, 1, 1, 0, 0, 1, 0, 1, 1]

support = sum([A[i] and target[i] for i in range(len(A))]) / len(A)
print(support)

confidence = support / (sum([A[i] for i in range(len(A))]) / len(A))
print(confidence)

lift = support / ((sum(A) / len(A)) * (sum(target) / len(target)))
print(lift)