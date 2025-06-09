import os

print("Working Directory:", os.getcwd())
print("Files in current directory:", os.listdir())

# The rest of your code follows...

import ccxt
import time
import os
import json

# === Load ENV ===
API_KEY = os.getenv("OKX_API_KEY")
API_SECRET = os.getenv("OKX_API_SECRET")
PASSPHRASE = os.getenv("OKX_API_PASSPHRASE")

# === Config ===
SYMBOL = 'BTC/USDT'
TIMEFRAME = '1m'
RSI_PERIOD = 14
TRAILING_STOP = 0.003
MAX_HOLD = 120
MIN_BALANCE = 10
STATE_FILE = 'state.json'

# === Init ===
okx = ccxt.okx({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'password': PASSPHRASE,
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})

# === Utilities ===
def fetch_closes():
    candles = okx.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=RSI_PERIOD + 1)
    return [c[4] for c in candles]

def calculate_rsi(closes):
    deltas = [closes[i + 1] - closes[i] for i in range(len(closes) - 1)]
    gain = sum(d for d in deltas if d > 0) / RSI_PERIOD
    loss = -sum(d for d in deltas if d < 0) / RSI_PERIOD
    rs = gain / loss if loss != 0 else 0
    return 100 - (100 / (1 + rs))

def load_state():
    if not os.path.exists(STATE_FILE):
        return {'wins': 0, 'losses': 0}
    with open(STATE_FILE, 'r') as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def get_balance():
    return okx.fetch_balance()['total']['USDT']

def get_trade_size(balance, price):
    tier = 0.025 if balance < 25 else 0.05 if balance < 150 else 0.1
    return round((balance * tier) / price, 4)

def trailing_logic(entry, current, signal, stop):
    delta = current * TRAILING_STOP
    if signal == 'buy':
        return max(stop, current - delta)
    else:
        return min(stop, current + delta)

# === Main Bot ===
def run():
    state = load_state()
    while True:
        try:
            balance = get_balance()
            if balance < MIN_BALANCE:
                print("[!] Low balance. Sleeping.")
                time.sleep(300)
                continue

            closes = fetch_closes()
            rsi = calculate_rsi(closes)
            signal = None

            if rsi <= 30:
                signal = 'buy'
            elif rsi >= 70:
                signal = 'sell'

            if not signal:
                print("[!] No trade signal.")
                time.sleep(30)
                continue

            price = okx.fetch_ticker(SYMBOL)['last']
            size = get_trade_size(balance, price)
            order = okx.create_market_order(SYMBOL, signal, size)
            entry = order['average']
            stop = trailing_logic(entry, entry, signal, entry)
            print(f"[+] Entered {signal.upper()} @ {entry}")

            exit_side = 'sell' if signal == 'buy' else 'buy'
            start = time.time()

            while time.time() - start < MAX_HOLD:
                current = okx.fetch_ticker(SYMBOL)['last']
                stop = trailing_logic(entry, current, signal, stop)
                if (signal == 'buy' and current <= stop) or (signal == 'sell' and current >= stop):
                    exit_order = okx.create_market_order(SYMBOL, exit_side, size)
                    print(f"[-] Exited {exit_side.upper()} @ {exit_order['average']}")
                    pnl = (current - entry) if signal == 'buy' else (entry - current)
                    if pnl > 0:
                        state['wins'] += 1
                        state['losses'] = 0
                    else:
                        state['losses'] += 1
                        state['wins'] = 0
                    save_state(state)
                    break
                time.sleep(10)

            if state['losses'] >= 2:
                print("[!] 2 Losses. Studying market before next trade.")
                time.sleep(300)
                state['losses'] = 0
                save_state(state)

            time.sleep(30)

        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(60)

if __name__ == "__main__":
    run()
