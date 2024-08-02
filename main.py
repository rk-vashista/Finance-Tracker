import pandas as pd
import csv
from datetime import datetime
import os
import matplotlib.pyplot as plt
from data_entry import get_date, get_amount, get_category, get_description

class CSV:
    CSV_FILE = os.path.join(os.path.dirname(__file__), 'finance_data.csv')
    COLUMNS = ['Date', 'Amount', 'Category', 'Description']

    @classmethod
    def initialize(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
    
    @classmethod
    def add_data(cls, date, amount, cattegory, description):
        new_entry ={
            'Date': date,
            'Amount': amount,
            'Category': cattegory,
            'Description': description
        }

        with open(cls.CSV_FILE, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print('Data added successfully')

    @classmethod
    def get_transtactions(cls , start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

        start_date = datetime.strptime(start_date, '%d-%m-%Y')
        end_date = datetime.strptime(end_date, '%d-%m-%Y')

        mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print('No data available for the selected date range')
        else:
            print(f'Transactions from {start_date.strftime("%d-%m-%Y")} to {end_date.strftime("%d-%m-%Y")}')
            print(filtered_df.to_string(index=False, formatters={'Date': lambda x: x.strftime('%d-%m-%Y')}))

            total_income = filtered_df[filtered_df['Category'] == 'Income']['Amount'].sum()
            total_expense = filtered_df[filtered_df['Category'] == 'Expense']['Amount'].sum()
            print('\n Summary')
            print(f'Total Income: {total_income}')
            print(f'Total Expense: {total_expense}')
            print(f'Net Income: {total_income - total_expense}')
        return filtered_df

def add():
    CSV.initialize()
    date = get_date('Enter the date (DD-MM-YYYY): or press Enter for today\'s date: ', allow_default=True)
    amount = get_amount('Enter the amount: ')
    category = get_category('Enter the category: ')
    description = get_description('Enter a description: ')
    CSV.add_data(date, amount, category, description)

def plot(df):
    df.set_index('Date', inplace=True)

    income = df[df['Category'] == 'Income'].resample('D').sum().reindex(df.index, fill_value=0)
    expense = df[df['Category'] == 'Expense'].resample('D').sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10, 6))
    plt.plot(income['Amount'], label='Income')
    plt.plot(expense['Amount'], label='Expense')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Income vs Expense')
    plt.legend()
    plt.grid()
    plt.show()

def main():
    while True:
        print('\n1. Add New Transaction')
        print('2. View transactions')
        print('3. Exit')
        choice = input('Enter your choice (1-3): ')

        if choice == '1':
            add()
        elif choice == '2':
            start_date = get_date('Enter the start date (DD-MM-YYYY): ')
            end_date = get_date('Enter the end date (DD-MM-YYYY): ')
            df= CSV.get_transtactions(start_date, end_date)
            if input('Do you want to plot the data? (y/n): ').lower() == 'y':
                plot(df)
        elif choice == '3':
            print('Exiting....')
            break
        else:
            print('Invalid choice. Please enter a valid choice')

if __name__ == '__main__':
    main()