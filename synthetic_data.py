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

# saving data to .csv file
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

# ----------------------------------------------------------------------------------------

# Task 2:
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_query(query):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(query)
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    return filtered_words

def query_transaction_data(transaction_data, query):
    words = preprocess_query(query)
    category_keywords = ['category', 'spending', 'expenses']
    time_keywords = ['past', 'months', 'inconsistent']

    relevant_categories = [word for word in words if word in category_keywords]
    relevant_time = [word for word in words if word in time_keywords]

    if relevant_categories and relevant_time:
        if 'mostly' in words:
            return analyze_spending_category(transaction_data, relevant_time[0])

    return "Sorry, I couldn't understand your query."

def analyze_spending_category(transaction_data, time_frame):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90) # 3 month timeframe

    if '6' in time_frame:
        start_date = end_date - timedelta(days=180) # 6 month timeframe

    relevant_transactions = filter_transactions_by_date(transaction_data, start_date, end_date)

    if not relevant_transactions.empty:  # checks if dataframe is empty
        category_counts = relevant_transactions['category'].value_counts()
        if not category_counts.empty:
            most_spent_category = category_counts.idxmax()

            # Generate a bar plot of spending by category
            plt.figure(figsize=(10, 6))
            category_counts.plot(kind='bar')
            plt.title(f'Spending by Category in the Last {time_frame}')
            plt.xlabel('Category')
            plt.ylabel('Spending')
            plt.show()

            return f"You mostly spent on {most_spent_category} in the {time_frame}."

    return f"No transactions found in the {time_frame}."

def filter_transactions_by_date(transaction_data, start_date, end_date):
    transactions = pd.DataFrame(transaction_data)
    transactions['date'] = pd.to_datetime(transactions['date'])
    mask = (transactions['date'] >= start_date) & (transactions['date'] <= end_date)
    return transactions[mask]

if __name__ == "__main__":
    # loads synthetic data generated from the previous script
    transaction_data = pd.read_csv("transaction_data.csv").to_dict(orient='records')

    # example queries
    query1 = "What category did I spend mostly on in the past 3 months?"
    query2 = "What spending category am I most inconsistent in?"

    # processing queries
    result1 = query_transaction_data(transaction_data, query1)
    result2 = query_transaction_data(transaction_data, query2)

    # printing results from queries
    print(result1)
    print(result2)