from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    # Connect to the database
    conn = sqlite3.connect('db/infoArticle.db')
    c = conn.cursor()

    # Retrieve the last 5 publications as of today's date
    c.execute(
        "SELECT * FROM article WHERE date(date_publication) <= date('now') ORDER BY date(date_publication) DESC LIMIT 5")
    publications = c.fetchall()

    # Close the database connection
    conn.close()

    # Render the home page template with the publications data
    return render_template('home.html', publications=publications)


@app.route('/search')
def search():
    # Get the search query from the request
    query = request.args.get('q')

    # Connect to the database
    conn = sqlite3.connect('db/infoArticle.db')
    c = conn.cursor()

    # Search for articles with the query in the title or paragraph
    c.execute(
        "SELECT identifiant, titre, date_publication FROM article WHERE titre LIKE ? OR paragraphe LIKE ? ORDER BY date("
        "date_publication) DESC",
        ('%' + query + '%', '%' + query + '%'))
    search_results = c.fetchall()

    # Close the database connection
    conn.close()

    # Render the search results template with the search query and results data
    return render_template('search.html', query=query, search_results=search_results)


@app.route('/article/<identifier>')
def article(identifier):
    # Connect to the database
    conn = sqlite3.connect('db/infoArticle.db')
    c = conn.cursor()

    # Retrieve the article with the given identifier
    c.execute("SELECT * FROM article WHERE identifiant = ?", (identifier,))
    article = c.fetchone()

    # Close the database connection
    conn.close()

    # Check if the article was found
    if article is None:
        return render_template('404.html'), 404

    # Render the article page template with the article data
    return render_template('article.html', article=article)


if __name__ == '__main__':
    app.run(debug=True)
