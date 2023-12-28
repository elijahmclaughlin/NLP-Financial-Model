# NLP Financial Model

## Task 1: Generating Fake User Bank and Credit Card Transaction Data
>[!IMPORTANT]
>Review **synthetic_data.ipynb**

**In (3)**: I defined a predetermine set of merchants and categories.  
**In (4)**: This is the actual generation of transactional data. It's generated randomly between two dates, time, and the amount is random.  
**In (5) & (6)**: These are the saving of the data to CSV and JSON files.  
**In (7)**: This is the main function, and calls upon the other three functions to generate and save the data.  

## Task 2: Developing an NLP Model for Querying Transaction Data
>[!IMPORTANT]
>Review **nlp_fin.ipynb**

**In (3)**: Preprocessing the query to be in English.  
**In (4)**: defining the transactions to be filtered by date.  
**In (5)**: defining the spending category by time frame (3 and 6 months).  
**In (6) & (7)**: defining inconsistent and consistent spending, respectively.  
**In (8)**: defining the query transaction process.  
**In (9)**: This is the main function, and uses the other functions to analyze the queries, and then respond.  
  
### Here are the queries and responses:  
Q.1: "What category did I spend mostly on in the past 3 months?"  
A.1: You mostly spent on 'Health and Fitness' from 'Amazon' in the past.  
Q.2: "What spending category am I most inconsistent in?"  
A.2: Your most inconsistent category (high spending variance): Travel  
Q.3: "What spending category am I most consistent in?"  
A.3: Your most consistent category (low spending variance): Electronics  
Q.4: "What category did I spend mostly on in the past 6 months?"  
A.4: You mostly spent on 'Health and Fitness' from 'Amazon' in the past.  

>[!NOTE]
>For Q.2 and Q.3, there are graphs associated with the answers as well.
