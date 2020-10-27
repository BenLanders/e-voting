import sqlite3
conn = sqlite3.connect('e_voting_user_data.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE users
             (userName, password)''')

c.execute('''CREATE TABLE votes
             (userName, vote)''')

c.execute('''CREATE TABLE admin
             (userName, password)''')

c.execute("INSERT INTO admin VALUES ('Admin','Admin')")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
