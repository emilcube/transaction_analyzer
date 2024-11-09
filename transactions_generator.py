import random
from datetime import datetime, timedelta

# Generate transactions from September 1, 2024, to December 15, 2024
start_date = datetime(2024, 9, 1)
end_date = datetime(2024, 12, 15)

# Initialize variables
transactions = []
current_date = start_date

# Generate transactions for each day, with two income transactions per month
while current_date < end_date:
    # Random number of transactions per day (1 to 5 transactions per day)
    num_transactions = random.randint(1, 5)

    for _ in range(num_transactions):
        # Generate a random transaction type (TRANSACTION<number> where number is between 1 and 10)
        transaction_number = random.randint(1, 10)
        # Generate transaction amounts between -30000 and -10000
        amount = random.randint(-30000, -10000)
        transaction = f"{current_date.strftime('%Y-%m-%d %H:%M')} - TRANSACTION{transaction_number} - {amount}"
        transactions.append(transaction)
    
    # Add two income transactions each month with a deviation around 1 million (±10,000)
    if current_date.day == 1 or current_date.day == 15:  # Add income on 1st and 15th of every month
        income = random.randint(900000, 1090000)  # Income around 1 million with ±10,000
        income_transaction = f"{current_date.strftime('%Y-%m-%d %H:%M')} - INCOME - {income}"
        transactions.append(income_transaction)

    # Move to the next day
    current_date += timedelta(days=1)

# Write to the file without seconds in the time format
with open("transactions_test.txt", 'w') as file:
    for transaction in transactions:
        file.write(transaction + '\n')
