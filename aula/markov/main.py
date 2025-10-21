import matplotlib.pyplot as plt

index_dict = {"F": 0, "A": 1, "Q": 2, "MQ": 3}

def init_matrix(size: int) -> list[list]:
    l = []
    for i in range(size):
        l.append([0] * size)

    return l

def run(state: int, times: int, transitions: list[list]) -> list[float]:
    current = [0.0] * len(transitions)
    current[state] = 1.0

    for _ in range(times):
        next_state = [0.0] * len(transitions)
        for i in range(len(transitions)):
            for j in range(len(transitions)):
                next_state[i] += current[j] * transitions[j][i]
        current = next_state

    return current

def fit(data: list[int]) -> list[list]:
    transitions = init_matrix(4)
    for i in range(len(data)-1):
        val_from = index_dict[data[i]]
        val_to = index_dict[data[i+1]]

        transitions[val_from][val_to] += 1

    for i in range(len(transitions)):
        transitions[i] = [k / (sum(transitions[i])) for k in transitions[i]]
    
    return transitions

def read() -> list[float]:
    temps = []
    with open("TemperaturaSM_2022_aug_oct.csv", "r", encoding="utf8") as file:
        file.readline()
        for line in file:
            try:
                temps.append(float(line.split(",")[2]))
            except:
                pass
    
    return temps

def classify(temps) -> list[int]:
    classes = []
    for temp in temps:
        if temp < 15:
            classes.append("F")
        elif temp <= 25:
            classes.append("A")
        elif temp <= 30:
            classes.append("Q")
        else:
            classes.append("MQ")
    
    return classes
        

def main() -> None:
    temps = read()
    classes = classify(temps)
    transitions = fit(classes)
    print(transitions)

    results = run(2, 3, transitions)
    print(results)

if __name__ == "__main__":
    main()