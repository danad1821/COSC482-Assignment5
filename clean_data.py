import pandas as pd
import re
import numpy as np

if __name__ == "__main__":
    df = pd.read_csv("ebay_tech_deals.csv")
    
    def extract_price(price_string):
        if isinstance(price_string, str):  
            match = re.search(r"[\d.]+", price_string)
            if match:
                try:
                    return float(match.group(0))
                except ValueError:
                    return None
            else:
                return None
        else:
            return None

    df['price'] = df['price'].apply(extract_price)
    df['original_price'] = df['original_price'].apply(extract_price)
    
    df["price"] = df["price"].fillna(df["price"].median(skipna=True))
    df["original_price"] = df["original_price"].fillna(df["price"])
    
    df["shipping"] = df["shipping"].fillna("Shipping info unavailable")
    
    df["price"] = pd.to_numeric(df['price'], errors="coerce")
    df["original_price"] = pd.to_numeric(df['original_price'], errors="coerce")
    df['original_price'] = np.where(df['original_price'] < df['price'], df['price'], df['original_price'])
    df["discount_percentage"] = ((1 - (df["price"]/df["original_price"]))*100).round(2)
    
    
    df.to_csv("cleaned_ebay_deals.csv")
    
    