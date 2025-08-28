def q1(dataset: list[dict]) -> list[dict]:
    return [{"Nome": line["Nome"], "Afiliação": line["Afiliação"], "QI": line["QI"]} 
            for line in dataset if line["Afiliação"] == "Avengers"]

def q2(dataset: list[dict]) -> list[dict]:
    return [*filter(lambda x: x["QI"] == "NA", dataset)]

def q3(dataset: list[dict]) -> list[dict]:
    return [*filter(lambda x: x["QI"] != "NA" and int(x["QI"]) > 120, dataset)]

def q4(dataset: list[dict]) -> list[dict]:
    return sorted(dataset, key=lambda x : x["QI"], reverse=True)

def main() -> None:
    data = []

    with open("fakeMarvelData.csv", encoding="iso8859-1") as file:
        categories = file.readline().replace("\n", "").split(",")
        for line in file:
            vals = dict(zip(categories, line.replace("\n", "").split(",")))
            data.append(vals)

    print(q1(data))
    print(q2(data))
    print(filtered := q3(data))
    print(q4(filtered))

if __name__ == "__main__":
    main()
    