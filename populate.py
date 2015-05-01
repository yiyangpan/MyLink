#!/usr/bin/python

import sqlite3

print
print "Run only once or you will get error for duplicates"
print 

conn = sqlite3.connect('picture_share.db')
c = conn.cursor()

# Add one user

# Larger example that inserts many records at a time
users = [('george@gmail.com', 'george','bush','abc123'),
             ('mary@gmail.com', 'mary','polard','mary123'),
             ('peter@gmail.com','peter','pan', 'peter123'),
			 ('ypan91@gmail.com','yiyang','pan', '1'),
            ]
c.executemany('INSERT INTO users VALUES (?,?,?,?)', users)

t = [('ypan91@gmail.com','ypan91@gmail.com'),('peter@gmail.com','peter@gmail.com'),]
c.executemany('INSERT INTO subscribe(owner,target) VALUES (?,?)', t)

#c.executemany('INSERT INTO twitts(time,msg,owner,parent) VALUES (?,?,?,?)', twitts)

# commit or there are no changes
conn.commit()

print 'Done.'
