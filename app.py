from flask import Flask, render_template
import yfinance as yf

app = Flask(__name__)

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
    app.run(debug=True)
