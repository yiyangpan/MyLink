#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('gott_is_a_ladyboy.db')

c = conn.cursor()

# Turn on foreign key support
c.execute("PRAGMA foreign_keys = ON")

# Create users table
c.execute('''CREATE TABLE users
	     (	      
	      email TEXT NOT NULL, 
	      first_name TEXT NOT NULL, 
	      last_name TEXT NOT NULL,
	      password TEXT NOT NULL)''')

# Create twitts table
c.execute('''CREATE TABLE twitts
	     (	      
	      time DATETIME NOT NULL,
	      msg TEXT NOT NULL,
	      owner TEXT NOT NULL,
	      id INTEGER PRIMARY KEY AUTOINCREMENT,
	      parent INT NOT NULL,
	      FOREIGN KEY(owner) REFERENCES users(email)
	      )''')

# CREATE subscribe table
c.execute('''CREATE TABLE subscribe
	     (id INTEGER PRIMARY KEY AUTOINCREMENT,
	      owner TEXT NOT NULL,
	      target TEXT NOT NULL,
	      FOREIGN KEY(owner) REFERENCES users(email)
	     )''')

# Create album table
# Visibility is 'public' or 'private'
c.execute('''CREATE TABLE albums
	     (name TEXT NOT NULL,
	      owner TEXT NOT NULL,
	      visibility TEXT NOT NULL,
	      FOREIGN KEY (owner) REFERENCES users(email),
	      PRIMARY KEY(name, owner))''')

# Create pictures table
c.execute('''CREATE TABLE pictures
	     (path TEXT NOT NULL,
	      album TEXT NOT NULL,
	      owner TEXT NOT NULL,
	      FOREIGN KEY(album, owner) REFERENCES albums(name, owner),
	      FOREIGN KEY(owner) REFERENCES users(email),
	      PRIMARY KEY(path))''')

# Create sessions table
c.execute('''CREATE TABLE sessions
	     (user TEXT NOT NULL,
	      session TEXT NOT NULL,
	      FOREIGN KEY(user) REFERENCES users(email),
	      PRIMARY KEY(session))''')


# Save the changes
conn.commit()

# Close the connection
conn.close()
