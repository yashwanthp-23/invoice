# utils/data_loader.py
import pandas as pd
from pymongo import MongoClient

def load_data():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["invoice_bot"]
    
    # Load customer data
    customer_df = pd.read_csv("merged_indian_customer_data.csv")
    db.customers.insert_many(customer_df.to_dict(orient='records'))

    # Load product data
    product_df = pd.read_csv("dataset.csv")
    db.products.insert_many(product_df.to_dict(orient='records'))
