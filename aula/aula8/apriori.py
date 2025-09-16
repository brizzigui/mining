import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

df = pd.DataFrame(
    {
        "a": [1, 1, 0, 0, 1],
        "b": [0, 1, 0, 1, 1],
        "c": [0, 1, 1, 0, 1],
        "target": [1, 0, 1, 0, 1]
    }
)

print(df)

df = df.map(bool)

print(result := apriori(df, min_support=0.01, use_colnames=True))
print(association_rules(result, metric="lift", min_threshold=1))