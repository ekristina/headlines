from urllib.parse import quote

import feedparser
import json
import requests

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


# https://openexchangerates.org/account/app-ids

RSS_FEEDS = {'blogto': "http://feeds.feedburner.com/blogto",
             'blurt': "https://www.blurtitout.org/feed/",
             "npr": "https://www.npr.org/rss/rss.php?id=1007"}

DEFAULTS = {'source': 'blogto',
            'city': 'Toronto',
            'currency_from': 'USD',
            'currency_to': 'CAD'}

WEATHER_API_KEY = "f23e0a7bdffde96f9b6e38c7090f8787"
CURRENCY_API_KEY = "e2929d73c3794e92a55964b8517b1ae5"

CURRENCY_URL = f"https://openexchangerates.org//api/latest.json?" \
               f"app_id={CURRENCY_API_KEY}"


def get_weather(query):
    query = quote(query)
    url = f"http://api.openweathermap.org/data/2.5/weather?" \
          f"q={query}&units=metric&appid={WEATHER_API_KEY}"

    data = requests.get(url).text
    parsed = json.loads(data)

    weather = None
    if parsed.get("weather"):
        weather = {
            "description": parsed["weather"][0]["description"],
            "temperature": parsed["main"]["temp"],
            "city": parsed["name"],
            "country": parsed["sys"]["country"]
        }

    return weather


def get_rate(frm, to):
    all_currency = requests.get(CURRENCY_URL)
    parsed = json.loads(all_currency.text).get('rates')

    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())

    return to_rate/frm_rate, list(parsed.keys())


def get_news(source):

    if source.lower() not in RSS_FEEDS:
        source = DEFAULTS['source']

    feed = feedparser.parse(RSS_FEEDS[source.lower()])
    return feed['entries']


@app.route("/")
def home():

    # get rss

    source = request.args.get("source")
    if not source or source.lower() not in RSS_FEEDS:
        source = DEFAULTS['source']

    else:
        source = source.lower()

    articles = get_news(source)

    # get weather

    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']

    weather = get_weather(city)

    # get customized currency

    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS['currency_to']

    rate, currencies = get_rate(currency_from, currency_to)

    return render_template("home.html",
                           articles=articles,
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate,
                           currencies=sorted(currencies))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
