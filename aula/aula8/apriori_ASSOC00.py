import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

with open("./aula8/_ASSOC00.csv") as file:
    categories = file.readline().replace("\n", "").strip().split(",")
    transactions = []
    for line in file:
        transactions.append(line.replace("\n", "").strip().split(","))    

    data = {}
    for item in transactions:
        for i in range(len(item)):
            if i > 0:
                if categories[i] not in data:
                    data[categories[i]] = []

                data[categories[i]].append(bool(int(item[i]))) 

    df = pd.DataFrame(data)

result = apriori(df, min_support=0.01, use_colnames=True)
rules = association_rules(result, metric="lift", min_threshold=1).sort_values(by="support", ascending=False)
filtered_df = rules[rules["antecedents"].apply(lambda x: "Carne" in x)]
print(filtered_df)