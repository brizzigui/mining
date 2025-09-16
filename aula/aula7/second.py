import math

def min_max_normalize(lower: float, upper: float, data: list[dict]) -> list[dict]:
    clone = [val.copy() for val in data]
    for key in clone[0].keys():
        max_x = max(clone, key=lambda x: x[key])[key]
        min_x = min(clone, key=lambda x: x[key])[key]

        for val in clone:
            val[key] = (val[key] - min_x) / (max_x - min_x) * (upper - lower) + lower  

    return clone                     

def z_score_normalize(data: list[dict]) -> list[dict]:
    clone = [val.copy() for val in data]
    for key in clone[0].keys():
        sum_x = sum([val[key] for val in clone])
        mean = sum_x / len(clone)
        sd = (sum([(val[key] - mean)**2 for val in clone]) / (len(clone) - 1))**(1/2)

        for val in clone:
            val[key] = (val[key] - mean) / sd

    return clone

def decimal_scaling(data: list[dict]) -> list[dict]:
    clone = [val.copy() for val in data]
    for key in clone[0].keys():
        max_x = max(clone, key=lambda x: x[key])[key]

        j = -math.log(1/max_x, 10)
        for val in clone:
            val[key] = val[key] / (10**j)
        
    return clone

def main() -> None:
    data = []

    with open("vendas_lucro.csv") as file:
        categories = file.readline().replace("\n", "").split(",")
        for line in file:
            vals = dict(zip(categories, map(int, line.replace("\n", "").split(","))))
            data.append(vals)

    print("\n----- Min Max -----")
    clone = min_max_normalize(0, 1, data)
    print(clone)

    print("\n----- Z Score -----")
    clone = z_score_normalize(data)
    print(clone)

    print("\n----- Decimal -----")
    clone = decimal_scaling(data)
    print(clone)




if __name__ == "__main__":
    main()