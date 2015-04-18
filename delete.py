#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('picture_share.db')
c = conn.cursor()


print
print 'Delete the circles'
c.execute('DELETE FROM friendCircles;')
conn.commit()

print
print 'Delete the circleMembers'
c.execute('DELETE FROM circleMembers;')
conn.commit()

print
print 'Delete the twitts'
c.execute('DELETE FROM twitts;')
conn.commit()


# Close the connection
print 'Done.'
