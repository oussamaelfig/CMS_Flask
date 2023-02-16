import sqlite3

# Connect to the database
conn = sqlite3.connect('db/infoArticle.db')
c = conn.cursor()

# Execute a SELECT query to retrieve data from the article table
c.execute("SELECT * FROM article")

# Print the results
for row in c:
    print(row)

# Close the database connection
conn.close()
