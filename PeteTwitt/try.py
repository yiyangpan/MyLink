#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('tweet.db')
c = conn.cursor()

# Add one user

# Larger example that inserts many records at a time
twitts = [('2014-04-28 11:33:55', 'are you fucking serious?' ,'gott',21),
             ('2014-04-28 01:31:52', 'I know right? this project is so damn time consuming','mary@gmail.com',19),
             ('2014-04-28 12:33:51', 'FUCK YOU ALL (LOL)' ,'peter@gmail.com',18),
            ]
c.executemany('INSERT INTO twitts(time,msg,owner,parent) VALUES (?,?,?,?)', twitts)

# commit or there are no changes
conn.commit()

print 'Done.'
