## Financial Analyzer

A Python app that analyzes companies using Yahoo Finance data
and applies Warren Buffett–style financial rules.

### Prerequisites
Before running the project, make sure you have:
- [Python 3+](https://www.python.org/downloads/)
- pip (python package manager)

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
1. Create a virtual environment
```
python3 -m venv venv
```

2. Activate the virtual environment
```
source venv/bin/activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Run the analyzer
```
python3 app.py
```

### Output & Reporting

#### Console Output
- Results are printed directly to the terminal
- Each rule includes:
  - Rule title
  - Description
  - Pass / Fail / Excellent / Great status
- Actual Yahoo Finance values used in the calculation

### Markdown Report
In addition to console output, the app **automatically generates a Markdown report after execution.**

The Markdown report includes:
- One section per company
- Separate sections for Income, Balance Sheet, and Cash Flow
- A table per section with:
  - Rule name
  - Rule description
  - Evaluation result (with visual status indicators)
  - Exact financial values used

The file is generated in the project root with a timestamped name, for example:
```
analysis_2025-01-04_21-35.md
```

### Notes
- The app uses yfinance under the hood, so available data depends on Yahoo Finance coverage.
- If certain data points are missing, rules may be marked as `N/A` and clearly documented as such.
- Company categories (consumer, banking, tech, etc.) can be customized in app.py to apply category-specific rules.