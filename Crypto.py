import requests
import matplotlib.pyplot as plt
from datetime import datetime
import sys

# -----------------------------
# Settings
# -----------------------------
CRYPTO = ["bitcoin", "ethereum"]  # list of cryptocurrencies
CURRENCY = "usd"                  # currency
DAYS = 7                           # number of days to plot

# -----------------------------
# Fetch data from API
# -----------------------------
def get_crypto_data(crypto):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart"
    params = {"vs_currency": CURRENCY, "days": DAYS}
    response = requests.get(url, params=params)
    data = response.json()
    return data["prices"]  # list of [(timestamp, price)]

# -----------------------------
# Plot chart
# -----------------------------
def plot_crypto_data(crypto_data):
    plt.figure(figsize=(10,6))
    for name, data in crypto_data.items():
        times = [datetime.fromtimestamp(ts/1000) for ts, price in data]
        prices = [price for ts, price in data]
        plt.plot(times, prices, label=name.capitalize())

    plt.title(f"Price of {', '.join([c.capitalize() for c in CRYPTO])} in Last {DAYS} Days")
    plt.xlabel("Date")
    plt.ylabel(f"Price ({CURRENCY.upper()})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("crypto_dashboard.png")
    plt.show()

# -----------------------------
# Main function
# -----------------------------
def main():
    crypto_data = {}
    for coin in CRYPTO:
        # Safe print for all platforms
        sys.stdout.buffer.write(("Fetching data for " + coin + "...\n").encode('utf-8'))
        crypto_data[coin] = get_crypto_data(coin)

    sys.stdout.buffer.write("Plotting chart...\n".encode('utf-8'))
    plot_crypto_data(crypto_data)
    sys.stdout.buffer.write("Chart saved: crypto_dashboard.png\n".encode('utf-8'))

if __name__ == "__main__":
    main()
