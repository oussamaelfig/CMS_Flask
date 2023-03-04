import sqlite3
import random
import string
from datetime import datetime, timedelta

# Connect to the database
conn = sqlite3.connect('db/infoArticle.db')
c = conn.cursor()

# Define some sample data
titles = ['Lorem ipsum dolor sit amet', 'Consectetur adipiscing elit',
          'Nullam vestibulum magna vel']
authors = ['John Doe', 'Jane Doe', 'Bob Smith', 'Alice Brown']
paragraphs = ['Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
              ' In ac magna ut velit dignissim gravida.',
              'Nullam vestibulum magna vel eros ultrices eleifend.'
              ' Donec a odio et mi convallis feugiat.']

# Generate 50 random articles and insert them into the database
for i in range(50):
    # Generate random data for the article
    title = random.choice(titles)
    identifier = ''.join(random.choices(string.ascii_lowercase + string.digits,
                                        k=8))
    author = random.choice(authors)
    date_publication = (datetime.now() -
                        timedelta(days=random.randint(0, 365))).date()
    paragraph = random.choice(paragraphs)

    # Insert the article into the database
    c.execute('INSERT INTO article (titre, identifiant, auteur,'
              ' date_publication, paragraphe) VALUES (?, ?, ?, ?, ?)',
              (title, identifier, author, date_publication.isoformat(),
               paragraph))

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()
