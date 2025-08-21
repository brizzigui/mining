import csv
import matplotlib.pyplot as plt

def clean_dataset() -> list:
    with open("./aula5/LD00c.csv", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)
        print(header)

        lines = [line for line in reader]
        dataframe = []

        for line in range(0, len(lines), 2):
            entry = {}
            for index, key in enumerate(header):
                entry[key] = lines[line][index] if lines[line][index] != "" else lines[line+1][index]
                if index >= 3:
                    entry[key] = float(entry[key])
            
            dataframe.append(entry)
                
        return dataframe
    
def stats_per_var(dataframe: list[dict]) -> None:
    vars = list(dataframe[0].keys())

    for var in vars[3:]:
        stat = {"type": var}
        count = 0
        for entry in dataframe:
            if "min" not in stat:
                stat["min"] = entry[var]

            else:
                stat["min"] = min(stat["min"], entry[var])

            if "max" not in stat:
                stat["max"] = entry[var]

            else:
                stat["max"] = max(stat["max"], entry[var])

            if "total" not in stat:
                stat["total"] = entry[var]

            else:
                stat["total"] += entry[var]

            count += 1
        stat["mean"] = stat["total"] / count

        print(stat)


def find_max_attribute(dataframe: list[dict], attribute: str) -> None:
    max_entry = {attribute: -float("inf")}

    for entry in dataframe:
        max_entry = max(max_entry, entry, key=lambda x : x[attribute])

    print(f"--- Maior {attribute }: ---")
    print(max_entry)

def histogram_min_temp(dataframe: list[dict]) -> None:
    x = {}
    for entry in dataframe:
        val = entry["TempMinima"]
        if val not in x:
            x[val] = 1
        else:
            x[val] += 1

    plt.hist(x)
    plt.show()

def main() -> None:
    dataframe = clean_dataset()
    # print(dataframe)
    stats_per_var(dataframe)
    find_max_attribute(dataframe, "Insolacao")
    find_max_attribute(dataframe, "TempMaxima")
    print("Some max temp and min temp are noise and should be cleaned")
    histogram_min_temp(dataframe)


if __name__ == "__main__":
    main()