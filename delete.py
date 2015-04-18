#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('picture_share.db')
c = conn.cursor()

print
print 'Delete the circleMembers'
c.execute('DELETE FROM circleMembers;')
conn.commit()


# Close the connection
print 'Done.'
