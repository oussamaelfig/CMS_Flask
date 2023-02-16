from flask import Flask, render_template, request, redirect, url_for, abort
import sqlite3
import datetime

app = Flask(__name__)


@app.route('/')
def home():
    # Connect to the database
    conn = sqlite3.connect('db/infoArticle.db')
    c = conn.cursor()

    # Retrieve the last 5 publications
    today = datetime.date.today().isoformat()
    c.execute("SELECT * FROM article WHERE date_publication <= ? ORDER BY date_publication DESC LIMIT 5", (today,))
    publications = c.fetchall()

    # Close the database connection
    conn.close()

    return render_template('home.html', publications=publications)


@app.route('/search')
def search():
    # Connect to the database
    conn = sqlite3.connect('db/infoArticle.db')
    c = conn.cursor()

    # Retrieve the search query from the request
    query = request.args.get('q')

    # Search for articles that contain the query in the title or paragraph
    c.execute("SELECT * FROM article WHERE article.titre LIKE ? OR article.paragraphe LIKE ?",
              ('%' + query + '%', '%' + query + '%'))
    results = c.fetchall()

    # Close the database connection
    conn.close()

    return render_template('search.html', results=results)


@app.route('/article/<identifier>')
def article(identifier):
    # Connect to the database
    conn = sqlite3.connect('db/infoArticle.db')
    c = conn.cursor()

    # Retrieve the article with the specified identifier
    c.execute("SELECT * FROM article WHERE identifiant=?", (identifier,))
    article = c.fetchone()

    # Close the database connection
    conn.close()

    # If no article was found, return a 404 error page
    if article is None:
        return render_template('404.html'), 404

    return render_template('article.html', article=article)


if __name__ == '__main__':
    app.run(debug=True)
