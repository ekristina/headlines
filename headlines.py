import feedparser

from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)

RSS_FEEDS = {'blogto': "http://feeds.feedburner.com/blogto",
             'blurt': "https://www.blurtitout.org/feed/",
             "npr": "https://www.npr.org/rss/rss.php?id=1007"}


@app.route("/")
def get_news():

    query = request.args.get("source")
    if not query or query.lower() not in RSS_FEEDS:
        source = "blogto"

    else:
        source = query.lower()

    feed = feedparser.parse(RSS_FEEDS[source])

    return render_template("home.html", articles=feed['entries'])


if __name__ == '__main__':
    app.run(port=5000, debug=True)
