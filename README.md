# 💰 Expense Tracker

A simple, terminal-based personal expense tracker built using **Python** and **SQLite**. Log, search, analyze, and visualize your expenses with ease — all from the command line.

## 🔧 Features

- 📌 Add and store expenses with date, category, and description  
- 🔍 Filter and search expenses by date range, category, or keyword  
- 📊 Visualize category-wise spending with pie charts  
- 📈 Track monthly expense trends  
- 📁 Export your data to CSV  
- 📋 View summaries including totals, averages, and extreme spendings  

## 🛠️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
```

### 2. Install Dependencies

Make sure you have Python 3 installed. Then run:

```bash
pip install matplotlib
```

### 3. Run the Tracker

```bash
python expense_tracker.py
```

## 📂 File Structure

```
.
├── expense_tracker.py    # Main script
├── expenses.db           # SQLite database (auto-generated)
├── expenses.csv          # CSV export (auto-generated)
└── README.md             # Project documentation
```

## 🧪 Sample Commands

- Add an expense  
- Filter by date and category  
- Summarize expenses  
- View charts  
- Export all data to CSV

All via an intuitive terminal menu.

## 📈 Visualizations

- Pie Chart of Category Distribution  
- Line Graph of Monthly Spending  

## 📤 Export

Easily export all your data:

```bash
> Export expenses to CSV
```

Generates `expenses.csv` with all records.
