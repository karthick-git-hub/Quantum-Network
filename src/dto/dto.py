import sqlite3

def setup():
    # Connect to or create the database
    conn = sqlite3.connect('example.db')

    # Create a cursor
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS replay (
            id INTEGER PRIMARY KEY,
            nodeTraversal TEXT
        )
    ''')
    return conn

def insert(nodeTraversal):
    # Insert values into the table
    conn = setup()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO replay (id, nodeTraversal) VALUES (?, ?)', (1, nodeTraversal))
    conn.commit()

    # Close the connection
    conn.close()


def select(id):
    conn = setup()
    cursor = conn.cursor()

    cursor.execute('SELECT nodeTraversal FROM replay where id =' + id)
    rows = cursor.fetchall()

    # Close the connection
    conn.close()
    return rows