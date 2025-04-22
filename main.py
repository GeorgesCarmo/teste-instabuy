import pandas as pd
import requests
import json
import time

CSV_PATH = 'items.csv'
API_URL = 'https://api.instabuy.com.br/store/products'
API_KEY = 'IGs8rlcEb0jUEgsNvzDsatF5gAvQ_8iGde-tZ-iwGFc'
BATCH_SIZE = 5000

def normalize_date(date_str):
    '''
    Convert date string to ISO format
    params:
        date_str (str): Date string to be normalized
    returns:
        str: Normalized date string in ISO format or None if invalid
    '''
    if pd.isna(date_str):
        return None
    try:
        return pd.to_datetime(date_str, dayfirst=True).isoformat()
    except Exception:
        return None

def load_and_clean_data():
    '''
    Load and clean data from CSV
    params:
        None
    returns:
        pd.DataFrame: Cleaned DataFrame
    '''
    df = pd.read_csv(CSV_PATH, sep=';', decimal=',', on_bad_lines='skip')
    df['Preço regular'] = pd.to_numeric(df['Preço regular'], errors='coerce').fillna(0.0)
    df['Promocao'] = pd.to_numeric(df['Promocao'], errors='coerce').fillna(0.0)
    df['Data termino promocao'] = df['Data termino promocao'].apply(normalize_date)
    df['estoque'] = pd.to_numeric(df['estoque'], errors='coerce').fillna(0).astype(float)
    df['ativo'] = df['ativo'].astype(bool)
    df = df.dropna(subset=['Nome', 'Preço regular'])
    return df

def build_payload(row):
    '''
    Build payload for API request
    params:
        row (pd.Series): Row from DataFrame
    returns:
        dict: Payload for the product    
    '''
    product = {
        "internal_code": str(row['Código interno']),
        "visible": row['ativo'],
        "stock": row['estoque'],
        "name": row['Nome'],
        "barcodes": [str(row['Código de barras']).split('.')[0]] if pd.notna(row['Código de barras']) else [],
        "price": round(row['Preço regular'], 2),
        "promo_price": round(row['Promocao'], 2) if row['Promocao'] > 0 else None,
        "promo_end_at": row['Data termino promocao']
    }
    return product

def send_batch(products_batch):
    '''
    Send a batch of products to the API
    params:
        products_batch (list): List of product dictionaries
    returns:
        tuple: Status code and response from the API
    '''
    headers = {
        'api-key': API_KEY,
        'Content-Type': 'application/json'
    }
    payload = {"products": products_batch}
    response = requests.put(API_URL, headers=headers, data=json.dumps(payload))
    try:
        return response.status_code, response.json()
    except Exception:
        return response.status_code, response.text

def main():
    '''
    Main function to load data, process it, and send to API
    params:
        None
    returns:
        None
    '''
    df = load_and_clean_data()
    products = [build_payload(row) for _, row in df.iterrows()]

    for i in range(0, len(products), BATCH_SIZE):
        batch = products[i:i + BATCH_SIZE]
        print(f"Sending batch {i // BATCH_SIZE + 1} with {len(batch)} products...")
        status_code, response = send_batch(batch)
        print(f"Batch {i // BATCH_SIZE + 1}: Status [{status_code}] - Response: {response}")
        time.sleep(0.5)  # Optional: avoid hitting the API too fast

if __name__ == '__main__':
    main()
