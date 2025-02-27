import os
import sys
import pandas as pd
from pdfminer.pdfdocument import PDFPasswordIncorrect

from utils import *

DEBUG_MODE = False
if __name__ == '__main__':
    prompt = (
            "Enter the folder path where your Flipkart Axis Bank credit card statements (PDFs) are stored.\n"
            "The program will scan this location and process all PDF files.\n"
            "Press Enter without typing anything to exit.\n\n"
            "Folder Path: "
        )
    cc_statement_dir = input(prompt)
    if not cc_statement_dir:
        sys.exit("⚠️ No folder path provided. Exiting the program.")
    
    if not os.path.isdir(cc_statement_dir):
        sys.exit(f"❌ The provided path does not exist or is not a directory: {cc_statement_dir}")

    cc_statements = [i for i in os.listdir(cc_statement_dir) if i.endswith('.pdf')]
    prompt = (
        "🔑 Please enter the password to open your Flipkart Axis Bank credit card statements.\n"
        "The password format is one of the following:\n"
        "   1️⃣ First 4 letters of your name (in CAPITAL) + Date of Birth (DDMM)\n"
        "   2️⃣ First 4 letters of your name (in CAPITAL) + Last 4 digits of your credit card\n"
        "📌 Example: If your name is *Rahul Kumar* and your DOB is *15th June*, the password could be *RAHU1506*.\n"
        "⚠️ If you enter an incorrect password, the program may not be able to read the statements.\n"
    )

    password = input(prompt).strip()
    
    if not password:
        sys.exit("❌ No password entered. Exiting the program.")
    
    all_transactions = []
    for file in cc_statements:
        print(f'Reading file -> {file}')
        pdf_file = os.path.join(cc_statement_dir, file)
        try:
            data = read_encrypted_pdf(pdf_file, password)
            transactions = extract_all_transactions(data)
            all_transactions+=transactions    
        except PDFPasswordIncorrect:
            print("Error: The PDF is password-protected. Please provide the correct password.")
        except Exception as e:
            print('Error while reading the PDF -> ', e)

    if not all_transactions:
        sys.exit("❌ No transactions to process. Exiting the program.")
    
    cleaned_all_transactions = clean_transaction_list(all_transactions)
    transactions_df = pd.DataFrame(cleaned_all_transactions)
    transactions_df['credit'] = transactions_df['credit'].apply(lambda x: x.replace('Cr', '').replace(',', '')).apply(float)
    transactions_df['debit'] = transactions_df['debit'].apply(lambda x: x.replace('Dr', '').replace(',', '')).apply(float)
    transactions_df['date'] = pd.to_datetime(transactions_df['date'], format = "%d/%m/%Y")
    transactions_df = transactions_df.sort_values(by='date', ascending=False)
    del transactions_df['others']
    col_order = ['date', 'complete_entry', 'debit', 'credit']
    current_folder = os.getcwd()
    output_location = input(f'Enter location where output will be saved. Press Enter to save at --> {current_folder}\n')
    if output_location == '':
        output_location = current_folder
    save_name = os.path.join(output_location, 'axis_flikpart_cc_transactions.xlsx')
    
    transactions_df[col_order].to_excel(save_name, index=False)
    