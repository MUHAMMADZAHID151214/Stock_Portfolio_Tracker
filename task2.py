import requests
from prettytable import PrettyTable

# Write your own api key here
API_KEY = 'write your api key here'

# Getting real time stock price from Alpha Vantage
def get_stock_price(symbol):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()

        if "Error Message" in data:
            print(f"Error fetching data for {symbol}. The stock symbol might be incorrect.")
            return None
        elif "Time Series (1min)" in data:
            latest_data = data['Time Series (1min)']
            latest_time = list(latest_data.keys())[0]
            return float(latest_data[latest_time]['1. open'])  # Return the latest stock price
        else:
            print(f"Data for {symbol} is not available or API limit reached.")
            return None

class Portfolio:
        def __init__(self):
            self.stocks = {}  

# Here adding stock to portfolio
        def add_stock(self, symbol, shares):
            if symbol in self.stocks:
                self.stocks[symbol] += shares
            else:
                self.stocks[symbol] = shares
            print(f"Added {shares} shares of {symbol} to your portfolio.")

# Here removing stock from portfolio
        def remove_stock(self, symbol, shares):
            if symbol in self.stocks:
                if self.stocks[symbol] > shares:
                    self.stocks[symbol] -= shares
                    print(f"Removed {shares} shares of {symbol} from your portfolio.")
                elif self.stocks[symbol] == shares:
                    del self.stocks[symbol]
                    print(f"Removed all shares of {symbol} from your portfolio.")
                else:
                    print(f"You don't own that many shares of {symbol}.")
            else:
                print(f"{symbol} is not in your portfolio.")

# Here view stock portfolio with real-time stock data
        def view_portfolio(self):
            if not self.stocks:
                print("Your portfolio is empty.")
                return

            table = PrettyTable()
            table.field_names = ["Symbol", "Shares", "Price per Share (USD)", "Total Value (USD)"]

            total_portfolio_value = 0.0
            for symbol, shares in self.stocks.items():
                price = get_stock_price(symbol)
                if price:
                    total_value = shares * price
                    table.add_row([symbol, shares, f"${price:.2f}", f"${total_value:.2f}"])
                    total_portfolio_value += total_value

            print(table)
            print(f"Total Portfolio Value: ${total_portfolio_value:.2f}")

def main():
        portfolio = Portfolio()

        while True:
            print("\n--- Stock Portfolio Tracker ---")
            print("1. Add stock")
            print("2. Remove stock")
            print("3. View portfolio")
            print("4. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                symbol = input("Enter stock symbol (e.g., AAPL): ").upper()
                shares = int(input(f"Enter number of shares to add for {symbol}: "))
                portfolio.add_stock(symbol, shares)

            elif choice == "2":
                symbol = input("Enter stock symbol (e.g., AAPL): ").upper()
                shares = int(input(f"Enter number of shares to remove for {symbol}: "))
                portfolio.remove_stock(symbol, shares)

            elif choice == "3":
                portfolio.view_portfolio()

            elif choice == "4":
                print("Exiting the stock portfolio tracker.")
                break

            else:
                print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
        main()
