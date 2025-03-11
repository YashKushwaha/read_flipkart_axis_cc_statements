import pdfplumber
import datetime
import os, sys
from pdfminer.pdfdocument import PDFPasswordIncorrect

def is_int(int_str):
    try:
        return int(int_str)
    except:
        return False

def read_encrypted_pdf(pdf_file, password):
    with pdfplumber.open(pdf_file, password = password) as pdf:
        data = dict()
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            data[page_num] = text
    return data

def is_date(date_string, date_format = "%d/%m/%Y"):
    try:
        valid_date = datetime.datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False

def extract_all_transactions(page_contenct_dict):
    transaction_list = []
    for page, content in  page_contenct_dict.items():
        for i in content.split('\n'):
            if is_date(i.split()[0]):
                transaction_list.append(i)
            else:
                try:
                    if (len(i) ==10) & is_int(i[6:10]) & is_int(i[:2]):
                        #print('Looks like date -> ', i)      
                        pass
                except Exception as e:
                    pass
                    #print(e, i)
    return transaction_list    

def extract_table(pdf_file, password):
    with pdfplumber.open(pdf_file, password = password) as pdf:
        data = dict()
        for page_num, page in enumerate(pdf.pages):
            # Extract text from each page
            tables = page.extract_tables({
                    'vertical_strategy': 'lines',  # Try 'lines' or 'text'
                    'horizontal_strategy': 'lines',  # 'lines', 'text', or 'explicit'
                    'intersection_tolerance': 5,  # Adjust as needed to detect lines better
                })
            data[page_num] = tables
    return data

def clean_transaction_list(all_transactions):
    cleaned_transactions = []
    for i in all_transactions:
        i = i.replace(' Cr', 'Cr').replace(' Dr', 'Dr')
        entries = i.split()
        date = entries.pop(0)        
        debit = None
        credit = None
    
        for _ in range(2):
            last_entry = entries.pop()
            if last_entry.endswith('Cr'):
                credit = last_entry
            else:
                debit = last_entry
        others = entries
    
        record = dict(date=date, debit=debit, credit=credit, others=others, complete_entry = i)
        cleaned_transactions.append(record)
    return cleaned_transactions
    
def extract_transactions_from_pdfs(cc_statement_dir, password):
    cc_statements = [i for i in os.listdir(cc_statement_dir) if i.endswith('.pdf')]
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
        
    return all_transactions