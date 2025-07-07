import pandas as pd


def write_to_csv(fighter_data_list, filename='fighters.csv'):
    df = pd.DataFrame(fighter_data_list)
    df.to_csv(filename, index=False)