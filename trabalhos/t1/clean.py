import pandas as pd

def read() -> pd.DataFrame:
    pass

def mine(data: pd.DataFrame) -> pd.DataFrame:
    pass

def main() -> None:
    df = read()
    result = mine(df)

if __name__ == "__main__":
    main()