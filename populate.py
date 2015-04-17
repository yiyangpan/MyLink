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
            ]
c.executemany('INSERT INTO users VALUES (?,?,?,?)', users)

subscribe = [('george@gmail.com', 'mary@gmail.com'),
	      ('mary@gmail.com', 'george@gmail.com'),
            ]
c.executemany('INSERT INTO subscribe(owner,target) VALUES (?,?)', subscribe)

albums = [("album1",'george@gmail.com',"public"),
           ("album2",'george@gmail.com',"public"),
           ("album3",'george@gmail.com',"private"),
           ("album1",'mary@gmail.com',"public"),
         ]
c.executemany('INSERT INTO albums VALUES (?,?,?)', albums)

pictures = [
             ("image-89.jpg","album1","george@gmail.com"),
             ("image-90.jpg","album1","george@gmail.com"),
             ("image-91.jpg","album1","george@gmail.com"),
             ("image-92.jpg","album1","george@gmail.com"),
             ("image-93.jpg","album1","george@gmail.com"),
             ("image-94.jpg","album1","george@gmail.com"),
             ("image-95.jpg","album1","george@gmail.com"),
             ("image-96.jpg","album1","george@gmail.com"),
             ("image-97.jpg","album1","george@gmail.com"),
             ("image-98.jpg","album1","george@gmail.com"),
             ("image-99.jpg","album1","george@gmail.com"),
             ("image-100.jpg","album1","george@gmail.com"),
             ("image-101.jpg","album1","george@gmail.com"),
             ("image-102.jpg","album1","george@gmail.com"),
             ("image-103.jpg","album1","george@gmail.com"),
             ("image-104.jpg","album1","george@gmail.com"),
             ("image-105.jpg","album1","george@gmail.com"),
             ("image-106.jpg","album1","george@gmail.com"),
             ("image-107.jpg","album1","george@gmail.com"),
             ("image-108.jpg","album1","george@gmail.com"),
             ("image-109.jpg","album1","george@gmail.com"),
             ("image-110.jpg","album1","george@gmail.com"),
           ]

c.executemany('INSERT INTO pictures VALUES (?,?,?)', pictures)

twitts = [('2014-04-28 11:33:55', 'are you fucking serious?' ,'gott',21),
             ('2014-04-28 01:31:52', 'I know right? this project is so damn time consuming','mary@gmail.com',19),
             ('2014-04-28 12:33:51', 'FUCK YOU ALL (LOL)' ,'peter@gmail.com',18),
            ]
#c.executemany('INSERT INTO twitts(time,msg,owner,parent) VALUES (?,?,?,?)', twitts)

# commit or there are no changes
conn.commit()

print 'Done.'
