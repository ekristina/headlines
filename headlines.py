import feedparser

from flask import Flask


app = Flask(__name__)

RSS_FEEDS = {'blogto': "http://feeds.feedburner.com/blogto",
             'blurt': "https://www.blurtitout.org/feed/",
             "npr": "https://www.npr.org/rss/rss.php?id=1007"}


@app.route("/")
@app.route("/<source>")
def get_news(source="blogto"):
    feed = feedparser.parse(RSS_FEEDS[source])

    first_article = feed['entries'][0]
    return """<html>
    <body>
    
        <h1> {3} Headlines </h1>
        
        <b>{0}</b> <br />
        <i>{1}</i> <br />
        <p>{2}</p> <br />
    
    </body>
    
    </html>""".format(
        first_article.get("title"),
        first_article.get("published"),
        first_article.get("summary"),
        source
    )


if __name__ == '__main__':
    app.run(port=5000, debug=True)
