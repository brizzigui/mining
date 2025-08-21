# quantização dos dados do DimR00.csv

import matplotlib.pyplot as plt

def plot(x, y) -> None:
    plt.plot(x, y)
    plt.show()

def read() -> tuple[list[int], list[float]]:
    with open("./aula6/DimR00.csv") as file:
        file.readline()
        x = []
        y = []
        for line in file:
            x.append(int(line.split(",")[0].replace('"', '')))
            y.append(float(line.split(",")[1]))

        return x, y

def quantize(x: list[int], y: list[float]) -> tuple[list[int], list[float]]:
    amplitude = max(y) - min(y)
    options = 4
    classes = [min(y) + (amplitude / options) * i for i in range(options)]

    quantizezed_y = []
    for item in y:
        for i in range(len(classes)):
            if i == (len(classes) - 1):
                quantizezed_y.append(classes[-1])

            elif item >= classes[i] and item < classes[i+1]:
                quantizezed_y.append(classes[i])
                break

    return x, quantizezed_y

def main() -> None:
    x, y = read()
    plot(x, y)

    x, y = quantize(x, y)
    plot(x, y)

if __name__ == "__main__":
    main()