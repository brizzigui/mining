import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def write_output(header: str, data, append: bool = True) -> None:
    mode = 'a' if append else 'w'
    with open('output.txt', mode, encoding='utf-8') as file:
        file.write(f"{'='*50}\n")
        file.write(f"{header}\n")
        file.write(f"{'='*50}\n")
        
        if isinstance(data, pd.DataFrame):
            file.write(data.to_string())
            file.write("\n\n")
        elif isinstance(data, (int, float, str)):
            file.write(str(data))
            file.write("\n\n")

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

def read() -> dict:   
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
                        val = {f"{key}_1": int(row[key]) for key in useful_categories}
                        match_id = row["match_id"] 

                    else:
                        row = {f"{key}_2": int(row[key]) for key in useful_categories}
                        data.append(val | row) 

                    match_count -= 1

    df = pd.DataFrame(data, columns=[
        *data[0].keys()
    ])
    df.to_csv('cleaned.csv', index=False)

    return data

def attack_implies_in_not(data: dict) -> pd.DataFrame:
    lhs = ["men_1", "kote_1", "do_1", "tsuki_1"]
    rhs = ["men_2", "kote_2", "do_2", "tsuki_2"]

    df = [
            {key: bool(val[key]) if i < 4 else not bool(val[key]) for i, key in 
                enumerate(lhs + rhs)
            } 
            for val in data
        ]
    df = pd.DataFrame(df, columns=[
        *df[0].keys()
    ])


    sets = apriori(df, min_support=0.01, use_colnames=True)   
    rules = association_rules(sets, metric="confidence", min_threshold=0.9).sort_values(by="support", ascending=False)
    rules = rules[
        (rules['antecedents'].apply(len) == 1) &
        (rules['consequents'].apply(len) == 1)
    ]


    rules = rules[
        rules['antecedents'].apply(lambda x: list(x)[0] in lhs) &
        rules['consequents'].apply(lambda x: list(x)[0] in rhs)
    ]

    return rules

def men_implies_ippon(data: dict) -> float:
    firsts = ["men_1", "ippon_taken_1"]
    seconds = ["men_2", "ippon_taken_2"]
    netral_notation = ["men", "ippon_taken"]

    df = []
    for val in data:
        df.append({nkey: bool(val[key]) for nkey, key in zip(netral_notation, firsts)})
        df.append({nkey: bool(val[key]) for nkey, key in zip(netral_notation, seconds)})

    df = pd.DataFrame(df, columns=[
        *df[0].keys()
    ])

    sets = apriori(df, min_support=0.01, use_colnames=True)   
    rules = association_rules(sets, metric="confidence", min_threshold=0.01).sort_values(by="support", ascending=False)

    return rules.iat[0, 5]

def slow_attacks(data: dict) -> pd.DataFrame:
    lhs = ["men_2", "kote_2", "do_2", "tsuki_2"]
    rhs = ["over25"]

    df = []
    for val in data:
        df.append({key: bool(val[key]) for key in lhs} |
                  {"over25": bool(val["seconds_between_2"] > 25)})

    df = pd.DataFrame(df, columns=[
        *df[0].keys()
    ])

    sets = apriori(df, min_support=0.01, use_colnames=True)   
    rules = association_rules(sets, metric="confidence", min_threshold=0.85).sort_values(by="support", ascending=False)

    rules = rules[
        (rules['antecedents'].apply(len) == 1) &
        (rules['consequents'].apply(len) == 1)
    ]

    rules = rules[
        rules['antecedents'].apply(lambda x: list(x)[0] in lhs) &
        rules['consequents'].apply(lambda x: list(x)[0] in rhs)
    ]

    return rules

def failed_slow_attacks(data: dict) -> pd.DataFrame:
    lhs = ["slow_attacks"]
    rhs = ["failed_men_2", "failed_kote_2", "failed_do_2", "failed_tsuki_2"]

    df= []
    for val in data:
        row = {
            "slow_attacks": val["seconds_between_1"] > 15 and val["seconds_between_2"] > 25,
            "failed_men_2": bool(val["men_2"]) and not bool(val["ippon_taken_2"]),
            "failed_kote_2": bool(val["kote_2"]) and not bool(val["ippon_taken_2"]),
            "failed_do_2": bool(val["do_2"]) and not bool(val["ippon_taken_2"]),
            "failed_tsuki_2": bool(val["tsuki_2"]) and not bool(val["ippon_taken_2"]),
        }
        df.append(row)

    df = pd.DataFrame(df)

    sets = apriori(df, min_support=0.01, use_colnames=True)
    rules = association_rules(sets, metric="confidence", min_threshold=0.01)

    rules = rules[
        (rules['antecedents'].apply(lambda x: set(x) == set(lhs))) &
        (rules['consequents'].apply(lambda x: len(x) == 1 and list(x)[0] in rhs))
    ].sort_values(by="confidence", ascending=False)

    return rules

def consecutive_blows(data: dict) -> float:
    lhs = ["ippon_taken_1"]
    rhs = ["ippon_taken_2"]

    df = []
    for val in data:
        row = {
            "ippon_taken_1": bool(val["ippon_taken_1"]),
            "ippon_taken_2": bool(val["ippon_taken_2"]),
        }
        df.append(row)
    
    df = pd.DataFrame(df)

    sets = apriori(df, min_support=0.01, use_colnames=True)
    rules = association_rules(sets, metric="confidence", min_threshold=0.01)

    rules = rules[
        (rules['antecedents'].apply(lambda x: set(x) == set(lhs))) &
        (rules['consequents'].apply(lambda x: set(x) == set(rhs)))
    ].sort_values(by="confidence", ascending=False)

    return rules.iat[0, 5]

def get_antedecent(rule) -> str:
    return list(rule)[0]

def follow_up_attack(data: dict) -> pd.DataFrame:
    lhs = ["men_1", "kote_1", "do_1", "tsuki_1"]
    rhs = ["men_2", "kote_2", "do_2", "tsuki_2"]

    df = []
    for val in data:
        row = {key: bool(val[key]) for key in lhs + rhs}
        df.append(row)

    df = pd.DataFrame(df)

    sets = apriori(df, min_support=0.01, use_colnames=True)
    rules = association_rules(sets, metric="confidence", min_threshold=0.01)

    rules = rules[
        (rules['antecedents'].apply(lambda x: len(x) == 1 and list(x)[0] in lhs)) &
        (rules['consequents'].apply(lambda x: len(x) == 1 and list(x)[0] in rhs))
    ].sort_values(by="confidence", ascending=False)

    rules = rules.sort_values('confidence', ascending=False).groupby(
        rules['antecedents'].apply(get_antedecent)
    ).head(1)

    return rules

def mine(data: dict) -> None:
    # for question 1
    q1 = attack_implies_in_not(data)
    write_output("Questão 1: golpe implica não uso de outro golpe", q1, append=False)

    # for question 2
    q2 = men_implies_ippon(data)
    write_output("Questão 2: confiança, atleta que aplicou men levou ippon", q2)

    # for question 3
    q3 = slow_attacks(data)
    write_output("Questão 3: segundo golpe lento", q3)

    # for question 4
    q4 = failed_slow_attacks(data)
    write_output("Questão 4: segundo golpe lento falhou", q4)

    qb1 = consecutive_blows(data)
    write_output("Bônus 1: ippon consecutivo", qb1)

    qb2 = follow_up_attack(data)
    write_output("Bônus 2: golpe de follow up", qb2)

def main() -> None:
    data = read()
    mine(data)

if __name__ == "__main__":
    main()