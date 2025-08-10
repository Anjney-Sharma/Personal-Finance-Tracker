import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount,get_category,get_date,get_description
import matplotlib.pyplot as plt

class CSV:          
    CSV_file = "finance_data.csv"       #to create a file name this in same directory in which entries will be updated
    COLUMNS = ["date","amount","category","description"]
    FORMAT = "%d-%m-%Y"

    @classmethod                        # have access to class but not to instance
    def initialize_csv(cls):             
        try:                            #reading the existing csv file
            pd.read_csv(cls.CSV_file)
        except FileNotFoundError:       #creating a csv if not exists
            df = pd.DataFrame(columns= cls.COLUMNS)
            df.to_csv(cls.CSV_file,index=False)

    @classmethod
    def add_entry(cls,date,amount,category,description):    #to add entries in csv file we are reading
        new_entry = {                   # creating a dictionary for each entry
            "date" : date,
            "amount" : amount,
            "category" : category,
            "description" : description
        }
        with open(cls.CSV_file, "a",newline="") as csvfile:   
            writer = csv.DictWriter(csvfile,fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("\nEntry added sucessfully")


    @classmethod
    def get_transactions(cls,start_date,end_date):
        df = pd.read_csv(cls.CSV_file)
        df["date"] = pd.to_datetime(df["date"],format=CSV.FORMAT)
        start_date = datetime.strptime(start_date,CSV.FORMAT)
        end_date = datetime.strptime(end_date,CSV.FORMAT)

        mask = (df["date"] >= start_date) & (end_date >= df["date"])
        filtered_df = df.loc[mask]

        if(filtered_df.empty):
            print("No transactions found in given date range")
        else:
            print(f"\nTransactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)} ")
            print(filtered_df.to_string(
                index=False,formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
            ))
        
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()  
            print("\nSummary: ")
            print(f"Total Income : ₹{total_income:.2f}")
            print(f"Total Expense : ₹{total_expense:.2f}")  
            print(f"Net Savings : ₹{(total_income - total_expense):.2f}") 
        return filtered_df
    
def add():
    CSV.initialize_csv()
    date = get_date("Enter date of transaction (dd-mm-yyyy) or press enter for today's date : ",allow_default=True)    
    # must remember : if "allow_default=True" this is not done the funtion will not work if a input not given i.e no default case where if nothing entered run this will work .
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date,amount,category,description)

def plot_transactions(df):
    df.set_index("date", inplace=True)      #(inplace=True) make changes to original df

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")      #("D"=> Daily Frequency) (Resampling Income data in df on daily basis(i.e providing row for every single day{basically filling every day})
        .sum()              #Aggregating all rows having same date and Adding their amounts together 
        .reindex(df.index, fill_value=0)    # CONFORMS df to "date" index.  USE: to reorder, add->0 in empty rows(fill_value=0 [if this is not done it'll fill with NaN])
    )
               
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")      
        .sum()              
        .reindex(df.index, fill_value=0)  
    )

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index , income_df["amount"], label="Income", color="g") 
    plt.plot(expense_df.index , expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses ")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice=="1":
            add()
        elif choice=="2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to plot?  (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice=="3":
            print("Exiting....")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")

if __name__ == "__main__":          # This line is used to control the execution of code when a file is run directly, versus when it is imported as a module into another script.
    main()



# Chat suggetion to upgarde it :
# ⚠️ But Here’s the Risk
# You also have this old transaction :  20-07-2023,124.0,Expense,Groceries
# If you ever choose a date range like: Start date: 01-07-2023 , End date: 31-07-2023
# You'll only have one transaction — and since your df.index has only that one date (2023-07-20), your .reindex(df.index) will create a plot with just one dot (instead of filling all July 2023 dates).

# So the plot will fail to show a proper timeline, especially when:
# You're visualizing date ranges with few transactions, or you want zero values to appear for inactive days.

# ✅ Recommendation (Best Practice)
# To make your plot robust and always accurate, replace: .reindex(df.index, fill_value=0) [#line 76]

# with: .reindex(pd.date_range(df.index.min(), df.index.max(), freq="D"), fill_value=0)

# That ensures:
# The plot has continuous dates, even if no transactions happened.
# Income and Expense lines will stretch across the full selected period.
# You avoid future bugs when working with sparse data.
