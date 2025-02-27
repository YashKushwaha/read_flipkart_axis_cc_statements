# Credit Card Statement Parser

## Overview
This Python program extracts transaction data from credit card statements (PDF files) and saves the extracted data into a structured Excel (`.xlsx`) file. Currently, the program supports **Flipkart Axis Bank** credit card statements, with plans to expand support for other banks in the future.

## Features
- Reads multiple credit card statement PDFs from a specified folder.
- Extracts transaction details such as **date, description, amount, and type (debit/credit)**.
- Supports **password-protected PDFs** (user provides password at runtime).
- Saves extracted transactions into a **tabular Excel format (`.xlsx`)**.

## Installation
### **1. Clone the Repository**
```bash
git clone https://github.com/YashKushwaha/read_flipkart_axis_cc_statements.git

```

### **2. Create a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

## Usage
### **Run the Script**
```bash
python src\credit_card_data_extraction.py
```

### **Inputs Required**
1. **Folder Location:** The directory containing the credit card statement PDFs.
2. **PDF Password:**
   - Option 1: First 4 letters of your name (in capital) + Date of Birth (DDMM)
   - Option 2: First 4 letters of your name (in capital) + Last 4 digits of your credit card

### **Output**
- An Excel file (`axis_flikpart_cc_transactions.xlsx`) containing extracted transaction details.

## File Structure
```
credit-card-parser/
│── src/
│   ├── credit_card_data_extraction.py   # Main script
│   ├── utils.py                         # Helper functions
│── sample_statements/                   # Sample credit card statements (if applicable)
│── requirements.txt                      # Dependencies
│── README.md                             # Project documentation
```


## Dependencies
- `pdfplumber` (for extracting text from PDFs)
- `pandas` (for data handling and exporting to Excel)
- `openpyxl` (for writing Excel files)

## Roadmap
- ✅ Support for Flipkart Axis Bank statements
- 🔜 Build a GUI for easier usage
- 🔜 Export to CSV/JSON formats

## Contributing
Feel free to open an issue or submit a pull request if you'd like to contribute!

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author
[Yash Kushwaha](https://github.com/YashKushwaha)

