from sklearn.linear_model import LinearRegression
import numpy as np

import matplotlib.pyplot as plt

# usando regressão linear
def solve_a():
    a = [3, 5, 6, 7, 9, 14, 16, 16, None, 27, 34, 50, 61]
    x = [i for i in range(len(a))]

    if None in a:
        x.remove(a.index(None))

    y = [item for item in a if item != None]

    model = LinearRegression()
    model.fit(np.array(x).reshape((-1, 1)), y)

    prediction = model.predict(np.array([a.index(None)]).reshape(-1, 1))
    print(f"Prediction for a[8] = {prediction[0]}")

# usando média
def solve_b():
    b = [10, 9, 10, 11, 8, 11, 10, 12, None, 11, 10, 8, 10]
    clean = b.remove(None)
    b = [item if item != None else sum(clean)/len(clean) for item in b]

    print(f"Prediction for b[8] = {b[8]}")


# usando média entre dois valores adjacentes
def solve_c():
    c = [0, 2, 3, 0, 4, 2, 0, 6, 2, 0, 4, 5, None, 3, 4, None, 5]
    c = [item if item != None else (c[i-1] + c[i+1])/2 for i, item in enumerate(c)]
    print(f"Prediction for c[12], c[15] = {c[12]}, {c[15]}")


solve_a()
solve_b()
solve_c()