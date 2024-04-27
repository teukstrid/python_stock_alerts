import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = '"STOCK_API_KEY'
NEWS_API_KEY = 'NEWS_API_KEY'

twilio_account_sid = 'TWILIO_ACC_SID'
twilio_auth_token = 'TWILIO_AUTH_TOKEN'
FROM_NUMBER = 'SENDERS_NUMBER'
TO_NUMBER = 'RECEIVERS_NUMBER'

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_data = stock_response.json()['Time Series (Daily)']

close_prices = [float(data['4. close']) for data, data in stock_data.items()]
close_price_day1 = close_prices[0]
close_price_day2 = close_prices[1]

difference = float(close_price_day1) - float(close_price_day2)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round(difference / float(close_price_day1) * 100)

if abs(diff_percent) > 1:
    print("Get news")
    news_parameters = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
        "language": "en"
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    articles = news_response.json()['articles']

    three_articles = articles[:3]

    formatted_articles = [f"{STOCK}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(twilio_account_sid, twilio_auth_token)

    for article in formatted_articles:
        message = client.messages.create(
            from_=FROM_NUMBER,
            body=article,
            to=TO_NUMBER
        )
