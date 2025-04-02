import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Test implementation of the key functions from hsn_transaction_system.py

def generate_sample_transactions(count=10, hsn_code=None):
    """Generate sample transaction data"""
    
    transaction_types = ["Inward", "Outward", "Transfer", "Return"]
    status_options = ["Completed", "Pending", "Cancelled", "On Hold"]
    hsn_codes = ["6109", "6203", "6204", "6110", "6205", "4202", "6403", "6104", "6206", "6201"]
    product_categories = [
        "T-shirts", "Men's trousers", "Women's suits", "Sweaters", "Men's shirts",
        "Handbags", "Footwear", "Women's suits (knitted)", "Women's blouses", "Men's coats"
    ]
    
    # Map HSN codes to product categories
    hsn_to_product = dict(zip(hsn_codes, product_categories))
    
    # Filter by HSN code if provided
    if hsn_code:
        filtered_hsn = [code for code in hsn_codes if str(hsn_code) in code]
        if filtered_hsn:
            hsn_codes = filtered_hsn
        else:
            hsn_codes = [str(hsn_code)]
    
    transactions = []
    for i in range(count):
        # Generate a random date within the last 30 days
        random_days = random.randint(0, 30)
        trans_date = (datetime.now() - timedelta(days=random_days)).strftime("%Y-%m-%d")
        
        # Randomly select HSN code and map to product category
        selected_hsn = random.choice(hsn_codes)
        product_cat = hsn_to_product.get(selected_hsn, "Other products")
        
        # Create transaction
        transaction = {
            "Transaction ID": f"TRX-{random.randint(10000, 99999)}",
            "Date": trans_date,
            "HSN Code": selected_hsn,
            "Product Category": product_cat,
            "Quantity": random.randint(10, 1000),
            "Value": round(random.uniform(1000, 50000), 2),
            "Transaction Type": random.choice(transaction_types),
            "Status": random.choice(status_options),
            "Location": random.choice(["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad"]),
            "User": f"User-{random.randint(1, 20)}"
        }
        transactions.append(transaction)
    
    return pd.DataFrame(transactions)

def generate_hsn_distribution():
    """Generate HSN distribution data for visualization"""
    
    # Define HSN sections, chapters, and codes
    sections = {
        "Section XI": "Textiles and textile articles",
        "Section VIII": "Raw hides, leather, furskins",
        "Section XII": "Footwear, headgear",
        "Section XX": "Miscellaneous manufactured articles"
    }
    
    # Define chapters under each section
    chapters = {
        "Chapter 61": "Articles of apparel and clothing accessories, knitted or crocheted",
        "Chapter 62": "Articles of apparel and clothing accessories, not knitted or crocheted",
        "Chapter 63": "Other made-up textile articles",
        "Chapter 42": "Articles of leather",
        "Chapter 64": "Footwear, gaiters",
        "Chapter 94": "Furniture, bedding, lamps"
    }
    
    # Map chapters to sections
    chapter_to_section = {
        "Chapter 61": "Section XI",
        "Chapter 62": "Section XI",
        "Chapter 63": "Section XI",
        "Chapter 42": "Section VIII",
        "Chapter 64": "Section XII",
        "Chapter 94": "Section XX"
    }
    
    # Define HSN codes
    hsn_codes = {
        "6109": "T-shirts, singlets and other vests, knitted or crocheted",
        "6110": "Sweaters, pullovers, sweatshirts, waistcoats (vests) and similar articles, knitted or crocheted",
        "6203": "Men's or boys' suits, ensembles, jackets, blazers, trousers, bib and brace overalls, breeches and shorts",
        "6204": "Women's or girls' suits, ensembles, jackets, blazers, dresses, skirts, divided skirts, trousers, bib and brace overalls, breeches and shorts",
        "6205": "Men's or boys' shirts",
        "6206": "Women's or girls' blouses, shirts and shirt-blouses",
        "4202": "Trunks, suitcases, vanity cases, executive-cases, briefcases, school satchels and similar containers",
        "6403": "Footwear with outer soles of rubber, plastics, leather or composition leather and uppers of leather",
        "6404": "Footwear with outer soles of rubber, plastics, leather or composition leather and uppers of textile materials",
        "9403": "Other furniture and parts thereof"
    }
    
    # Map HSN codes to chapters
    code_to_chapter = {
        "6109": "Chapter 61",
        "6110": "Chapter 61",
        "6203": "Chapter 62",
        "6204": "Chapter 62",
        "6205": "Chapter 62",
        "6206": "Chapter 62",
        "4202": "Chapter 42",
        "6403": "Chapter 64",
        "6404": "Chapter 64",
        "9403": "Chapter 94"
    }
    
    # Generate data for the treemap
    data = []
    for code, description in hsn_codes.items():
        chapter = code_to_chapter[code]
        section = chapter_to_section[chapter]
        
        # Random values for each HSN code
        transaction_count = random.randint(20, 500)
        value = random.randint(50000, 5000000)
        
        data.append({
            "HSN Code": code,
            "Description": description,
            "HSN Chapter": chapter,
            "HSN Section": section,
            "Transaction Count": transaction_count,
            "Value": value
        })
    
    return pd.DataFrame(data)

# Test function execution
if __name__ == "__main__":
    print("Testing generate_sample_transactions()...")
    transactions = generate_sample_transactions(5)
    print(transactions[["Transaction ID", "HSN Code", "Product Category", "Transaction Type", "Status"]])
    print("\n")
    
    print("Testing generate_hsn_distribution()...")
    hsn_data = generate_hsn_distribution()
    print(hsn_data[["HSN Code", "HSN Chapter", "HSN Section", "Transaction Count"]].head())
    
    print("\nAll functions tested successfully!")