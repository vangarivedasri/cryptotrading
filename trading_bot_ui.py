import tkinter as tk
from tkinter import messagebox
from binance.client import Client
import logging

# simple logging setup
logging.basicConfig(filename='trade_ui_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

class TradingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Binance Testnet Trading Bot")

        # heading
        tk.Label(root, text="Simplified Trading Bot (Testnet)", font=("Arial", 13, "bold")).pack(pady=10)

        # API key input
        tk.Label(root, text="API Key:").pack()
        self.key_entry = tk.Entry(root, width=45, show="*")
        self.key_entry.pack()

        # API secret input
        tk.Label(root, text="API Secret:").pack()
        self.secret_entry = tk.Entry(root, width=45, show="*")
        self.secret_entry.pack()

        # trading details
        tk.Label(root, text="Symbol (ex: BTCUSDT):").pack()
        self.symbol_entry = tk.Entry(root)
        self.symbol_entry.pack()

        tk.Label(root, text="Side (BUY / SELL):").pack()
        self.side_entry = tk.Entry(root)
        self.side_entry.pack()

        tk.Label(root, text="Order Type (MARKET / LIMIT):").pack()
        self.type_entry = tk.Entry(root)
        self.type_entry.pack()

        tk.Label(root, text="Quantity:").pack()
        self.qty_entry = tk.Entry(root)
        self.qty_entry.pack()

        tk.Label(root, text="Price (for LIMIT only):").pack()
        self.price_entry = tk.Entry(root)
        self.price_entry.pack()

        # button to place order
        tk.Button(root, text="Place Order", command=self.place_order, bg="#1a8f3d", fg="white", width=20).pack(pady=10)

        self.result_label = tk.Label(root, text="", fg="blue")
        self.result_label.pack()

    def place_order(self):
        api_key = self.key_entry.get().strip()
        api_secret = self.secret_entry.get().strip()
        symbol = self.symbol_entry.get().upper()
        side = self.side_entry.get().upper()
        order_type = self.type_entry.get().upper()
        qty = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()

        # basic input validation
        if not all([api_key, api_secret, symbol, side, order_type, qty]):
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        try:
            qty = float(qty)
            price_val = float(price) if price else None

            client = Client(api_key, api_secret, testnet=True)
            client.FUTURES_URL = "https://testnet.binancefuture.com"

            logging.info(f"Trying order: {symbol} {side} {order_type} {qty}")

            if order_type == "LIMIT" and price_val:
                order = client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type="LIMIT",
                    quantity=qty,
                    price=price_val,
                    timeInForce="GTC"
                )
            else:
                order = client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type="MARKET",
                    quantity=qty
                )

            msg = f"Order placed successfully!\nOrder ID: {order['orderId']}"
            messagebox.showinfo("Success", msg)
            self.result_label.config(text="✅ Order Placed Successfully", fg="green")
            logging.info(f"Order success: {order}")

        except Exception as e:
            logging.error(f"Order failed: {e}")
            messagebox.showerror("Error", f"Error placing order:\n{e}")
            self.result_label.config(text="❌ Failed to place order", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = TradingApp(root)
    root.mainloop()
