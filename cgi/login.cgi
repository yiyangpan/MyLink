#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random
import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
import session
import time
import string
import random

#Get Databasedir
MYLOGIN="pan41"
DATABASE="/homes/"+MYLOGIN+"/apache/htdocs/MyLink/picture_share.db"
IMAGEPATH="/homes/"+MYLOGIN+"/apache/htdocs/MyLink/images"




##############################################################
def id_generator(size=10):
	chars=string.ascii_lowercase + string.ascii_uppercase +string.digits
	s=""
	for i in range (0,size):
		s+=random.choice(chars)
	return s

random_string =["RVszcK4IVXYZzq4","Me4Zdk7Hp9g7SXQ","uAhp88nyMHoxHry","kBX3L0DTnb61WEX","WwcPbN3MQ91EkW3","eEhMzwsC1iOJfuE","Md37DWub1LBM1Ci","lvrcxxqliT5P2Rg","jNwt8jI5FsceiEJ","jAj0WjtIltgqcHW","5feZacndHU45kqg","kSOk784fbl2ahPu","C1f0jCBm6UJe0Nu","IWgpvrzuwf858q6","f8E7tIDJtPbxMgM","sWmqy4a97EZtNoD","3LkPFgf5ygflbJ2","TiVLlOhYLwAVnlE","geuAQFr99JFMioM","zX71DL7CGKpdsvC"]

##############################################################
def encrypt(password):
	s=""
	i=0
	j=0
	for ch in password:
		i+=67
		j+=97
		s=s+random_string[(ord(ch) - 1+i)%15][min((ord(ch)*2),j) % 15:max((ord(ch)*2),j) % 15]

	#login_form()
	#print s
	return s

##############################################################
# Define function to generate login HTML form.
def login_form():
	html="""
	<html lang="en">
	<head>
        <meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">	
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="description" content="">
        <meta name="author" content="">

	<title>MyLink</title>

	<!-- Bootstrap core CSS -->
        <link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">

	<!-- Custom styles for this template -->
	<link href="signin.css" rel="stylesheet">
	</head>

	<body background="bg.jpg">
	<div class="container">
	<form method=post action="login.cgi" class="form-signin" role="form">	
	<div class="row">
	<div class="col-md-12">
	<h2 class="form-signin-heading" style="text-align: center; color:white">MyLink</h2>
	</div>
	</div>
	<input type="email" name="email" class="form-control" placeholder="Email address" required autofocus>
	<input type="password" name="password" class="form-control" placeholder="Password" required>
	<button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
	<input type="hidden" name="action" value="login">
	<a href="login.cgi?action=signup" class="btn btn-link btn-lg btn-block" role="button" style="color:white">Register</a>
	</form>

	</div> <!-- /container -->

	<!-- Bootstrap core JavaScript ================================================== -->
	<!-- Placed at the end of the document so the pages load faster -->
	
	</body>
	</html>
	"""
	print_html_content_type()
	print(html)

# Define function to generate signup HTML form.
def signup_form():
	html="""
<HTML>
<HEAD>
<TITLE>Info Form</TITLE>
<!-- Bootstrap core CSS -->
    <link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Custom styles for this template -->
<link href="signup.css" rel="stylesheet">
</HEAD>

<BODY background="bg.jpg" style="text-align: center">

<center><H2 style="text-align: center; color:white">Register</H2></center>

<H3 style="text-align: center; color:white">Type User and Password:</H3>

<TABLE align=center >
<FORM METHOD=post ACTION="login.cgi" style="text-align: center">
<TR style="text-align: center; color:white"><TH >First name:</TH><TD><INPUT TYPE=text NAME="first_name" ></TD><TR>
<TR style="text-align: center; color:white"><TH>Last name:</TH><TD><INPUT TYPE=text NAME="last_name"></TD><TR>
<TR style="text-align: center; color:white"><TH>Email:</TH><TD><INPUT TYPE=text NAME="email"></TD><TR>
<TR style="text-align: center; color:white"><TH>Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
</TABLE>

<INPUT TYPE=hidden NAME="action" VALUE="add_user" style="text-align: center">	
<input type=hidden name="user" value={user} style="text-align: center">
<input type=hidden name="session" value={session} style="text-align: center">
<br>
<INPUT class="btn btn-lg btn-primary" TYPE=submit VALUE="Register" >
</FORM>

</BODY>
</HTML>
"""
	print_html_content_type()
	print(html)


###################################################
def change_password_form(user, session):
	html="""
<HTML>
<HEAD>
<TITLE>Info Form</TITLE>
	<!-- Bootstrap core CSS -->
        <link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">

</HEAD>

<BODY background="bg.jpg">

<center><H2 style="text-align: center; color:white">Change the password</H2></center>

<TABLE align=center>
<FORM METHOD=post ACTION="login.cgi">
<TR><TH style="text-align: center; color:white">New Password:</TH><TD ><INPUT TYPE=password NAME="password"></TD></TR>
</TABLE>

<INPUT TYPE=hidden NAME="action" VALUE="change_password">	
<input type=hidden name="user" value={user}>
<input type=hidden name="session" value={session}>
<br>
<div style="text-align: center">
	<INPUT style="text-align: center" class="btn btn-lg btn-primary" TYPE=submit VALUE="Submit">
</div>
</FORM>

</BODY>
</HTML>
"""
	print_html_content_type()
	print(html.format(user=user,session=session))

###################################################################

def search_last_name_form(form):
	user=form["user"].value
	s=form["session"].value
	html="""
		<HTML>
<HEAD>
<TITLE>Info Form</TITLE>
<!-- Bootstrap core CSS -->
    <link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">
</HEAD>

<BODY background="bg.jpg">

<center><H2 style="text-align: center; color:white">Find friends on MyLink</H2></center>

<TABLE BORDER = 0>
<FORM METHOD=post ACTION="login.cgi">
<TR><TH>Last name:</TH><TD><INPUT TYPE="text" NAME="message"></TD></TR>
</TABLE>

<INPUT TYPE=hidden NAME="action" VALUE="search_last_name">	
<input type=hidden name="user" value={user}>
<input type=hidden name="session" value={session}>
<INPUT TYPE=submit VALUE="Submit">
</FORM>
<br>
<a href="login.cgi?action=return&user={user}&session={session}">Finish stalking</a>
</BODY>
</HTML>
		"""
	print_html_content_type()
	print(html.format(user=user,session=s))


###################################################################

def choose_friend_circle_form(form):
	user=form["user"].value
	s=form["session"].value
	html="""
		<HTML>
<HEAD>
<TITLE>Info Form</TITLE>
<!-- Bootstrap core CSS -->
    <link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">
</HEAD>

<BODY background="bg.jpg">

<center><H2 style="text-align: center; color:white">Choose or Create a Friend Circle</H2></center>

<TABLE align=center>
<FORM METHOD=post ACTION="login.cgi">
<TR><TH>Create a new circle</TH><TD><INPUT TYPE="text" NAME="message"></TD></TR>
</TABLE>
	<div style="text-align: center">
		<INPUT TYPE=hidden NAME="action" VALUE="search_last_name">	
		<input type=hidden name="user" value={user}>
		<input type=hidden name="session" value={session}>
		<INPUT TYPE=submit VALUE="Create">
	</div>
	<br><br>
	<div style="text-align: center">
		<a style="text-align: center; color:white"  class="btn btn-lg btn-primary" href="login.cgi?action=manage_friend_circle_form&user={user}&session={session}">Manage Friend Circle</a>
	</div>
</FORM>
<br>

</BODY>
</HTML>
		"""
	print_html_content_type()
	print(html)


###################################################################

def manage_friend_circle_form(form):
	user=form["user"].value
	s=form["session"].value
	html="""
		<HTML>
<head>
<!-- Bootstrap core CSS -->
    <link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">
<meta http-equiv="Content-Type" content="text/HTML; charset=iso-8859-1" />
<title>Add Option Items </title>
<script type="text/javaScript">
	function addNewListItem(){
		var htmlSelect=document.getElementById('selectYear');
		var optionValue=document.getElementById('txtYearValue');

		if(optionValue.value==''){
			alert('please enter option value');
			optionValue.focus();
			return false;
		}
		if(isOptionAlreadyExist(htmlSelect,optionValue.value)){
			alert('Option value already exists');
			optionValue.focus();
			return false;
		}
		if(isOptionAlreadyExist(htmlSelect,optionValue.value)){
			alert('value already exists');
			optionValue.focus();
			return false;
		}
		var selectBoxOption = document.createElement("option");
		selectBoxOption.value = optionValue.value;
		selectBoxOption.text = optionValue.value;
		htmlSelect.add(selectBoxOption, null); 
		alert("Option has been added successfully");
		return true;

	}
	function isOptionAlreadyExist(listBox,value){
		var exists=false;
		for(var x=0;x<listBox.options.length;x++){
			if(listBox.options[x].value==value || listBox.options[x].text==value){ 
			exists=true;
			break;
			}
		}
		return exists;
	}
	function removeListItem(){
		var htmlSelect=document.getElementById('selectYear');

		if(htmlSelect.options.length==0){
			alert('You have removed all options');
			return false;
		}
		var optionToRemove=htmlSelect.options.selectedIndex;
		htmlSelect.remove(optionToRemove);
		alert('The selected option has been removed successfully');
		return true;
	}
</script>
</head>

<body background="bg.jpg">
<center><H2 style="text-align: center; color:white">Manage friends in the circle</H2></center>
<table align="center">
<tr>
<td style="color:white">Existing friends in the circle</td>
<td align="left"><select name="selectYear" id="selectYear">
<option value="John">John</option>
<option value="Ken">Ken</option>
<option value="Sarah">Sarah</option>
<option value="Dennis">Dennis</option>
<option value="Peter">Peter</option>
</select></td>
</tr>
<td align="left"><input name="btnRemoveItem" type="button" id="btnRemoveItem" value="Remove Friend" onClick="javaScript:removeListItem();" /></td>
</table>


<br><br>
<table align="center">
<tr>
<td style="color:white" align="right">Friend's name</td>
<td align="left"><input name="txtYearValue" type="text" id="txtYearValue" /></td>
</tr>
<tr>
</tr>
<tr>
<td align="left">&nbsp;</td>
<td align="left"><input name="btnAddItem" type="button" id="btnAddItem" value="Add Friend" onclick="javaScript:addNewListItem();" /></td>

</tr>
</table>

<br>
<div style="text-align: center">
	<INPUT style="text-align: center" class="btn btn-lg btn-primary" TYPE=submit VALUE="Submit">
</div>

</body>
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
	<head color>
	<title>MyLink: Feed</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="refresh" content="8;url=login.cgi?action=show_feed&user={user}&session={session}">
	<link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">
	<script src="//code.jquery.com/jquery-2.1.0.min.js"></script>
    </head>

	<body background="bg.jpg">
	<header class="navbar navbar-default navbar-static-top">
  <div class="container">
    <nav class="" role="navigation">
      <!-- Brand and toggle get grouped for better mobile display -->
      <div class="navbar-header">
        <a class="navbar-brand" href="#"><strong>MyLink</strong></a>
      </div>
      <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
        <ul class="nav navbar-nav navbar-right">
          <li class="dropdown">
                <a href="#" class="dropdown-toggle" data-toggle="dropdown">Menu <b class="caret"></b></a>
                <ul class="dropdown-menu">
                  <li><a href="login.cgi?action=change_password_form&user={user}&session={session}">Change Password</a></li>
                  <li><a href="login.cgi?action=upload&user={user}&session={session}">Upload Avatar</a></li>
		  <li><a href="login.cgi?action=show_feed&user={user}&session={session}">Refresh</a></li>
                  <li class="divider"></li>
                  <li><a href="login.cgi?action=return_login&user={user}&session={session}">Log out</a></li>
                </ul>
          </li>
        </ul>
      </div> <!-- /.navbar-collapse -->
    </nav>
  </div>
</header>
<div class="container">
   <div class="row">
	<div class = "col-md-4">
	  <div class="panel panel-default">
            <div class="panel-body">
              <div class="col-md-12">
		 <h5 style-"opacity: 70%">New Post</h5>
		 <form method=post action="login.cgi">
                    <textarea class="form-control" required name="message" rows="3" placeholder="What's on your mind?"></textarea>
		    <input type=hidden name="action" value="twitt">
		    <input type=hidden name="user" value={user}>
		    <input type=hidden name="session" value={session}>
		    <button class="btn btn-md btn-primary btn-block" style="margin-top: 7px" type="submit">Post</button> 
		 </form>
              </div>
            </div>
          </div>
	  <div class="panel panel-default">
            <div class="panel-body">
              <div class="col-md-12">
		 <h5 style-"opacity: 70%">Add Friends(subscribe)</h5>
		 <form method=post action="login.cgi">
                    <input type=email class="form-control" required name="message" placeholder="Username">
		    <input type=hidden name="action" value="subscribe">
		    <input type=hidden name="user" value={user}>
		    <input type=hidden name="session" value={session}>
		    <button class="btn btn-md btn-primary btn-block" style="margin-top: 7px" type="submit">Add</button> 
		 </form>
              </div>
            </div>
	 </div>
	 
	<FORM METHOD=post ACTION="login.cgi">
   	<H4> reply to twitt id: </H4>
	<INPUT TYPE=text name="id">
	<H4> content: </H4>
	<INPUT TYPE=text name="message">
	<INPUT TYPE=hidden NAME="action" VALUE="reply">
	<input type=hidden name="user" value={user}>
	<input type=hidden name="session" value={session}>
	<INPUT TYPE=submit VALUE="Reply">
	</FORM>

	<FORM METHOD=post ACTION="login.cgi">
   	<H4> retweet to twitt id: </H4>
	<INPUT TYPE=text name="message">
	<INPUT TYPE=hidden NAME="action" VALUE="retwitt">
	<input type=hidden name="user" value={user}>
	<input type=hidden name="session" value={session}>
	<INPUT TYPE=submit VALUE="retweet">
	</FORM>

	</div>
	<div class = "col-md-8">
	<div class="panel panel-default">
		<div class="panel-body">
			<div class="col-md-12">
		<ul>
		<li> <a href="login.cgi?action=search_last_name_form&user={user}&session={session}">Search Users</a>
		<li> <a href="login.cgi?action=choose_friend_circle_form&user={user}&session={session}">Manage Friend Circle</a>
		</ul>
		<h3> Latest Twitts </h3>
	<div id = content>
		
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
				if ((twit[2]==target[2]) and (twit[4]==0)):	
					user=twit[2]		
					picturepath='../images/user1/'+user+'.jpg'
					print '<div style="width:50px;height:50px;overflow:hidden">'
					print('<image src="'+picturepath+'" style="max-width: 100%"></div>')
					print '<div>' 
					print str(twit[1])+ " </div>"	
					print '<div style="color : #337ab7">' 
					print "Twitt id:" + str(twit[3]) + "|  Date:" + twit[0] + " | " + "id: " + twit[2] + "</div><br>"
					now=twit[3]
					for twit in data:
						if (twit[4]==now):
							picturepath='../images/user1/'+twit[2]+'.jpg'
							print '<div style="width:50px; height:50px; padding-right:50px; overflow:hidden ">'
							print('<image src="'+picturepath+'" style="max-width: 100%; position:relative; left:50px;">')	
							print ('</div>')
							print "&nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp Reply: Twitt id:  " + str(twit[3]) + "| Date:" + twit[0] + " |	" + twit[1]+ "	|	" + "id: " + twit[2] + "<br>"

	scriptee = """</div></div>	</div>
   </div>
</div>
</div></body>
	<script src="http://getbootstrap.com/dist/js/bootstrap.min.js"></script>
	<script type="text/javascript">
	/*function refreshData()
	{
	//    $('#content').load('login.cgi?action=show_feed&user={user}&session={session}');
	}

	// Execute every 5 seconds
	window.setInterval(refreshData, 5000);*/
	</script>
	</html>
	"""
	print scriptee
	

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

	user=form["user"].value
	s=form["session"].value
	# Read image

	with open(IMAGEPATH+'/user1/'+user+'.jpg', 'rb') as content_file:
	   content = content_file.read()

	# Send header and image content
	hdr = "Content-Type: image/jpeg\nContent-Length: %d\n\n" % len(content)
	print hdr+content

###############################################################################

def upload(form):
	if session.check_session(form) != "passed":
	   login_form()
	   return

	user=form["user"].value
	s=form["session"].value

	html="""
		<HTML>
		<HEAD>
			<TITLE>Upload Avatar</TITLE>
			<!-- Bootstrap core CSS -->
    		<link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">

			<!-- Custom styles for this template -->
			<link href="upload.css" rel="stylesheet">
		</HEAD>

		<BODY background="bg.jpg">
		<FORM ACTION="login.cgi" METHOD="POST" enctype="multipart/form-data">
			<input type="hidden" name="user" value="{user}">
			<input type="hidden" name="session" value="{session}">
			<input type="hidden" name="action" value="upload-pic-data">
			<div style="text-align: center; color:white">
				<H2>Choose a picture:</H2>
				
			</div>
			<div style="color : white">
				<INPUT style="" TYPE="FILE" NAME="file"  class="custom-file-input">
			</div>
			<br>
			<div style="text-align: center" >
				<input class="btn btn-lg btn-primary" type="submit" value="Submit">
				<br>
				<br>
				<a href="login.cgi?action=return&user={user}&session={session}" style="text-align: center; color:white">Return</a>
			</div>
			</form>
		</BODY>
		</HTML>
	"""
	print_html_content_type()
	print(html.format(user=user,session=s))

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
		
		open(IMAGEPATH+'/user1/'+user+'.jpg', 'wb').write(fileInfo.file.read())
		image_url="login.cgi?action=show_image&user={user}&session={session}".format(user=user,session=s)
		print_html_content_type()
		print ('<H2>The picture ' + fileName + ' was uploaded successfully</H2>')
		print('<image src="'+image_url+'">')
		print ('<a href="login.cgi?action=return&user={user}&session={session}">Return</a>'.format(user=user,session=s))
	else:
		message = 'No file was uploaded'

def print_html_content_type():
	# Required header that tells the browser how to render the HTML.
	print("Content-Type: text/html\n\n")

def validate(username,password):
	if len(username)==0 or len(password)==0 :
		return 0
	if username.find('"')!=-1 or username.find("'")!=-1 or password.find('"')!=-1 or password.find("'")!=-1 or username.find(" ")!=-1 or password.find(" ")!=-1:
		return 0
	return 1
 
def validate_tweet(username):
	if len(username)==0:
		return 0
	if username.find('<')!=-1 or username.find(">")!=-1 :
		return 0
	return 1
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
				if form["email"]==None or form["password"]==None:
					login_form();
					print("<H3><font color=\"red\">Input something</font></H3>")
				else:				
					username=form["email"].value
					password=form["password"].value
					if validate(username,password)==0:
					   login_form()
					   print("<H3><font color=\"red\">Invalid email/password (are you trying to inject our sql you bitch?)</font></H3>")
					elif check_password(username, encrypt(password))=="passed":
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
					t = (username,first_name,last_name,encrypt(password))
					c.execute("INSERT INTO users VALUES (?,?,?,?);",t)
				with conn:
					c = conn.cursor()
					t = (username,username)
					c.execute('INSERT INTO subscribe(owner,target) VALUES (?,?)', t)
				login_form()
		elif (action == "change_password_form"):
			change_password_form(form["user"].value,form["session"].value)
		elif (action == "change_password"):
			newpassword=form["password"].value
			conn = sqlite3.connect(DATABASE)
			with conn:
				c = conn.cursor()
				owner = form["user"].value
				params = (encrypt(newpassword),owner)				
				c.execute('UPDATE users SET password=? WHERE email=?', params)
			login_form()
		elif (action == "new-album"):
			new_album(form)
		elif (action == "upload"):
			upload(form)
		elif (action == "show_image"):
			show_image(form)
		elif action == "upload-pic-data":
			upload_pic_data(form)
		elif action == "show_feed":
			display_admin_options(form["user"].value, form["session"].value)
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
				if (validate_tweet(msg)!=0):
					now = time.strftime('%Y-%m-%d %H:%M:%S')
					conn = sqlite3.connect(DATABASE)
					with conn:
						c = conn.cursor()
						t = (now,msg,form["user"].value,0)
						c.execute("INSERT INTO twitts(time,msg,owner,parent) VALUES (?,?,?,?)",t)
					display_admin_options(form["user"].value, form["session"].value)
				else:
					display_admin_options(form["user"].value, form["session"].value)
					print("<H3><font color=\"red\">HAHAHA FUCK YOU HACKER</font></H3>")

		elif action == "retwitt":
			if "message" in form:		
				msg = form["message"].value
				now = time.strftime('%Y-%m-%d %H:%M:%S')
				conn = sqlite3.connect(DATABASE)
				with conn:
					c = conn.cursor()
					c.execute("SELECT * FROM twitts WHERE id=?",(msg,))
					row=c.fetchone()
					t=(now,'RT: '+row[1]+'@'+row[2],form["user"].value,0)
					c.execute("INSERT INTO twitts(time,msg,owner,parent) VALUES (?,?,?,?)",t)
				display_admin_options(form["user"].value, form["session"].value)

		elif action == "reply":
			if "message" in form:		
				msg = form["message"].value
				parent = form["id"].value
				now = time.strftime('%Y-%m-%d %H:%M:%S')
				conn = sqlite3.connect(DATABASE)
				with conn:
					c = conn.cursor()
					t = (now,msg,form["user"].value,parent)
					c.execute("INSERT INTO twitts(time,msg,owner,parent) VALUES (?,?,?,?)",t)
				display_admin_options(form["user"].value, form["session"].value)

		elif action == "search_last_name_form":
			search_last_name_form(form)
		elif action == "choose_friend_circle_form":
			choose_friend_circle_form(form)
		elif action == "manage_friend_circle_form":
			manage_friend_circle_form(form)
		elif action == "search_last_name":
			conn = sqlite3.connect(DATABASE)
			msg = form["message"].value
			if len(msg)!=0:
				with conn:
					c = conn.cursor()					
					c.execute("SELECT * FROM USERS WHERE last_name=?",(msg,))
					row = c.fetchall()			
				search_last_name_form(form)
				print('<br>')			
				for data in row:
					print('email: '+ data[0]+' first name: '+data[1]+' last name: '+data[2]+'<br>')
			else:
				search_last_name_form(form)
				print('<br> It is empty')
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
