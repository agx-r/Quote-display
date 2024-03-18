from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from flask import Flask, render_template, jsonify, request
import yfinance as yf
import asyncio
import aiohttp

app = Flask(__name__)
browser_opened = False
request_queue = asyncio.Queue()

def open_browser_on_localhost():
    print("BROWSER STARTED")
    firefox_options = Options()
    firefox_options.add_argument("--start-fullscreen")
    driver = webdriver.Firefox(options=firefox_options)
    driver.get("http://localhost:5000")

async def fetch_quote(session, symbol):
    async with session.get(f"http://localhost:5000/get_quote/{symbol}") as response:
        return await response.json()

async def fetch_price(session, symbol):
    async with session.get(f"http://localhost:5000/price/{symbol}") as response:
        return await response.json()

async def fetch_data(symbol):
    async with aiohttp.ClientSession() as session:
        quote_task = fetch_quote(session, symbol)
        price_task = fetch_price(session, symbol)
        quote = await quote_task
        price = await price_task
        return quote, price

async def process_requests():
    while True:
        symbol = await request_queue.get()
        try:
            quote, price = await fetch_data(symbol)
            print(f"Quote and price for {symbol} fetched successfully.")
            # You can handle the fetched data here
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
        finally:
            request_queue.task_done()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_quote/<symbol>')
def get_quote(symbol):
    try:
        ticker_info = yf.Ticker(symbol).info
        return jsonify({'symbol': symbol, 'info': ticker_info})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/price/<symbol>')
def get_index_quote_price(symbol):
    try:
        data = yf.download(symbol, period="1d")
        last_price = data["Close"].iloc[-1]
        return jsonify({"symbol": symbol, "price": last_price})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/fetch_data/<symbol>')
def fetch_data_route(symbol):
    request_queue.put_nowait(symbol)
    return jsonify({"message": f"Request for {symbol} added to the queue."})

if __name__ == '__main__':
    open_browser_on_localhost()
    # Start processing requests in the background
    asyncio.ensure_future(process_requests())
    # Run the Flask app with asyncio event loop
    app.run(debug=False, threaded=False)
