#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('picture_share.db')
c = conn.cursor()

print
print 'Print all users'
for row in c.execute('SELECT * FROM users'):
  print row


print
print 'Print all subscribe'
for row in c.execute('SELECT * FROM subscribe'):
  print row

print
print 'Print all friendCircles'
for row in c.execute('SELECT * FROM friendCircles'):
  print row

print
print 'Print all circleMembers'
for row in c.execute('SELECT * FROM circleMembers'):
  print row


print
print 'Print all twitts'
for row in c.execute('SELECT * FROM twitts'):
  print row

print
print "Print peter's password"
t = ('peter@gmail.com',)
c.execute('SELECT * FROM users WHERE email=?', t)
print c.fetchone()[1]

