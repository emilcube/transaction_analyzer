import pandas as pd
from datetime import datetime
import os

def create_dataframe(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")  # Raise an error if file is not found

    transactions = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            parts = line.split(' - ')

            datetime_str = parts[0]  # Пример: "2024-09-01 21:48"

            title = parts[1]
            amount_str = parts[2].replace(' ', '')  # Убираем пробелы из суммы

            datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')

            transactions.append({
                'Datetime': datetime_obj,
                'Title': title,
                'Amount': float(amount_str)
            })

    df = pd.DataFrame(transactions)

    return df
