
import yfinance as yf
import json
import os

FILE = "portfolio.json"

# Load portfolio data
def load_portfolio():
    if os.path.exists(FILE):
        with open(FILE, "r") as file:
            return json.load(file)
    return {}


# Save portfolio data
def save_portfolio(portfolio):
    with open(FILE, "w") as file:
        json.dump(portfolio, file, indent=4)


# Add stock
def add_stock():
    portfolio = load_portfolio()

    ticker = input("Enter stock symbol (e.g. RELIANCE.NS): ").upper()

    try:
        quantity = float(input("Enter quantity: "))
        buy_price = float(input("Enter buying price: "))

        if quantity <= 0 or buy_price <= 0:
            print("Quantity and price must be positive!")
            return

        if ticker in portfolio:
            old_qty = portfolio[ticker]["quantity"]
            old_price = portfolio[ticker]["buy_price"]

            total_qty = old_qty + quantity

            avg_price = (
                (old_qty * old_price) +
                (quantity * buy_price)
            ) / total_qty

            portfolio[ticker]["quantity"] = total_qty
            portfolio[ticker]["buy_price"] = avg_price

        else:
            portfolio[ticker] = {
                "quantity": quantity,
                "buy_price": buy_price
            }

        save_portfolio(portfolio)
        print("Stock added successfully!")

    except ValueError:
        print("Please enter valid numbers!")


# View portfolio
def view_portfolio():
    portfolio = load_portfolio()

    if not portfolio:
        print("Your portfolio is empty!")
        return

    total_investment = 0
    total_current_value = 0
    unavailable = False

    print("\n========== STOCK PORTFOLIO ==========")

    for ticker, data in portfolio.items():

        quantity = data["quantity"]
        buy_price = data["buy_price"]

        investment = quantity * buy_price
        total_investment += investment

        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="5d")

            if history.empty:
                raise ValueError("Price unavailable")

            current_price = float(
                history["Close"].dropna().iloc[-1]
            )

            current_value = quantity * current_price
            profit_loss = current_value - investment

            total_current_value += current_value

            print("\nStock:", ticker)
            print("Quantity:", quantity)
            print("Buying Price:", round(buy_price, 2))
            print("Current Price:", round(current_price, 2))
            print("Investment:", round(investment, 2))
            print("Current Value:", round(current_value, 2))
            print("Profit/Loss:", round(profit_loss, 2))

        except Exception:
            unavailable = True
            print("\nStock:", ticker)
            print("Price unavailable")
            print("Investment:", round(investment, 2))

    print("\n========== TOTAL SUMMARY ==========")
    print("Total Investment:", round(total_investment, 2))
    print("Current Value (available stocks):",
          round(total_current_value, 2))

    if not unavailable:
        total_profit = total_current_value - total_investment
        print("Total Profit/Loss:", round(total_profit, 2))
    else:
        print("Total Profit/Loss: Incomplete (some prices unavailable)")


# Main menu
while True:

    print("\n===== STOCK PORTFOLIO TRACKER =====")
    print("1. Add Stock")
    print("2. View Portfolio")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_stock()

    elif choice == "2":
        view_portfolio()

    elif choice == "3":
        print("Thank you for using Stock Tracker!")
        break

    else:
        print("Invalid choice! Try again.")
