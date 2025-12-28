## Financial Analyzer

A Python app that analyzes companies using Yahoo Finance data
and applies Warren Buffett–style financial rules.

### Modules
This app consists in 3 main modules each analyzing one aspect of a company's finances:
- **Income Statement**: how much money the company earned during a set period of time
  - Usually generated every 3 months and one for the whole year

- **Balance Sheet**: how much money the company has in the bank and how much it owes
  - Subtract the money owed from the money in the bank and we get the net worth of the company
  - Companies can create a balance sheet for any given day of the year (only worth/valid for that particular day obviously)
  - Usually generated every 3 months and one for the whole year
  - Some of the entries here such as the amount of cash the company has or the amount of long-term debt it carries are clear indicators of the presence of a durable competitive advantage.

- **Cash Flow Statement**: tracks the cash that flows in and out of the business
  - Good for seeing how much money the company is spending on capital improvements
  - Also tracks bond and stock sales and repurchase

### How to run the project
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python3 app.py`
