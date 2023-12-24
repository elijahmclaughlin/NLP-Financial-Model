import csv
import json
from faker import Faker
from random import randint
from datetime import datetime, timedelta

fake = Faker()

# Task 1: Generating Fake User Bank and Credit Card Transaction Data
# generating a list of transaction data between two dates
def generate_transaction_data(start_date, end_date, num_transactions):
    """
    :param start_date: start date for the transactions.
    :param end_date: end date for the transactions.
    :param num_transactions: number of transactions to generate.
    :return: list of dictionaries containing the transaction data.
    """
    transaction_data = []

    for _ in range(num_transactions):
        transaction_date = fake.date_time_between_dates(datetime_start=start_date, datetime_end=end_date)
        amount = round(randint(1, 1000) + randint(0, 99) / 100, 2)  # Random amount between 1 and 1000
        merchant = fake.company()
        category = fake.word()

        transaction = {
            "date": transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
            "amount": amount,
            "merchant": merchant,
            "category": category,
        }
        transaction_data.append(transaction)

    return transaction_data

# saving data to .csv file
def save_to_csv(data, filename):
    """
    :param data: data to save.
    :param filename: name of the file to save the data to.
    """
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ["date", "amount", "merchant", "category"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

# saving data to .json file
def save_to_json(data, filename):
    """
    :param data: data to save.
    :param filename: name of the file to save the data to.
    """
    try:
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=2)
    except Exception as e:
        print(f"Error saving data to JSON: {e}")

if __name__ == "__main__":
    start_date = datetime.now() - timedelta(days=730)  # 24 months ago
    end_date = datetime.now()
    num_transactions = 1000

    transaction_data = generate_transaction_data(start_date, end_date, num_transactions)

    csv_filename = "transaction_data.csv"
    json_filename = "transaction_data.json"

    save_to_csv(transaction_data, csv_filename)
    save_to_json(transaction_data, json_filename)

    print(f"Transaction data generated and saved to {csv_filename} and {json_filename}.")