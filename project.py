import json
import os
from datetime import datetime

EXPENSE_FILE = "expenses.json"

def load_expenses():
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, 'r') as file:
            return json.load(file)
    return []

def save_expenses(expenses):
    with open(EXPENSE_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)

def add_expense(expenses):
    print("\nAdd New Expense")
    print("----------------")
    
    while True:
        try:
            amount = float(input("Enter amount spent: $"))
            if amount <= 0:
                print("Amount must be positive. Please try again.")
                continue
            break
        except:
            print("Invalid amount. Please enter a number.")
    
    category = input("Enter category (e.g., Food, Transport, Entertainment): ").strip().title()
    if not category:
        category = "Uncategorized"
    
    date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
    if date_input:
        try:
            date = datetime.strptime(date_input, "%Y-%m-%d").strftime("%Y-%m-%d")
        except:
            print("Invalid date format. Using today's date.")
            date = datetime.now().strftime("%Y-%m-%d")
    else:
        date = datetime.now().strftime("%Y-%m-%d")
    
    expenses.append({
        "amount": amount,
        "category": category,
        "date": date
    })
    
    save_expenses(expenses)
    print("\nExpense added successfully!")

def view_summary(expenses):
    if not expenses:
        print("\nNo expenses to display.")
        return
    
    print("\nExpense Summary")
    print("--------------")
    
    while True:
        print("\n1. View by category")
        print("2. View total spending")
        print("3. View spending over time")
        print("4. View all expenses")
        print("5. Back to main menu")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            categories = {expense['category'] for expense in expenses}
            print("\nCategories:", ", ".join(categories))
            
            category = input("Enter category to view total: ").strip().title()
            category_total = sum(exp['amount'] for exp in expenses if exp['category'] == category)
            
            if category_total > 0:
                print(f"\nTotal spending on {category}: ${category_total:.2f}")
                print(f"Number of transactions: {len([exp for exp in expenses if exp['category'] == category])}")
            else:
                print(f"\nNo expenses found for category: {category}")
                
        elif choice == '2':
            total = sum(expense['amount'] for expense in expenses)
            print(f"\nTotal spending: ${total:.2f}")
            print(f"Number of transactions: {len(expenses)}")
            
        elif choice == '3':
            print("\nSpending Over Time")
            print("-----------------")
            print("1. Daily summary")
            print("2. Monthly summary")
            print("3. Back")
            
            time_choice = input("\nEnter your choice (1-3): ")
            
            if time_choice == '1':
                daily = {}
                for exp in expenses:
                    date = exp['date']
                    daily[date] = daily.get(date, 0) + exp['amount']
                
                print("\nDaily Spending Summary")
                for date, total in sorted(daily.items()):
                    print(f"{date}: ${total:.2f}")
                    
            elif time_choice == '2':
                monthly = {}
                for exp in expenses:
                    year_month = "-".join(exp['date'].split("-")[:2])
                    monthly[year_month] = monthly.get(year_month, 0) + exp['amount']
                
                print("\nMonthly Spending Summary")
                for month, total in sorted(monthly.items()):
                    print(f"{month}: ${total:.2f}")
                    
        elif choice == '4':
            print("\nAll Expenses")
            print("------------")
            for i, exp in enumerate(expenses, 1):
                print(f"{i}. {exp['date']} - {exp['category']}: ${exp['amount']:.2f}")
                
        elif choice == '5':
            break
            
        else:
            print("Invalid choice. Please try again.")

def edit_expense(expenses):
    if not expenses:
        print("\nNo expenses to edit.")
        return
    
    print("\nEdit Expense")
    print("------------")
    for i, exp in enumerate(expenses, 1):
        print(f"{i}. {exp['date']} - {exp['category']}: ${exp['amount']:.2f}")
    
    try:
        choice = int(input("\nEnter the number of the expense to edit: ")) - 1
        if 0 <= choice < len(expenses):
            expense = expenses[choice]
            print(f"\nEditing expense: {expense['date']} - {expense['category']}: ${expense['amount']:.2f}")
            
            new_amount = input(f"Enter new amount (current: {expense['amount']}) or press Enter to keep: ")
            if new_amount:
                try:
                    expense['amount'] = float(new_amount)
                except:
                    print("Invalid amount. Keeping original value.")
            
            new_category = input(f"Enter new category (current: {expense['category']}) or press Enter to keep: ").strip().title()
            if new_category:
                expense['category'] = new_category
            
            new_date = input(f"Enter new date (YYYY-MM-DD) (current: {expense['date']}) or press Enter to keep: ").strip()
            if new_date:
                try:
                    expense['date'] = datetime.strptime(new_date, "%Y-%m-%d").strftime("%Y-%m-%d")
                except:
                    print("Invalid date format. Keeping original date.")
            
            save_expenses(expenses)
            print("\nExpense updated successfully!")
        else:
            print("Invalid selection.")
    except:
        print("Please enter a valid number.")

def delete_expense(expenses):
    if not expenses:
        print("\nNo expenses to delete.")
        return
    
    print("\nDelete Expense")
    print("-------------")
    for i, exp in enumerate(expenses, 1):
        print(f"{i}. {exp['date']} - {exp['category']}: ${exp['amount']:.2f}")
    
    try:
        choice = int(input("\nEnter the number of the expense to delete: ")) - 1
        if 0 <= choice < len(expenses):
            deleted = expenses.pop(choice)
            save_expenses(expenses)
            print(f"\nDeleted expense: {deleted['date']} - {deleted['category']}: ${deleted['amount']:.2f}")
        else:
            print("Invalid selection.")
    except:
        print("Please enter a valid number.")

def main():
    print("Welcome to Personal Expense Tracker!")
    print("-----------------------------------")
    
    expenses = load_expenses()
    
    while True:
        print("\nMain Menu")
        print("---------")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            view_summary(expenses)
        elif choice == '3':
            edit_expense(expenses)
        elif choice == '4':
            delete_expense(expenses)
        elif choice == '5':
            print("\nThank you for using Personal Expense Tracker!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()