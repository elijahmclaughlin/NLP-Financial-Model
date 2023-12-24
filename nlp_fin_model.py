# Task 2:
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px


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
    time_keywords = ['past', 'months', 'inconsistent', 'consistent']

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

            return f"You mostly spent on '{most_spent_category}' in the {time_frame}."

    return f"No transactions found in the {time_frame}."

def filter_transactions_by_date(transaction_data, start_date, end_date):
    transactions = pd.DataFrame(transaction_data)
    transactions['date'] = pd.to_datetime(transactions['date'])
    mask = (transactions['date'] >= start_date) & (transactions['date'] <= end_date)
    return transactions[mask]

def query_transaction_data(transaction_data, query):
    words = preprocess_query(query)
    category_keywords = ['category', 'spending', 'expenses']
    time_keywords = ['past', 'months', 'inconsistent', 'consistent', 'regular', 'uniform']

    relevant_categories = [word for word in words if word in category_keywords]
    relevant_time = [word for word in words if word in time_keywords]

    if relevant_categories and relevant_time:
        if 'mostly' in words:
            return analyze_spending_category(transaction_data, relevant_time[0])
        elif 'inconsistent' in words:
            return analyze_inconsistent_spending(transaction_data)
        elif 'consistent' in words:
            return analyze_consistent_spending(transaction_data)

    return "Sorry, I couldn't understand your query."

def analyze_inconsistent_spending(transaction_data):
    # converting transaction_data to a df
    transactions = pd.DataFrame(transaction_data)
    transactions['date'] = pd.to_datetime(transactions['date'])

    # calculating sd for each spending category
    category_std = transactions.groupby('category')['amount'].std()

    # finding the category with the highest sd
    inconsistent_category = category_std.idxmax()

    fig = px.bar(x=category_std.index, y=category_std.values,
                 labels={'x': 'Spending Category', 'y': 'Standard Deviation of Spending'})
    fig.update_layout(title='Spending Variation by Category', xaxis_tickangle=-45)
    fig.show()

    return f"Your most inconsistent category (high spending variance): {inconsistent_category}"

# repeating to find the most consistent
def analyze_consistent_spending(transaction_data):
    transactions = pd.DataFrame(transaction_data)
    transactions['date'] = pd.to_datetime(transactions['date'])

    category_std = transactions.groupby('category')['amount'].std()

    consistent_category = category_std.idxmin()

    fig = px.bar(x=category_std.index, y=category_std.values,
                 labels={'x': 'Spending Category', 'y': 'Standard Deviation of Spending'})
    fig.update_layout(title='Spending Variation by Category', xaxis_tickangle=-45)
    fig.show()

    return f"Your most consistent category (low spending variance): {consistent_category}"

if __name__ == "__main__":
    # loads synthetic data generated from the previous script
    transaction_data = pd.read_csv("transaction_data.csv", sep=',').to_dict(orient='records')

    # example queries
    query1 = "What category did I spend mostly on in the past 3 months?"
    query2 = "What spending category am I most inconsistent in?"
    query3 = "What spending category am I most consistent in?"
    query4 = "What category did I spend mostly on in the past 6 months?"

    # processing queries
    result1 = query_transaction_data(transaction_data, query1)
    result2 = query_transaction_data(transaction_data, query2)
    result3 = query_transaction_data(transaction_data, query3)
    result4 = query_transaction_data(transaction_data, query4)

    # printing results from queries
    print(result1)
    print(result2)
    print(result3)
    print(result4)