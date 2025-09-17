import pandas as pd

def verify(row: dict) -> bool:
    try:
        summed = sum(int(row[key]) for key in ["men", "kote", "do", "tsuki"])
        time = int(row["seconds_between"])
        ippons = int(row["ippon_taken"])

    except (ValueError, IndexError):
        return False

    if summed != 1 or time < 0 or time > 100 or ippons not in (0, 1):
        return False
    
    return True

def read() -> pd.DataFrame:   
    data = []
    match_id = None
    match_count = 2
    
    with open('kendo_matches_work.csv', 'r') as file:
        categories = file.readline().strip().split(",")
        useful_categories = ["seconds_between", "ippon_taken", "men", "kote", "do", "tsuki"]

        for line in file:
            values = line.strip().split(",")

            if (len(values) != len(categories)):
                continue

            row = dict(zip(categories, values))
            
            if verify(row):
                if match_id != row["match_id"]:
                    match_count = 2

                if match_count > 0:
                    if match_id != row["match_id"]:
                        val = {f"{key}_1": row[key] for key in useful_categories}
                        match_id = row["match_id"] 

                    else:
                        row = {f"{key}_2": row[key] for key in useful_categories}
                        data.append(val | row) 

                    match_count -= 1

    
    df = pd.DataFrame(data, columns=[
        *data[0].keys()
    ])
    df.to_csv('cleaned.csv', index=False)
    
    return df

def mine(data: pd.DataFrame) -> pd.DataFrame:
    pass

def main() -> None:
    df = read()
    result = mine(df)

if __name__ == "__main__":
    main()