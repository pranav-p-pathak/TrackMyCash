import sqlite3
import datetime
import matplotlib.pyplot as plt
import csv

def create_table():
    """Creates the expenses table if it doesn't exist."""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            amount REAL,
            category TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def is_valid_date(date_str):
    """Checks if a date string is in YYYY-MM-DD format."""
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def add_expense(date, amount, category, description):
    """Adds an expense entry to the database."""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO expenses (date, amount, category, description) VALUES (?, ?, ?, ?)",
                       (date, amount, category, description))
        conn.commit()
        print("Expense added successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


def view_all_expenses():
    """Displays all expense records."""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    if not expenses:
        print("No expenses found.")
    else:
        for expense in expenses:
            print(expense)
    conn.close()

def filter_expenses(start_date=None, end_date=None, category=None):
    """Filters expenses by date range and/or category."""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    if category:
        query += " AND category = ?"
        params.append(category)

    cursor.execute(query, params)
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def search_expenses(keyword):
    """Searches for expenses by keyword in the description."""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE description LIKE ?", ('%' + keyword + '%',))
    expenses = cursor.fetchall()
    conn.close()
    return expenses


def summarize_expenses(start_date=None, end_date=None):
    """Summarizes expenses for a selected period."""
    expenses = filter_expenses(start_date, end_date)
    total_expenses = sum(expense[2] for expense in expenses)
    print(f"Total expenses: {total_expenses}")
    if len(expenses) > 0:
      dates = sorted([datetime.datetime.strptime(expense[1], "%Y-%m-%d").date() for expense in expenses])
      date_diff = dates[-1] - dates[0]
      average = total_expenses / date_diff.days if date_diff.days > 0 else total_expenses
      print(f"Average daily spending: {average}")
      max_expense = max(expenses, key=lambda x: x[2])
      print(f"Highest expense: {max_expense}")
      min_expense = min(expenses, key=lambda x: x[2])
      print(f"Lowest expense: {min_expense}")


def export_to_csv():
    """Exports all expense data to a CSV file."""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()

    try:
        with open('expenses.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['id', 'date', 'amount', 'category', 'description'])  # Write header
            csv_writer.writerows(expenses)  # Write data rows
        print("Expenses exported to expenses.csv")
    except Exception as e:
        print(f"An error occurred while exporting to CSV: {e}")

      
def visualize_category_distribution(start_date=None, end_date=None):
    """Visualizes category-wise expense distribution using a pie chart."""
    expenses = filter_expenses(start_date, end_date)
    category_totals = {}
    for expense in expenses:
        category = expense[3]
        amount = expense[2]
        category_totals[category] = category_totals.get(category, 0) + amount

    if not category_totals:
        print("No expenses found for the selected period to visualize.")
        return
    
    categories = category_totals.keys()
    amounts = category_totals.values()
    
    try:
      plt.figure(figsize=(8, 8))
      plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
      plt.title('Category-wise Expense Distribution')
      plt.show()
    except Exception as e:
      print(f"An error occurred while creating the pie chart: {e}")


def visualize_monthly_trends(start_date=None, end_date=None):
    """Visualizes monthly expense trends using a line chart."""
    expenses = filter_expenses(start_date, end_date)
    monthly_totals = {}
    for expense in expenses:
        date_obj = datetime.datetime.strptime(expense[1], '%Y-%m-%d')
        month_year = date_obj.strftime('%Y-%m')
        amount = expense[2]
        monthly_totals[month_year] = monthly_totals.get(month_year, 0) + amount

    if not monthly_totals:
        print("No expenses found for the selected period to visualize.")
        return

    sorted_months = sorted(monthly_totals.keys())
    amounts = [monthly_totals[month] for month in sorted_months]

    try:
        plt.figure(figsize=(10, 6))
        plt.plot(sorted_months, amounts, marker='o')
        plt.title('Monthly Expense Trends')
        plt.xlabel('Month')
        plt.ylabel('Total Expenses')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"An error occurred while creating the line chart: {e}")


def main():
    create_table()
    add_expense("2023-10-27", 50.0, "Food", "Lunch")    
    add_expense("2023-10-28", 25.0, "Transport", "Bus")    
    add_expense("2023-10-29", 10.0, "Food", "Coffee")    
    add_expense("2023-10-30", 100.0, "Clothes", "Shirt")    
    add_expense("2023-11-15", 75.0, "Food", "Dinner")
    add_expense("2023-11-20", 30.0, "Entertainment", "Movie")
    view_all_expenses()
    
    filtered_expenses = filter_expenses(start_date="2023-10-28", end_date="2023-10-30", category="Food")    
    print("Filtered expenses:", filtered_expenses)

    search_result = search_expenses("Shirt")
    print("Search result:", search_result)
    
    summarize_expenses(start_date="2023-10-28", end_date="2023-10-30")

    visualize_category_distribution(start_date="2023-10-27", end_date="2023-11-20")

    visualize_monthly_trends(start_date="2023-10-27", end_date="2023-11-20")

    export_to_csv()
def main():
    create_table()
    
    while True:
        print("\n===== Personal Expense Tracker =====")
        print("1. Add a new expense")
        print("2. View all expenses")
        print("3. Filter expenses")
        print("4. Search expenses by description")
        print("5. Summarize expenses")
        print("6. Visualize category-wise expense distribution")
        print("7. Visualize monthly expense trends")
        print("8. Export expenses to CSV")
        print("9. Exit")
        
        choice = input("Enter your choice (1-9): ").strip()

        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            if not is_valid_date(date):
                print("Invalid date format.")
                continue
            try:
                amount = float(input("Enter amount: "))
            except ValueError:
                print("Invalid amount.")
                continue
            category = input("Enter category: ")
            description = input("Enter description: ")
            add_expense(date, amount, category, description)

        elif choice == '2':
            view_all_expenses()

        elif choice == '3':
            start_date = input("Enter start date (YYYY-MM-DD) or press Enter to skip: ").strip()
            end_date = input("Enter end date (YYYY-MM-DD) or press Enter to skip: ").strip()
            category = input("Enter category to filter or press Enter to skip: ").strip()
            filtered = filter_expenses(start_date or None, end_date or None, category or None)
            if filtered:
                for f in filtered:
                    print(f)
            else:
                print("No matching records found.")

        elif choice == '4':
            keyword = input("Enter keyword to search in description: ")
            results = search_expenses(keyword)
            if results:
                for r in results:
                    print(r)
            else:
                print("No matching records found.")

        elif choice == '5':
            start_date = input("Enter start date (YYYY-MM-DD) or press Enter to skip: ").strip()
            end_date = input("Enter end date (YYYY-MM-DD) or press Enter to skip: ").strip()
            summarize_expenses(start_date or None, end_date or None)

        elif choice == '6':
            start_date = input("Enter start date (YYYY-MM-DD) or press Enter to skip: ").strip()
            end_date = input("Enter end date (YYYY-MM-DD) or press Enter to skip: ").strip()
            visualize_category_distribution(start_date or None, end_date or None)

        elif choice == '7':
            start_date = input("Enter start date (YYYY-MM-DD) or press Enter to skip: ").strip()
            end_date = input("Enter end date (YYYY-MM-DD) or press Enter to skip: ").strip()
            visualize_monthly_trends(start_date or None, end_date or None)

        elif choice == '8':
            export_to_csv()

        elif choice == '9':
            print("Exiting... Have a great day!")
            break
        else:
            print("Invalid choice. Please select from the menu.")



if __name__ == '__main__':
    main()