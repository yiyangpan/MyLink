#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random
import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
import session
import time

#Get Databasedir
MYLOGIN="xiao67"
DATABASE="/homes/"+MYLOGIN+"/PeteTwitt/tweet.db"
IMAGEPATH="/homes/"+MYLOGIN+"/PeteTwitt/images"

##############################################################
# Define function to generate login HTML form.
def login_form():
	html="""
<HTML>
<HEAD>
<TITLE>Info Form</TITLE>
</HEAD>

<BODY BGCOLOR = white>

<center><H2>PeteTwitt</H2></center>

<H3>Type User and Password:</H3>

<TABLE BORDER = 0>
<FORM METHOD=post ACTION="login.cgi">
<TR><TH>Email:</TH><TD><INPUT TYPE=text NAME="email"></TD><TR>
<TR><TH>Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
</TABLE>

<INPUT TYPE=hidden NAME="action" VALUE="login">
<INPUT TYPE=submit VALUE="Enter">
</FORM>

<FORM METHOD=post ACTION="login.cgi">
<INPUT TYPE=hidden NAME="action" VALUE="signup">
<INPUT TYPE=submit VALUE="Sign Up">
</FORM>

</BODY>
</HTML>
"""
	print_html_content_type()
	print(html)

# Define function to generate signup HTML form.
def signup_form():
	html="""
<HTML>
<HEAD>
<TITLE>Info Form</TITLE>
</HEAD>

<BODY BGCOLOR = white>

<center><H2>Register</H2></center>

<H3>Type User and Password:</H3>

<TABLE BORDER = 0>
<FORM METHOD=post ACTION="login.cgi">
<TR><TH>First name:</TH><TD><INPUT TYPE=text NAME="first_name"></TD><TR>
<TR><TH>Last name:</TH><TD><INPUT TYPE=text NAME="last_name"></TD><TR>
<TR><TH>Email:</TH><TD><INPUT TYPE=text NAME="email"></TD><TR>
<TR><TH>Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
</TABLE>

<INPUT TYPE=hidden NAME="action" VALUE="add_user">	
<input type=hidden name="user" value={user}>
<input type=hidden name="session" value={session}>
<INPUT TYPE=submit VALUE="Register">
</FORM>

</BODY>
</HTML>
"""
	print_html_content_type()
	print(html)

def change_password_form():
	html="""
<HTML>
<HEAD>
<TITLE>Info Form</TITLE>
</HEAD>

<BODY BGCOLOR = white>

<center><H2>ARE YOU FUCKING SERIOUS??? CHANGING PASSWORD?????!!!</H2></center>

<TABLE BORDER = 0>
<FORM METHOD=post ACTION="login.cgi">
<TR><TH>New Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
</TABLE>

<INPUT TYPE=hidden NAME="action" VALUE="change_password">	
<input type=hidden name="user" value={user}>
<input type=hidden name="session" value={session}>
<INPUT TYPE=submit VALUE="Submit">
</FORM>

</BODY>
</HTML>
"""
	print_html_content_type()
	print(html)


###################################################################
# Define function to test the password.
def check_password(user, passwd):

	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()

	t = (user,)
	c.execute('SELECT * FROM users WHERE email=?', t)

	row = stored_password=c.fetchone()
	conn.close();

	if row != None: 
	  stored_password=row[3]
	  if (stored_password==passwd):
		 return "passed"

	return "failed"

##########################################################
# Diplay the options of admin
def display_admin_options(user, session):
	conn = sqlite3.connect(DATABASE)
	with conn:
		c = conn.cursor()
		c.execute("SELECT * FROM twitts ORDER BY time DESC")
		data = c.fetchall()	
	html="""
	<head>
	<title>PeteTwitt</title>
	</head>

	<body>
		<H1> Tweet your shit here!</H1>
	<form method=post action="login.cgi">
	<INPUT TYPE=text name="message">
	<input type=hidden name="action" value="twitt">
	<input type=hidden name="user" value={user}>
	<input type=hidden name="session" value={session}>
	<input type=submit value="Twitt">
	</form>

	<FORM METHOD=post ACTION="login.cgi">
	<INPUT TYPE=text name="message">
	<INPUT TYPE=hidden NAME="action" VALUE="subscribe">
	<input type=hidden name="user" value={user}>
	<input type=hidden name="session" value={session}>
	<INPUT TYPE=submit VALUE="Subscribe">
	</FORM>

		<ul>
		<li> <a href="login.cgi?action=change_password_form&user={user}&session={session}">Change pasword</a>
		<li> <a href="login.cgi?action=upload&user={user}&session={session}">Upload Avatar</a>
		<li> <a href="login.cgi?action=show_image&user={user}&session={session}">Show Image</a>
		<li> <a href="login.cgi?action=return_login&user={user}&session={session}">Return to login</a>
		</ul>
	</body>
		"""
		
	#Also set a session number in a hidden field so the
		#cgi can check that the user has been authenticated


	print_html_content_type()
	print(html.format(user=user,session=session))
	conn = sqlite3.connect(DATABASE)
	t = (user,)
	with conn:
		c = conn.cursor()
		c.execute("SELECT * FROM subscribe where owner=? ",t)
		data2 = c.fetchall()	
		for twit in data:
			for target in data2:
				if (twit[2]==target[2]):
					print "Twitt id:" + str(twit[3]) + "|  Date:" + twit[0] + " |	" + twit[1]+ "	|	" + "id: " + twit[2] + "<br>"
					now=twit[3]
					for twit in data:
						if (twit[4]==now):
							print "&nbsp &nbsp &nbsp &nbsp &nbsp Twitt id:  " + str(twit[3]) + "| Date:" + twit[0] + " |	" + twit[1]+ "	|	" + "id: " + twit[2] + "<br>"
					

#################################################################
def create_new_session(user):
	return session.create_session(user)

##############################################################
def new_album(form):
	#Check session
	if session.check_session(form) != "passed":
	   return

	html="""
		<H1> New Album</H1>
		"""
	print_html_content_type()
	print(html);

##############################################################
def show_image(form):
	#Check session
	if session.check_session(form) != "passed":
	   login_form()
	   return

	# Your code should get the user album and picture and verify that the image belongs to this
	# user and this album before loading it

	#username=form["username"].value

	# Read image
	with open(IMAGEPATH+'/user1/test.jpg', 'rb') as content_file:
	   content = content_file.read()

	# Send header and image content
	hdr = "Content-Type: image/jpeg\nContent-Length: %d\n\n" % len(content)
	print hdr+content

###############################################################################

def upload(form):
	if session.check_session(form) != "passed":
	   login_form()
	   return

	html="""
		<HTML>

		<FORM ACTION="login.cgi" METHOD="POST" enctype="multipart/form-data">
			<input type="hidden" name="user" value="{user}">
			<input type="hidden" name="session" value="{session}">
			<input type="hidden" name="action" value="upload-pic-data">
			<BR><I>Browse Picture:</I> <INPUT TYPE="FILE" NAME="file">
			<br>
			<input type="submit" value="Press"> to upload the picture!
			<a href="login.cgi?action=return&user={user}&session={session}">Return</a>
			</form>
		</HTML>
	"""

	user=form["user"].value
	s=form["session"].value
	print_html_content_type()
	print(html.format(user=user,session=s))
	print ('<a href="login.cgi?action=return&user={user}&session={session}">Return</a>')

#######################################################

def upload_pic_data(form):
	#Check session is correct
	if (session.check_session(form) != "passed"):
		login_form()
		return

	#Get file info
	fileInfo = form['file']

	#Get user
	user=form["user"].value
	s=form["session"].value

	# Check if the file was uploaded
	if fileInfo.filename:
		# Remove directory path to extract name only
		fileName = os.path.basename(fileInfo.filename)
		open(IMAGEPATH+'/user1/test.jpg', 'wb').write(fileInfo.file.read())
		image_url="login.cgi?action=show_image&user={user}&session={session}".format(user=user,session=s)
		print_html_content_type()
		print ('<H2>The picture ' + fileName + ' was uploaded successfully</H2>')
		print('<image src="'+image_url+'">')
		print ('<a href="login.cgi?action=return&user={user}&session={session}">Return</a>')
	else:
		message = 'No file was uploaded'

def print_html_content_type():
	# Required header that tells the browser how to render the HTML.
	print("Content-Type: text/html\n\n")

##############################################################
# Define main function.
def main():
	form = cgi.FieldStorage()
	if "action" in form:
		action=form["action"].value
		#print("action=",action)
		if action == "login":
			if "email" in form and "password" in form:
				#Test password
				username=form["email"].value
				password=form["password"].value
				if check_password(username, password)=="passed":
				   session=create_new_session(username)
				   display_admin_options(username, session)
				else:
				   login_form()
				   print("<H3><font color=\"red\">Incorrect email/password</font></H3>")
		elif action == "signup":
			signup_form()
		elif action == "add_user":
			if "email" in form and "password" in form and "first_name" in form and "last_name" in form:
				username=form["email"].value
				password=form["password"].value
				first_name=form["first_name"].value
				last_name=form["last_name"].value		
				conn = sqlite3.connect(DATABASE)
				with conn:
					c = conn.cursor()
					t = (username,first_name,last_name,password)
					c.execute("INSERT INTO users VALUES (?,?,?,?);",t)
				with conn:
					c = conn.cursor()
					t = (username,username)
					c.execute('INSERT INTO subscribe(owner,target) VALUES (?,?)', t)
				login_form()
		elif (action == "change_password_form"):
			change_password_form()
		elif (action == "change_password"):
			newpassword=form["password"].value
			conn = sqlite3.connect(DATABASE)
			with conn:
				c = conn.cursor()
				owner = form["user"].value
				params = (newpassword,owner)				
				c.execute('UPDATE users SET password=? WHERE email=?', params);
				conn.commit()
			login_form()
		elif (action == "new-album"):
			new_album(form)
		elif (action == "upload"):
			upload(form)
		elif (action == "show_image"):
			show_image(form)
		elif action == "upload-pic-data":
			upload_pic_data(form)
		elif action == "subscribe":
			if "message" in form:		
				target = form["message"].value
				conn = sqlite3.connect(DATABASE)
				with conn:
					c = conn.cursor()
					t = (form["user"].value,target)
					c.execute('INSERT INTO subscribe(owner,target) VALUES (?,?)', t)

				display_admin_options(form["user"].value, form["session"].value)
		elif action == "twitt":
			if "message" in form:		
				msg = form["message"].value
				now = time.strftime('%Y-%m-%d %H:%M:%S')
				conn = sqlite3.connect(DATABASE)
				with conn:
					c = conn.cursor()
					t = (now,msg,form["user"].value,0)
					c.execute("INSERT INTO twitts(time,msg,owner,parent) VALUES (?,?,?,?)",t)
				display_admin_options(form["user"].value, form["session"].value)
		elif action == "return_login":
			login_form()
		else:
			display_admin_options(form["user"].value, form["session"].value)
	else:
		login_form()
	#cgi.test()

###############################################################
# Call main function.
main()
