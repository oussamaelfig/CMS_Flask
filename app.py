# Code permanent : ELFO74030209
# Nom et Prenom : OUSSAMA EL-FIGHA

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
    c.execute(
        "SELECT * FROM article WHERE date_publication <= ? "
        "ORDER BY date_publication "
        "DESC LIMIT 5",
        (today,))
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
    c.execute(
        "SELECT * FROM article WHERE article.titre LIKE ? OR"
        " article.paragraphe LIKE ?",
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


@app.route('/admin')
def admin():
    # Connect to the database
    conn = sqlite3.connect('db/infoArticle.db')
    c = conn.cursor()

    # Retrieve all articles
    c.execute("SELECT * FROM article")
    articles = c.fetchall()

    # Close the database connection
    conn.close()

    return render_template('admin.html', articles=articles)


@app.route('/admin-editer/<identifier>', methods=['GET', 'POST'])
def admin_edit(identifier):
    # Connect to the database
    conn = sqlite3.connect('db/infoArticle.db')
    c = conn.cursor()

    # Retrieve the article with the specified identifier
    c.execute("SELECT * FROM article WHERE identifiant=?", (identifier,))
    article = c.fetchone()

    # If no article was found, return a 404 error page
    if article is None:
        return render_template('404.html'), 404

    if request.method == 'POST':
        # Retrieve the form data
        titre = request.form['titre']
        paragraphe = request.form['paragraphe']

        # Check the length of the fields
        titre_len = len(titre)
        paragraphe_len = len(paragraphe)

        if titre_len > 100:
            error = 'Le champs Titre ne doit pas depasser 100 caracteres'
            return render_template('admin_edit.html',
                                   article=article, error=error)

        if paragraphe_len > 500:
            error = 'Le champs Paragraphe ne doit pas depasser 500 caracteres'
            return render_template('admin_edit.html',
                                   article=article, error=error)

        # Update the article in the database
        c.execute("UPDATE article SET titre=?,"
                  " paragraphe=? WHERE identifiant=?",
                  (titre, paragraphe, identifier))
        conn.commit()

        # Close the database connection
        conn.close()

        # Redirect to the article page
        return redirect(url_for('article', identifier=identifier))

    # Close the database connection
    conn.close()

    return render_template('admin_edit.html', article=article)


@app.route('/admin-nouveau', methods=['GET', 'POST'])
def admin_new():
    if request.method == 'POST':
        # Connect to the database
        conn = sqlite3.connect('db/infoArticle.db')
        c = conn.cursor()

        # Retrieve the form data
        titre = request.form['titre']
        identifiant = request.form['identifiant']
        auteur = request.form['auteur']
        date_publication = request.form['date_publication']
        paragraphe = request.form['paragraphe']

        # Validate the form data
        error = None

        if len(titre) > 100:
            error = 'Le champs Titre ne doit pas depasser 100 caracteres'

        if len(identifiant) > 50:
            error = 'Le champs Identifiant ne doit pas depasser 50 caracteres'

        if len(auteur) > 100:
            error = 'Le champs Auteur ne doit pas depasser 100 caracteres'

        if len(paragraphe) > 500:
            error = 'Le champs Paragraphe ne doit pas depasser 500 caracteres'

        if not titre or not identifiant or not auteur \
                or not paragraphe or not date_publication:
            error = 'Tout les champs doivent ??tre remplies'

        if error is not None:
            return render_template('admin_new.html', titre=titre,
                                   identifiant=identifiant, auteur=auteur,
                                   paragraphe=paragraphe,
                                   date_publication=date_publication,
                                   error=error)

        try:
            datetime.datetime.strptime(date_publication, '%Y-%m-%d')
        except ValueError:
            error = 'Format de date est invalide,' \
                    ' veuillez utiliser le format YYYY-MM-DD'
            return render_template('admin_new.html', titre=titre,
                                   identifiant=identifiant, auteur=auteur,
                                   paragraphe=paragraphe,
                                   date_publication=date_publication,
                                   error=error)

            # Insert the new article into the database
        c.execute(
            "INSERT INTO article (titre,identifiant, auteur, paragraphe, "
            "date_publication) VALUES (?, ?, ?, ?, ?)",
            (titre, identifiant, auteur, paragraphe, date_publication))
        conn.commit()

        # Close the database connection
        conn.close()

        # Redirect to the admin page
        return redirect(url_for('admin'))

    return render_template('admin_new.html')


if __name__ == '__main__':
    app.run(debug=True)
