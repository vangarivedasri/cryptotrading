from binance.client import Client
import logging

# Setup logging (keeps track of actions & errors)
logging.basicConfig(filename="trade_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

class TradingBot:
    def __init__(self, api_key, api_secret):
        # Connect to Binance Testnet
        self.client = Client(api_key, api_secret, testnet=True)
        self.client.FUTURES_URL = "https://testnet.binancefuture.com"

    # Check balance for a specific asset (like USDT)
    def check_balance(self, asset="USDT"):
        try:
            data = self.client.futures_account_balance()
            for x in data:
                if x["asset"] == asset:
                    return float(x["balance"])
            return 0.0
        except Exception as e:
            logging.error(f"Error while checking balance: {e}")
            return 0.0

    # Function to place an order
    def place_order(self, symbol, side, order_type, qty, price=None, stop_price=None):
        try:
            if order_type == "LIMIT":
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type="LIMIT",
                    quantity=qty,
                    price=price,
                    timeInForce="GTC"
                )
            elif order_type == "STOP_MARKET":
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type="STOP_MARKET",
                    stopPrice=stop_price,
                    quantity=qty
                )
            else:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type="MARKET",
                    quantity=qty
                )

            logging.info(f"Order successful: {order}")
            return order
        except Exception as e:
            logging.error(f"Failed to place order: {e}")
            return {"error": str(e)}


if __name__ == "__main__":
    print("==== Binance Futures Testnet Bot ====")
    api_key = input("Enter your API key: ")
    api_secret = input("Enter your API secret: ")

    bot = TradingBot(api_key, api_secret)
    bal = bot.check_balance()
    print(f"Available USDT Balance: {bal}")

    symbol = input("Enter trading pair (ex: BTCUSDT): ").upper()
    side = input("Buy or Sell? (BUY/SELL): ").upper()
    order_type = input("Type of order (MARKET/LIMIT/STOP_MARKET): ").upper()
    qty = float(input("Quantity: "))

    price = None
    stop_price = None
    if order_type == "LIMIT":
        price = float(input("Enter Limit Price: "))
    elif order_type == "STOP_MARKET":
        stop_price = float(input("Enter Stop Price: "))

    confirm = input("Do you want to confirm this order? (y/n): ").lower()
    if confirm == "y":
        result = bot.place_order(symbol, side, order_type, qty, price, stop_price)
        print("Order details:", result)
    else:
        print("Order cancelled.")

