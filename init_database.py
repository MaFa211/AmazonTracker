import sqlite3	
# Set up database
connection = sqlite3.connect("amazon_track.db")
c = connection.cursor()
#c.execute("DROP TABLE results")
connection.commit()
c.execute("""
        CREATE TABLE results(
            name text,
            price real,
            date text)                        
            """)