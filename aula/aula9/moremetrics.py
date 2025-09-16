def invert(v: bool) -> bool:
    return not v

def support_unary(A: list[bool]) -> float:
    return sum([A[i] for i in range(len(A))]) / len(A)

def support_binary_implication(A: list[bool], B: list[bool]) -> float:
    return sum([A[i] and B[i] for i in range(len(A))]) / len(A)

def confidence(A: list[bool], B: list[bool]) -> float:
    return (support_binary_implication(A, B) / support_unary(A))
     
def conviction(A: list[bool], B: list[bool]) -> float:
    not_B = [*map(invert, B)]
    union = [a and not b for a, b in zip(A, B)]
    return support_unary(A) * support_unary(not_B) / support_unary(union)

def leverage(A: list[bool], B: list[bool]) -> float:
    return support_binary_implication(A, B) - support_unary(A)*support_unary(B)

def added_value(A: list[bool], B: list[bool]) -> float:
    return confidence(A, B) - support_unary(B)

A       = [1, 1, 0, 0, 1, 1, 0, 1]
B       = [0, 1, 0, 1, 1, 0, 0, 0]
C       = [0, 1, 1, 0, 1, 1, 1, 0]
goal    = [1, 0, 1, 0, 1, 1, 1, 1]

print(support_binary_implication(A, goal))
print(confidence(A, goal))
print(conviction(A, goal))
print(leverage(A, goal))
print(added_value(A, goal))