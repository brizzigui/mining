import matplotlib.pyplot as plt

index_dict = {}
gl_index = 0

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
    global gl_index
    transitions = init_matrix(len(set(data)))
    print(len(set(data)))
    for i in range(len(data)-1):
        if data[i] not in index_dict:
            index_dict[data[i]] = gl_index
            gl_index += 1

        if data[i+1] not in index_dict:
            index_dict[data[i+1]] = gl_index
            gl_index += 1

        val_from = index_dict[data[i]]
        val_to = index_dict[data[i+1]]

        transitions[val_from][val_to] += 1

    for i in range(len(transitions)):
        transitions[i] = [k / (sum(transitions[i])) for k in transitions[i]]
    
    return transitions

def read() -> list[float]:
    temps = []
    with open("genesis_1.txt", "r", encoding="utf8") as file:
        file.readline()
        for line in file:
            for token in line.split():
                temps.append(token)
    
    return temps
       

def main() -> None:
    tokens = read()
    transitions = fit(tokens)
    print(transitions)

    while True:
        print("Type the starting word: ")
        results = run(index_dict[input()], 30, transitions)
        print(results)

if __name__ == "__main__":
    main()