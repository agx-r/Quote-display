import webbrowser
from flask import Flask, render_template
import yfinance as yf
import pyautogui, time

app = Flask(__name__)
browser_opened = False

def open_browser_on_localhost():
    print("BROWSER STARTED")
    global browser_opened
    if not browser_opened:
        url = "http://localhost:5000"
        webbrowser.open(url)
        time.sleep(1)
        pyautogui.press('f11')
        browser_opened = True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_quote/<symbol>')
def get_quote(symbol):
    try:
        ticker_info = yf.Ticker(symbol).info
        return {'symbol': symbol, 'info': ticker_info}
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    open_browser_on_localhost()
    app.run(debug=False)