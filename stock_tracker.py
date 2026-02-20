# ==========================
# STOCK PORTFOLIO TRACKER 
# ==========================

import csv
import os  # to check if the user is returning (file exists)

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

# ------------------------------
# UTILITIES: load & save
# ------------------------------
def portfolio_exists():
    """Returns True if a previous portfolio CSV is present."""
    return os.path.exists("portfolio.csv")

def load_portfolio():
    """
    Loads existing portfolio.csv (if present) and returns a dict:
    holdings = { 'AAPL': qty, ... }
    """
    holdings = {}
    if not portfolio_exists():
        return holdings

    with open("portfolio.csv", "r") as file:
        reader = csv.reader(file)
        header = next(reader, None)  # skip header
        for row in reader:
            if not row:
                continue
            if row[0] == "TOTAL INVESTMENT":
                break
            # Expected row = [Stock, Quantity, Today, Yesterday, Value, P/L]
            symbol = row[0].strip()
            try:
                qty = int(row[1])
            except ValueError:
                qty = 0
            holdings[symbol] = holdings.get(symbol, 0) + qty
    return holdings

def save_csv_from_holdings(holdings):
    """
    Takes holdings dict {symbol: qty} and writes a fresh portfolio.csv
    with calculated values based on current STOCKS.
    """
    rows = []
    total_investment = 0

    for symbol, qty in holdings.items():
        if symbol not in STOCKS:
            # Skip symbols that are no longer defined in STOCKS
            continue
        today = STOCKS[symbol]["price"]
        yesterday = STOCKS[symbol]["yesterday"]
        value = today * qty
        profit_loss = (today - yesterday) * qty
        total_investment += value

        rows.append([symbol, qty, today, yesterday, value, profit_loss])

    save_csv(rows, total_investment)
    return total_investment

# ------------------------------
# MARKET OVERVIEW
# ------------------------------
def show_market():
    print("\n📈 MARKET OVERVIEW")
    print("--------------------------------")
    for stock, data in STOCKS.items():
        today = data["price"]
        yesterday = data["yesterday"]
        change = today - yesterday
        status = "📈 Leading Today" if change > 0 else "📉 Down"
        print(
            f"{stock}: Today ${today} | "
            f"Yesterday ${yesterday} | "
            f"Change {change:+} | {status}"
        )

# ------------------------------
# CREATE / UPDATE PORTFOLIO
# ------------------------------
def create_or_update_portfolio():
    """
    If a portfolio exists, we load it and let the user add more.
    Otherwise, we start fresh.
    """
    # Load existing holdings if any
    holdings = load_portfolio()
    returning_user = len(holdings) > 0

    if returning_user:
        print("\n👋 Welcome back! We'll update your existing portfolio.")
        print("Your current holdings:")
        for sym, qty in holdings.items():
            print(f" - {sym}: {qty} shares")
    else:
        print("\nLet's build your portfolio.")
    
    print("\nEnter stocks you want to buy (new purchases only).")
    print("Type DONE when finished.")

    while True:
        stock = input("\nEnter stock: ").upper().strip()

        if stock == "DONE":
            break

        if stock not in STOCKS:
            print("❌ Invalid stock.")
            continue

        try:
            quantity = int(input("Quantity: "))
            if quantity <= 0:
                print("❌ Quantity must be a positive integer.")
                continue
        except ValueError:
            print("❌ Please enter a valid number.")
            continue

        # Update holdings (additive)
        holdings[stock] = holdings.get(stock, 0) + quantity
        print(f"✅ Added {quantity} share(s) of {stock}. New total: {holdings[stock]}")

    # Write updated portfolio
    total_investment = save_csv_from_holdings(holdings)

    if returning_user:
        print(f"\n✅ Portfolio updated.")
    else:
        print(f"\n✅ Portfolio created.")

    print(f"Total Investment: ${total_investment}")

# ------------------------------
# SAVE DATA TO CSV FILE
# ------------------------------
def save_csv(data, total):
    with open("portfolio.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Stock",
            "Quantity",
            "Today Price",
            "Yesterday Close",
            "Value",
            "Daily Profit/Loss"
        ])
        writer.writerows(data)
        writer.writerow([])
        writer.writerow(["TOTAL INVESTMENT", "", "", "", total, ""])

# ------------------------------
# VIEW USER PORTFOLIO
# ------------------------------
def view_portfolio():
    try:
        with open("portfolio.csv", "r") as file:
            reader = csv.reader(file)

            print("\n📊 USER PORTFOLIO")
            print("------------------------------------------------")

            total_profit = 0

            header = next(reader)
            print(" | ".join(header))

            for row in reader:
                if not row:
                    continue
                if row[0] == "TOTAL INVESTMENT":
                    print("\n" + " | ".join(row))
                    break

                print(" | ".join(row))
                try:
                    total_profit += float(row[5])
                except (IndexError, ValueError):
                    pass

            print("\n--------------------------------")
            status = "📈 PROFIT" if total_profit > 0 else "📉 LOSS"
            print(f"Daily Portfolio Result: {total_profit:+.2f} ({status})")

    except FileNotFoundError:
        print("\n⚠ No portfolio found. Create one first.")

# ------------------------------
# MENU
# ------------------------------
def menu():
    while True:
        returning_text = " (Detected previous portfolio)" if portfolio_exists() else ""
        print("\n===== 📈 STOCK TRACKER MENU =====")
        print("1. View Market Overview")
        print("2. Create/Update Portfolio" + returning_text)
        print("3. Exit")
        print("4. View My Account / Portfolio")

        choice = input("Select option: ")

        if choice == "1":
            show_market()
        elif choice == "2":
            create_or_update_portfolio()
        elif choice == "3":
            print("👋 Exiting program.")
            break
        elif choice == "4":
            view_portfolio()
        else:
            print("❌ Invalid choice.")

# Runs menu when script is executed
menu()
