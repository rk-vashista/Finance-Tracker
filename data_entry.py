from datetime import datetime

CATEGORY = {
    'I': 'Income',
    'E': 'Expense'
}

def get_date(prompt, allow_default=True):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime('%d-%m-%Y')
    else:
        try:
            valid_date = datetime.strptime(date_str, '%d-%m-%Y')
            return valid_date.strftime('%d-%m-%Y')
        except ValueError:
            print('Invalid date format. Please enter a date in the format DD-MM-YYYY')
            return get_date(prompt, allow_default)

def get_amount(prompt):
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError('Amount must be greater than 0')
        return amount
    except ValueError as e:
        print(e)
        return get_amount()
        

def get_category(prompt):
    category = input("Enter the category: ('I' for Income, 'E' for Expense) ").upper()
    if category in CATEGORY:
        return CATEGORY[category]
    else:
        print('Invalid category. Please enter "I" for Income or "E" for Expense')
        return get_category()

def get_description(prompt):
    return input("Enter a description: ")