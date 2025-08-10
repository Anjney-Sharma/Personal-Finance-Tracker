from datetime import datetime

date_Format = "%d-%m-%Y"
CATEGORIES = {"I":"Income","E":"Expense"}

def get_date(prompt_str,allow_default = False):
    date_str = input(prompt_str)
    if (allow_default and not date_str):
        return datetime.today().strftime(date_Format)
    
    try:
        valid_date = datetime.strptime(date_str,date_Format)      #Converts any invlid format into correct one
        return valid_date.strftime(date_Format)                  #Returns that after converting into string
    except ValueError:
        print("Invalid date format \nplease enter in dd-mm-yyyy format")
        return get_date(prompt_str,allow_default)        

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if(amount<=0):
            raise ValueError("Amount must be non-zero , non-negative.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter a category ('I' for Income or 'E' for Expense) : ").upper()
    if (category in CATEGORIES):
        return CATEGORIES[category]

    print("Invalid category. Please enter 'I' for Income or 'E' for Expense. ")
    return get_category()

def get_description():
    return input("Enter a description (*optional) : ")