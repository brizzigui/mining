import pandas as pd

def read() -> pd.DataFrame:    
    data = []
    
    with open('kendo_matches_work.csv', 'r') as file:
        categories = file.readline().strip().split(",")
        for line in file:
            values = line.strip().split(",")

            if (len(values) != len(categories)):
                continue

            row = dict(zip(categories, values))

            try:
                summed = sum(int(values[i]) for i in range(5, 9))
                time = int(row["seconds_between"])
                ippons = int(row["ippon_taken"])
            except (ValueError, IndexError):
                continue

            if summed != 1 or time < 0 or time > 100 or ippons not in (0, 1):
                continue

            data.append(row)
    
    df = pd.DataFrame(data, columns=[
        "match_id", "ippon_number", "seconds_between", "ippon_taken", "men", "kote", "do", "tsuki"
    ])
    df = df.drop_duplicates()
    df.to_csv('cleaned.csv', index=False)
    
    return df

def mine(data: pd.DataFrame) -> pd.DataFrame:
    pass

def main() -> None:
    df = read()
    result = mine(df)

if __name__ == "__main__":
    main()