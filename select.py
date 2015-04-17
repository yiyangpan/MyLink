#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('picture_share.db')
c = conn.cursor()

print
t = ('Bowling','ypan91@gmail.com')
c.execute('SELECT friendCircleID FROM friendCircles WHERE friendCircleName = ? AND owner = ?;', t)
print c.fetchone()[0]

