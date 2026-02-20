# ==========================
# STOCK PORTFOLIO TRACKER 
# ==========================
 
# csv module allows us to save and read files on excel
import csv
 
# Dictionary storing stock prices
# Each stock has:
#   - today's price
#   - yesterday's closing price

STOCKS = {
    "AAPL": {"price": 182, "yesterday": 178},
    "TSLA": {"price": 255, "yesterday": 248},
    "GOOG": {"price": 142, "yesterday": 141},
    "MSFT": {"price": 335, "yesterday": 330},
    "NVDA": {"price": 720, "yesterday": 700},
    "AMZN": {"price": 170, "yesterday": 168},
    "META": {"price": 495, "yesterday": 480}
}
 
# Displays all stocks and shows whether
# they are gaining or losing today
def show_market():
 
    print("\n📈 MARKET OVERVIEW")
    print("--------------------------------")
 
    # Loop through each stock in dictionary
    for stock, data in STOCKS.items():
 
        # Extract today's and yesterday's prices
        today = data["price"]
        yesterday = data["yesterday"]
 
        # Calculate daily price change
        change = today - yesterday
 
        # Decide status icon
        status = "📈 Leading Today" if change > 0 else "📉 Down"
 
        # Display formatted result
        print(
            f"{stock}: Today ${today} | "
            f"Yesterday ${yesterday} | "
            f"Change {change:+} | {status}"
        )
 
# Allows user to buy stocks and build portfolio
def create_portfolio():
 
    portfolio = []           # list to store purchases
    total_investment = 0     # tracks total money spent
 
    print("\nEnter stocks you want to buy.")
    print("Type DONE when finished.")
 
    # Infinite loop until user types DONE
    while True:
 
        stock = input("\nEnter stock: ").upper()
 
        # Exit condition
        if stock == "DONE":
            break
 
        # Validate stock symbol
        if stock not in STOCKS:
            print("❌ Invalid stock.")
            continue
 
        # Ask how many shares user buys
        quantity = int(input("Quantity: "))
 
        # Get price data
        today = STOCKS[stock]["price"]
        yesterday = STOCKS[stock]["yesterday"]
 
        # Calculate investment value
        value = today * quantity
 
        # Calculate daily profit/loss
        profit_loss = (today - yesterday) * quantity
 
        # Add to running total
        total_investment += value
 
        # Store purchase info as a row
        portfolio.append([
            stock,
            quantity,
            today,
            yesterday,
            value,
            profit_loss
        ])
 
    # Save portfolio to CSV file
    save_csv(portfolio, total_investment)
 
    print(f"\n✅ Portfolio saved.")
    print(f"Total Investment: ${total_investment}")
 
 
# ------------------------------------------
# SAVE DATA TO CSV FILE
# ------------------------------------------
# Writes portfolio data into portfolio.csv
def save_csv(data, total):
 
    # "w" mode = overwrite file each time
    # newline="" prevents blank rows
    with open("portfolio.csv", "w", newline="") as file:
 
        writer = csv.writer(file)
 
        # Write column headers
        writer.writerow([
            "Stock",
            "Quantity",
            "Today Price",
            "Yesterday Close",
            "Value",
            "Daily Profit/Loss"
        ])
 
        # Write all portfolio rows
        writer.writerows(data)
 
        # Empty line for readability
        writer.writerow([])
 
        # Write total investment summary
        writer.writerow(["TOTAL INVESTMENT", "", "", "", total, ""])
 
# ------------------------------------------
# VIEW USER PORTFOLIO
# ------------------------------------------
# Reads saved CSV and displays account summary
def view_portfolio():
 
    try:
        # Open saved portfolio file
        with open("portfolio.csv", "r") as file:
 
            reader = csv.reader(file)
 
            print("\n📊 USER PORTFOLIO")
            print("------------------------------------------------")
 
            total_profit = 0
 
            # Read header row first
            header = next(reader)
            print(" | ".join(header))
 
            # Loop through remaining rows
            for row in reader:
 
                # Skip empty lines
                if not row:
                    continue
 
                # Stop when TOTAL row reached
                if row[0] == "TOTAL INVESTMENT":
                    print("\n" + " | ".join(row))
                    break
 
                # Display portfolio row
                print(" | ".join(row))
 
                # Add profit/loss values
                total_profit += float(row[5])
 
            print("\n--------------------------------")
 
            # Show overall result
            status = "📈 PROFIT" if total_profit > 0 else "📉 LOSS"
 
            print(f"Daily Portfolio Result: {total_profit:+.2f} ({status})")
 
    # Handle case where file doesn't exist
    except FileNotFoundError:
        print("\n⚠ No portfolio found. Create one first.")
 
# Controls entire program navigation
def menu():
 
    while True:
 
        print("\n===== 📈 STOCK TRACKER MENU =====")
        print("1. View Market Overview")
        print("2. Create Portfolio")
        print("3. Exit")
        print("4. View My Account / Portfolio")
 
        choice = input("Select option: ")
 
        # Call functions based on user choice
        if choice == "1":
            show_market()
 
        elif choice == "2":
            create_portfolio()
 
        elif choice == "3":
            print("👋 Exiting program.")
            break
 
        elif choice == "4":
            view_portfolio()
 
        else:
            print("❌ Invalid choice.")
 
# Runs menu when script is executed
menu()