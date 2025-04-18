# 💪 Instabuy Product Integration – April 2025

This script reads a CSV file containing product data and updates the Instabuy API in batches using authenticated PUT requests.

## 📦 Features

- CSV parsing and data cleaning using `pandas`
- Handles promotion prices, stock, and activation flags
- Sends requests in batches of 50 products
- Includes simple logging and error handling

## 🛠️ Technologies

- Python 3.8+
- pandas
- requests

## 🗂️ File Structure

- `main.py` → Main script for processing and sending product data
- `items.csv` → CSV file with product information (sample provided)
- `requirements.txt` → Dependencies to install with pip

## 🚀 How to Run

1. Clone this repository or download the files.

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Place your `items.csv` file in the root directory. The file must contain the following columns:

   ```
   Nome;Código interno;Código de barras;Preço regular;Promocao;Data termino promocao;estoque;ativo
   ```

4. Run the script:
   ```bash
   python3 main.py
   ```

5. The script will send authenticated PUT requests to the Instabuy API and print the response for each batch.

## 📝 Notes

- The batch size is set to 50 to avoid `413 Payload Too Large` errors.
- Promo price is only sent if greater than 0.
- Dates are converted to ISO 8601 format (`YYYY-MM-DDTHH:MM:SS`).

## 📧 Author

Developed by Georges do Carmo Pereira – April 2025
