import numpy as np
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt


model = LinearRegression()
model.fit(x, y)

plt.plot(x, y)