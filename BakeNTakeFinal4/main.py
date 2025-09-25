from flask import Flask
from flask import request
from flask import render_template, make_response
#from flask import url_for

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import uuid
import csv
#import json
from os.path import exists
from datetime import date, datetime
#import traceback
import re
import random
from collections import OrderedDict

app = Flask(__name__)

#nlp = spacy.load("en_core_web_sm")

################################################################
#username|password|firstname|lastname|gender|age|email|address|verificationcode|likes|lastlogin|currenttoken|currentsessionid|orders

user_list_of_dict = []
userfilename = "accounts/allusers.txt"
if exists(userfilename) == True:
  with open(userfilename, 'r') as file:
    for linedict in csv.DictReader(file, delimiter='|'):
      user_list_of_dict.append(linedict)

thisuser = None
sessionidinfile = ''
tokeninfile = ''
###############################################################

#chatbot=ChatBot('BakeNTake')
#trainer = ChatterBotCorpusTrainer(chatbot)
#trainer.train("chatterbot.corpus.english.greetings",
#              "chatterbot.corpus.english.conversations" )


##### HOME PAGE ###############################################
@app.route('/', methods=['GET'])
def index():
  #return 'Hello from Flask!'

  modalscripthtml = """
  <script>
  $(document).ready(function()
  {
    $("#myModal").modal('show');
  });
  </script>
  """

  if request.method == 'GET':
    style = request.args.get("style")
    if style == 're':
      modalscripthtml = "<script></script>"

  contenthtml = """
   <div class="hero_area">
    <!-- slider section -->
    <section class="slider_section position-relative">
      <div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel">
        <ol class="carousel-indicators">
          <li data-target="#carouselExampleIndicators" data-slide-to="0" class="active"></li>
          <li data-target="#carouselExampleIndicators" data-slide-to="1"></li>
          <li data-target="#carouselExampleIndicators" data-slide-to="2"></li>
        </ol>
        
        <div class="carousel-inner">
          
          <div class="carousel-item active">
            <div class="container">
              <div class="row">
                <div class="col-md-4">
                  <div class="img-box" style="margin-top:30px">
                    <img src="/static/images/2_2.jpg" alt="">
                  </div>
                </div>
                <div class="col-md-8">
                  <div class="detail-box">
                    <h1>
                      Welcome to  <br>
                      <span>
                        Our low sugar bakery
                      </span>

                    </h1>
                    <p style="font-size:1rem;color:#ffffff;font-weight:300"><b>
                      We present to you our low sugar bakery: Bake N' Take. We serve a variety of products starting from mouth-watering cup-cakes to 
                      donuts to muffins to name a few. Each of these items is carefully baked with low-sugar ingredients and we always
                      keep in mind that finally our product compares by 70% or even less sugar than the average market counterpart. Please place an
                      order and judge yourself.</b>
                    </p>
                    <div>
                      <button class=modalbutton onclick="window.location.href = '/order'" title="Order">Order</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="carousel-item">
            <div class="container">
              <div class="row">
                <div class="col-md-4">
                  <div class="img-box" style="margin-top:30px">
                    <img src="/static/images/3_3.jpg" alt="">
                  </div>
                </div>
                <div class="col-md-8">
                  <div class="detail-box">
                    <h1>
                      We bake with <br>
                      <span>
                        Your health in our mind
                      </span>

                    </h1>
                     <p style="font-size:1rem;color:#ffffff;font-weight:300"><b>
                      We use the best ingredient to bake our products and at the same time use low sugar ingredients to make sure it is both healthy
                      and delicious. This is not very easy task. We always have to keep in mind to reduce sugar and also make our items enjoyable and delicious. 
                      We have to strike a good balance to 
                      keep ourselves in business as well as keep your health in our mind. Check out the menu and see the sugar ratings.</b>
                    </p>
                    <div>
                       <button class=modalbutton onclick="window.location.href = '/order'" title="Order">Order</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="carousel-item">
            <div class="container">
              <div class="row">
                <div class="col-md-4">
                  <div class="img-box" style="margin-top:30px">
                    <img src="/static/images/1_1.jpg" alt="">
                  </div>
                </div>
                <div class="col-md-8">
                  <div class="detail-box">
                    <h1>
                      We help you <br>
                      <span>
                        Take control of your life
                      </span>

                    </h1>
                    <p style="font-size:1rem;color:#ffffff;font-weight:300"><b>
                      In the beginning of your order process we let you decide how much sugar you plan to intake. This is where you set your health goal. Based on that
                      we keep an eye on the items you are adding into the cart. We remind you of your health goal along the way and if you go over it then we 
                      show warning. This is our way of letting you take control and at the same time be there as a friend to assist you.</b>
                    </p>
                    <div>
                      <button class=modalbutton onclick="window.location.href = '/order'" title="Order">Order</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div> 
       <!-- Commmenting Next and Prev button
        <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
          <span class="sr-only">Next</span>
        </a>

        <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
          <span class="sr-only">Previous</span>
        </a>-->
       
      </div>


    </section>
    <!-- end slider section -->
  </div>

  <section class="about_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
          About Us
        </h2>
      </div>
      <br/>      
      <table border="0" cellpadding="10" cellspacing="0" width="100%">
      <tr><td valign="top" align=center>
        <img src="/static/images/baker.jpg" alt="" width="60%" style="border-radius:10px">
      </td><td valign="top">
      <div class="detail-box">
        <p align="left"> 
          Welcome to our bakery, where every bite is a little slice of heaven. Starting a bakery can be a rewarding and fulfilling endeavor, but it also requires significant hard work, dedication, and planning. Our business aims to create unique flavors that customers can enjoy! We want you to feel delighted after tasting our baked goods. We also want to inspire bakers worldwide to follow their passions and bake healthy and tasty.</p>
        <p align="left">
          We are a team of passionate bakers who believe that great food starts with the best ingredients and a lot of love. Our mission is to create delicious baked goods low in sugar that satisfy both the stomach and the soul.</p>
        <div class="d-flex justify-content-center">
          <button class=modalbutton onclick="window.location.href = '/about'" title="About Us">Read More</button>
        </div>
      </div>
      </td></tr>
     </table>
    </div>
  </section>

  <section class="discount_section">
    <div class="container-fluid">
      <div class="row">
        <div class="col-lg-3 col-md-5 offset-md-2">
          <div class="detail-box">
            <h2 style="text-transform:none">
              You get <br>
              any bakery item <br>
              with at least 
              <span>
                70% less sugar
              </span>

            </h2>
            <p style="font-size: 1rem;color:#ffffff;font-weight:300">
              We use high quality low-sugar ingredient in all our baking. We do not compromise on taste though.
            </p>
            <div>
              <button class=modalbutton onclick="window.location.href = '/menu'" title="Check The Menu">Check The Menu</button>
            </div>
          </div>
        </div>
        <div class="col-lg-7 col-md-5">
          <div class="img-box">
            <img src="/static/images/0.jpg" alt="">
          </div>
        </div>
      </div>
    </div>
  </section>

  
  <section class="about_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
        Sugar Bar : A new Concept        
        </h2>
      </div>
      <br/>      
      <table border="0" cellpadding="20" cellspacing="0" width="100%">
      <tr><td valign="top" align=center width=50%>
        <img src=/static/images/sugarbar.jpg width="100%" style="border-radius:10px">
      </td><td valign="top">
      <div class="detail-box">
        <p align="left">  When you start ordering, we ask you how much sugar you would like to consume today - Please
        see on the left how it will look like. <br/><br/>
        And as you set your own limit and take charge of your health, we will also be there
        as a friend to show you your "SugarBar" (sugar progress bar) which will be dynamically
        show you how close you are towards your goal. This will look something like below. </p>
        <br/><br/>
        <table width=50%><tr><td>
          SugarBar:  &nbsp; &nbsp; &nbsp; &nbsp;  98%
          <progress max="100" value="98" class="html5" style="height:20px">
          <div class="progress-bar"><span style="width: 98%">98%</span</div>
          </progress>
        </td></tr></table>
        
        <br/><br/>
        
      <p align="left">    When you see it is close to 100% that means you are closing on your own set goal and it is
        probably the time to stop adding any more item. <br/><br/>

        We are here in this business, more as a friend, who helps you with your health goal rather than
        just making a profit. </p>
      </div>
      </td></tr>
     </table>
    </div>
  </section>

  """
  scripthtml = """
   <script type="text/javascript" src="/static/js/jquery-3.4.1.min.js"></script>
  <script type="text/javascript" src="/static/js/bootstrap.js"></script>
  <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.2.1/owl.carousel.min.js">
  </script>
  <script type="text/javascript">
    $(".owl-carousel").owlCarousel({
      loop: true,
      margin: 10,
      nav: true,
      navText: [],
      autoplay: true,
      responsive: {
        0: {
          items: 1
        },
        600: {
          items: 2
        },
        1000: {
          items: 4
        }
      }
    });
  </script>
  <script type="text/javascript">
    $(".owl-2").owlCarousel({
      loop: true,
      margin: 10,
      nav: true,
      navText: [],
      autoplay: true,

      responsive: {
        0: {
          items: 1
        },
        600: {
          items: 2
        },
        1000: {
          items: 4
        }
      }
    });
  </script>
  <script>

    // When the user scrolls the page, execute myFunction
window.onscroll = function() {myFunction()};

// Get the header
var header = document.getElementById("myHeader");

// Get the offset position of the navbar
var sticky = header.offsetTop;

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.pageYOffset > sticky) {
    header.classList.add("sticky");
  } else {
    header.classList.remove("sticky");
  }
}
  </script>

  """

  messages = [("  New Item Introduced : Classic Brownies", """
    
    <p style="text-align: justify;"> We have introduced <b>Classic Brownies</b> with only 15gm of sugar, much lower than the market counter 
    part and good for 2 people.<br/><br/>
    <a href="/menu?iid=bt0005"><img style="float:left; margin-right:10px; border-radius:5px;" src="/static/images/5-brownies.jpg" width=200px></a> <br/>
    To see more information please <br/> <br/> <a href="/menu?iid=bt0005"><button class=modalbutton>Click Here</button></a> </p>
    
    """),
              ("  Subscribe", """
     Please subscribe to our newsletter to get up-to-date news. <br/>
     <form action="/newsletter" method="POST">
              <input type="text" placeholder="Enter Your email" name="email">
              <div class="d-flex justify-content-start  mt-3">
                <button class=modalbutton onclick=this.form.submit()>Subscribe</button>
              </div>
            </form>
     """),
              ("  Check Out Our Menu", """
    Please check out our menu here for the full list of our baked goodness.<br/><br/>
    <a href = "/menu"><button class=modalbutton> Menu </button> </a>
     """)]

  message = messages[0]  # random.randint(0, 2)]

  modaldivhtml = """  
  <div id="myModal" class="modal fade">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <section style="width:100%;background-color:#1a0503;align:center;padding:15px;">
                <img src="/static/images/logo-bakery.png" height=52px width=227px>&nbsp;
                <span style="color:#ffffff; text-align:right;font-size:24px;vertical-align:middle">
                <button type="button" class="close" data-dismiss="modal" style="color:white">&times;</button>
                </span>
                <h5 class="modal-title" style="color:#ffffff;font-size:24px;vertical-align:middle;margin-left:15px;">Important Announcement</h5>
                
                </section>
                
            </div>
            <div class="modal-body">
                <p><b> {0} </b></p>
                <table border=0 cellpadding=5 cellspacing=5 width=100%>
                <tr><td> {1} </td> </tr>
                <tr><td> <hr/>- Bake N' Take News Team! </td></tr>
                </table>
            </div>
        </div>
    </div>
</div>
  
  """.format(message[0], message[1])

  return render_template('template.html',
                         contenthtml=contenthtml,
                         scripthtml=scripthtml,
                         useraccounthtml=GetUserAccountHTML(None, None),
                         modalscript=modalscripthtml,
                         modaldivhtml=modaldivhtml)
  #return render_template('index.html')


###### COUPONS ################################################
@app.route('/coupon', methods=['GET', 'POST'])
def coupon():

  return


###############################################################
def RefreshUsers():
  global user_list_of_dict
  user_list_of_dict = []
  userfilename = "accounts/allusers.txt"
  if exists(userfilename) == True:
    with open(userfilename, 'r') as file:
      for linedict in csv.DictReader(file, delimiter='|'):
        user_list_of_dict.append(linedict)


###############################################################
def GetUserAccountName(userid, ctoken):
  # if userid or ctoken not given then read from cookie
  if (userid == None) | (ctoken == None):
    #print("1")
    userid = ''
    if 'user' in request.cookies:
      userid = request.cookies.get("user")
    ctoken = ''
    if 'tokn' in request.cookies:
      ctoken = request.cookies.get("tokn")
  if (userid != '') & (ctoken != ''):
    if VerifyCurrentUserToken(userid, ctoken) == True:
      return userid

  return "Guest"


###############################################################
def GetUserAccountEmail(userid, ctoken):
  # if userid or ctoken not given then read from cookie
  if (userid == None) | (ctoken == None):
    #print("1")
    userid = ''
    email = ''
    if 'user' in request.cookies:
      userid = request.cookies.get("user")
    ctoken = ''
    if 'tokn' in request.cookies:
      ctoken = request.cookies.get("tokn")
  if (userid != '') & (ctoken != ''):
    if VerifyCurrentUserToken(userid, ctoken) == True:
      if (len(user_list_of_dict) > 0):
        for line in user_list_of_dict:
          if userid == line["username"]:
            email = line["email"]
        return email

  return ""


###############################################################
def GetUserAccountHTML(userid, ctoken):
  userhtml = """
  <div class="dropdown">
      <a class=navbar-user href="/login">
       <img src="/static/images/user-not-logged.png" alt="" height="50px" width="50px"><br/>
       Guest
      </a>
      <div class="dropdown-content">
        <a href="/login">Login</a>
        <a href="/signup">Signup</a>
  </div>
  </div>    
  """
  # if userid or ctoken not given then read from cookie
  if (userid == None) | (ctoken == None):
    print("1")
    userid = ''
    if 'user' in request.cookies:
      userid = request.cookies.get("user")
    ctoken = ''
    if 'tokn' in request.cookies:
      ctoken = request.cookies.get("tokn")

  print(userid)
  print(ctoken)
  if (userid != '') & (ctoken != ''):
    if VerifyCurrentUserToken(userid, ctoken) == True:
      userhtml = """
      <div class="dropdown">
        <a class=navbar-user href="/account">
          <img src="/static/images/user-logged.png" alt="" height="50px" width="50px"><br/>
          {0}
        </a>
        <div class="dropdown-content">
          <a href="/account">My Profile</a>
          <a href="/account?w=o">My Past Orders</a>
          <a href="/logout?conf=y">Logout</a>
        </div>
      </div>    
      """.format(userid)
  return userhtml


###############################################################
def VerifyCurrentUserToken(user, cookietokn):
  #read
  global tokeninfile
  global thisuser
  global sessionidinfile

  match = False
  if (len(user_list_of_dict) > 0):
    for line in user_list_of_dict:
      if user == line["username"]:
        #print(user)
        #print( "VerifyCurrentUserToken " + line["currenttoken"] + "== "+ cookietokn)
        if (line["currenttoken"] == cookietokn):
          s = line["currentsessionid"]
          if s == 'NA':
            s = ''
          if len(s) > 0:
            (dt, sm, us, em, st) = GetSessionInfo(s)
            if dt != None:
              if st == '':  #not complete
                sessionidinfile = s
              else:
                sessionidinfile = ''
          tokeninfile = line["currenttoken"]
          if tokeninfile == 'NA':
            tokeninfile = ''
          thisuser = line
          match = True
  return match


###############################################################
def UpdateTokenForUser(user, token):
  if (len(user_list_of_dict) > 0):
    for line in user_list_of_dict:
      if user == line["username"]:
        line["currenttoken"] = token
  return user_list_of_dict


def UpdateCurrentSessionIdForUser(user, sessionid):
  if (len(user_list_of_dict) > 0):
    for line in user_list_of_dict:
      if user == line["username"]:
        line["currentsessionid"] = sessionid
  return user_list_of_dict


###############################################################
def SaveAllUsers():
  try:
    with open(userfilename, 'w', newline='') as file:
      columns = [
        "username", "password", "firstname", "lastname", "gender", "age",
        "email", "address", "verificationcode", "likes", "lastlogin",
        "currenttoken", "currentsessionid", "orders"
      ]
      writer = csv.DictWriter(file, fieldnames=columns, delimiter='|')
      writer.writeheader()
      for linedict in user_list_of_dict:
        writer.writerow(linedict)
  except:
    return False
  return True


###############################################################
def VerifyCurrentUserWithPassword(user, pwds):
  #read
  realpass = ''
  ret = False
  global tokeninfile
  global thisuser
  global sessionidinfile

  if (len(user_list_of_dict) > 0):
    for line in user_list_of_dict:
      print(line)
      if user == line["username"]:
        #print("user in")
        realpass = line["password"]
        #print("pas=" + realpass)
        if realpass == pwds:
          #print("pass in")
          s = line["currentsessionid"]
          if s == 'NA':
            s = ''
          if len(s) > 0:
            (dt, sm, us, em, st) = GetSessionInfo(s)
            if dt != None:
              if st == '':  #not complete
                sessionidinfile = s
              else:
                sessionidinfile = ''
          tokeninfile = line["currenttoken"]
          if tokeninfile == 'NA':
            tokeninfile = ''
          thisuser = line
          #print(thisuser)
          ret = True
          break
  return ret


###############################################################
def ForgotUsernameFormHTML():
  html = """
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td align=center style="border-bottom: solid 1px;"> 
        <div class="acctab_h">
          <a href="/forgot?f=u" class='b'>Forgot Username </a>
          <a href="/forgot?f=p" >Forgot Password</a>
        </div>
      </td></tr>
      <tr><td align=center>
        <form action=/forgot method=POST><input type=hidden name=what value=forgotuser>
        <table border=0 cellpadding=5 cellspacing=5 width=50%>
        <tr><td colspan=2 align=center><b>Forgot Username Form</b></td></tr>
        <tr><td align=right width=40%> <b>Please Enter Your Email Address:</b> </td><td><input type=text size=30 name=email></td></tr>
        <tr><td>&nbsp; </td><td><button class="cartbuttonbig" onclick=this.form.submit()> Send Username </button></td></tr>
        </table></form>
      </td></tr>
      </table>
  """
  return html


###############################################################
def ForgotPasswordFormHTML():
  html = """
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td align=center style="border-bottom: solid 1px;"> 
        <div class="acctab_h">
          <a href="/forgot?f=u" >Forgot Username </a>
          <a href="/forgot?f=p" class='b'>Forgot Password</a>
        </div>
      </td></tr>
      <tr><td align=center>
        <form action=/forgot method=POST><input type=hidden name=what value=forgotpass>
        <table border=0 cellpadding=5 cellspacing=5 width=50%>
        <tr><td colspan=2 align=center><b>Forgot Password Form</b></td></tr>
        <tr><td align=right width=40%> <b>Please Enter Your Username:</b> </td><td><input type=text size=30 name=user></td></tr>
        <tr><td>&nbsp; </td><td><button class="cartbuttonbig" onclick=this.form.submit()> Send Password </button></td></tr>
        </table></form>
      </td></tr>
      </table>
  """
  return html


def LoginFormHTML():
  html = """
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td align=center style="border-bottom: solid 1px;"> 
        <div class="acctab_h">
          <a href="/login" class='b'>Log In </a>
          <a href="/signup" >Sign Up</a>
        </div>
      </td></tr>
      <tr><td align=center>
        <form action=/login method=POST>
        <table border=0 cellpadding=5 cellspacing=5 width=50%>
        <tr><td colspan=2 align=center><b>Login Form </b></td></tr>
        <tr><td align=right width=40%> <b>Username:</b> </td><td><input type=text size=30 name=user></td></tr>
        <tr><td align=right> <b>Password:</b> </td><td><input type=password size=30 name=pwds></td></tr>
        <tr><td>&nbsp; </td><td><button class="cartbuttonbig" onclick=this.form.submit()> Login </button></td></tr>
        </table></form>
      </td></tr>
      </table>
  """
  return html


###############################################################
def SignupFormHTML():
  html = """
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td align=center style="border-bottom: solid 1px;"> 
        <div class="acctab_h">
          <a href="/login" >Log In </a>
          <a href="/signup" class='b'>Sign Up</a>
        </div>
      </td></tr>
      <tr><td align=center>
        <form action=/signup method=POST>
        <table border=0 cellpadding=5 cellspacing=5 width=50%>
        <tr><td colspan=2 align=center><b>Signup Form </b></td></tr>
        <tr><td align=right width=40%> <b>* Desired Username:</b> </td><td><input type=text size=30 name=user required></td></tr>
        <tr><td align=right> <b>* Password:</b> </td><td><input type=password size=30 name=pwds required></td></tr>
        <tr><td align=right> <b>* Repeat Password:</b> </td><td><input type=password size=30 name=pwds2 required></td></tr>
        <tr><td align=right> <b>First Name:</b> </td><td><input type=text size=30 name=fname></td></tr>
        <tr><td align=right> <b>Last Name:</b> </td><td><input type=text size=30 name=lname></td></tr>
        <tr><td align=right> <b>Gender:</b> </td><td> <select id="gender" name="gender">
                                                      <option value="male">Male</option>
                                                      <option value="female">Female</option>
                                                      <option value="other">Other</option>
                                                    </select>  </td></tr>
        <tr><td align=right> <b>Age:</b> </td><td><input type=number min=10 step="1"/></td></tr>
        <tr><td align=right> <b>* Email:</b> </td><td><input type=email size=30 name=email required></td></tr>
        <tr><td align=right> <b>Address:</b> </td><td><input type=text size=30 name=address></td></tr>
        <tr><td>&nbsp; </td><td><button class="cartbuttonbig" onclick=this.form.submit()> Signup </button></td></tr>
        </table></form>
      </td></tr>
      </table>
  """
  return html


######  LOGOUT PAGE ##############################################
@app.route('/logout', methods=['GET', 'POST'])
def logout():
  confirm = ''
  if request.method == 'GET':
    confirm = request.args.get("conf")
    if confirm == 'y':
      html = """<section class="about_section layout_padding">
          <div class="container">
            <div class="custom_heading-container ">
              <h2>
              You have been logged out
              </h2>
            </div>
            <br/>
            <table border=0 cellpadding=5 cellspacing=5 width=100%>
            <tr><td colspan=2 style="border-top: solid 1px;"></tr>
            </table>
            <br/>
            <img src="/static/images/cookie.png" width=150px>
            <br/><br/>
            Please visit again<br/><br/>
          """
      html += """
              </div>
            </section>
            """

      resp = make_response(
        render_template('template.html',
                        contenthtml=html,
                        useraccounthtml=GetUserAccountHTML('', '')))
      resp.set_cookie("user", '', max_age=0)  #30 minutes max
      resp.set_cookie("tokn", '', max_age=0)
      resp.set_cookie("sessid", '', max_age=0)
    return resp
  return


def AllItemsOfAnOrder(orderid):
  sessionid = orderid
  item_listdict = readitems()
  filename = "sessions/{0}.txt".format(sessionid)
  retdict = {}
  with open(filename, 'r') as file:
    for linedict in csv.DictReader(file, delimiter='|'):
      itemid = linedict["itemid"]
      qty = int(linedict["quanti"])
      for item in item_listdict:
        if itemid == item["itemid"]:
          iname = item["itemname"]
          if iname in retdict:
            retdict[iname] = retdict[iname] + qty
          else:
            retdict[iname] = qty
  return retdict


def AllDetailsOfAnOrder(orderid):
  sessionid = orderid
  (dt, sm, us, em, st) = GetSessionInfo(sessionid)
  #print(dt, sm, us, em, st)
  conthtml = ''
  if st == '':
    st = "<font color=red>Not Complete (You did not submit the order)</font>"
    conthtml = """
    <tr><td valign=top align=right><b>Continue: </b></td><td align=left><font color=red>You had started this order in the past but never completed/submit it. To continue with this order<br/>
    <a href=/order?sessid={0}&cartup=Started&suglim={1}> <button class="cartbuttonbig"> Please Click Here </button> </a>
    <br/></td></tr>
    """.format(orderid, sm)
  item_listdict = readitems()
  flav_listdict = readflavors()
  topp_listdict = readtoppings()
  type_listdict = readtypes()
  (currentsugar, currentcalor, currentcosts, carthtml) = ShowCartHTML(item_listdict, flav_listdict, topp_listdict, type_listdict,\
                                                                          "NA", "NA","NA","NA", 0, sessionid, sm, "SendEmail", [] )
  html = """<table border=0 cellpadding=5 width=90%>
  <tr><td align=right width=120px><b>Order Id: </b></td><td align=left>{0}</td></tr>
  <tr><td align=right><b>Date time: </b></td><td align=left>{1}</td></tr>
  <tr><td align=right><b>Status: </b></td><td align=left>{2}</td></tr>
  {4}
  <tr><td valign=top align=right><b>Details:</b></td><td align=left>{3}</td></tr>
  </table>
  """.format(orderid, dt, st, carthtml, conthtml)
  return (currentsugar, currentcalor, currentcosts, html)


##### ACCOUNT PAGE ###############################################
@app.route('/account', methods=['GET', 'POST'])
def account():
  html = """<section class="about_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
        User Account Details  
        </h2>
      </div>
      <br/>
    """

  userid = ''
  if 'user' in request.cookies:
    userid = request.cookies.get("user")
  ctoken = ''
  if 'tokn' in request.cookies:
    ctoken = request.cookies.get("tokn")

  success = False
  status = ''
  if (userid != '') & (ctoken != ''):
    if VerifyCurrentUserToken(userid, ctoken) == True:

      #read the password
      success = True
      if request.method == 'GET':
        which = request.args.get("w")
        ordid = request.args.get("ord")
      ec_ = ''
      ec_o = ''
      ec_a = ''
      if which == 'o':
        ec_o = "class='b'"
      elif which == 'a':
        ec_a = "class='b'"
      else:
        ec_ = "class='b'"
      html += """
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td align=center style="border-bottom: solid 1px;"> 
        <div class="acctab_h">
          <a href="/account" {0}>Account Profile</a>
          <a href="/account?w=o" {1}>Activity/Past Orders</a>
          <a href="/account?w=a" {2}>Order Data Analysis</a>
        </div>
      </td></tr>
      <tr><td>
      """.format(ec_, ec_o, ec_a)

      if which == None:
        html += """
        <table border="0" cellpadding="5" cellspacing="5" width="90%">
        <tr><td valign=top align=right width=50%><b>Username:</b> </td><td valign="top" align=left> {0} </td></tr>
        <tr><td valign=top align=right><b>First Name: </b></td><td valign="top" align=left> {1} </td></tr>
        <tr><td valign=top align=right><b>Last Name: </b></td><td valign="top" align=left> {2} </td></tr>
        <tr><td valign=top align=right><b>Email: </b></td><td valign="top" align=left> {3} </td></tr>
        <tr><td valign=top align=right><b>Address: </b></td><td valign="top" align=left> {4} </td></tr>
        
        <tr><td valign="top" align=center colspan=2> <button class="cartbuttonbig" onclick="window.location.href='/logout?conf=y';"> Logout </button> </td></tr>
        </table>   
        """.format(thisuser["username"], thisuser["firstname"],
                   thisuser["lastname"], thisuser["email"],
                   thisuser["address"])
        html += """
            </td></tr></table>
            </div>
          </section>
          """
        resp = make_response(
          render_template('template.html',
                          contenthtml=html,
                          useraccounthtml=GetUserAccountHTML(userid, ctoken)))
      elif which == 'o':
        firstordernum = 0
        orderlinkhtml = '<div class="acctab_v"><table border=0 cellspacing=2 width=100% height=100% >'
        orders = thisuser["orders"]
        if orders.startswith(","):
          orders = orders[1:]
        if (orders != None) and (orders != '') and (orders != 'NA'):
          if ',' in orders:
            orderlist = orders.split(',')
          else:
            orderlist = [orders]

          #if no order id mentioned show the first one
          if ordid == None:
            firstordernum = orderlist[0]
          else:
            firstordernum = ordid

          orddict = {}
          statdict = {}
          for ord in orderlist:
            (dt, sm, us, em, st) = GetSessionInfo(ord)
            orddict[ord] = dt
            statdict[ord] = st

          #print("orddict dict")
          #print(orddict)
          if len(orddict) > 0:
            orddict = dict(sorted(orddict.items(), key=lambda x: x[1]))
            print("statdict dict")
            print(statdict)
            for ord, dt in orddict.items():
              st = statdict[ord]
              color = " class='d'"
              if st == '':  #not complete
                st = "*"
                color = " class='c'"
              else:
                st = ''  #do not write anything

              if ord == firstordernum:
                orderlinkhtml += "<tr><td align=right><a href=/account?w=o&ord={0} class='b'>{1} {0}<br/>(On {2})</a></td></tr>".format(
                  ord, st, dt[0:10])
              else:
                orderlinkhtml += "<tr><td align=right><a href=/account?w=o&ord={0} {3}>{1} {0}<br/>(On {2})</a></td></tr>".format(
                  ord, st, dt[0:10], color)
          else:
            orderlinkhtml += "<tr><td></td></tr>"
        else:
          orderlinkhtml += "<tr><td></td></tr>"
        orderlinkhtml += "</table></div>"

        #print("firstordernum=" + firstordernum)
        firstorderhtml = ''
        if firstordernum == 0:
          firstorderhtml = "You have not yet placed or started any order in our system."
        else:
          (currentsugar, currentcalor, currentcosts,
           firstorderhtml) = AllDetailsOfAnOrder(firstordernum)
        html += """
          <table border="0" cellpadding="5" cellspacing="5" width="90%">
          <tr><td valign=top align=right width=35%><b></b></td><td valign="top" align=left style="border-bottom: solid 1px;"> <b>Order Details </b></td></tr>
          <tr><td valign=top alighn=right style="border-right: solid 1px;"> {0} </td><td valign=top> {1} </td></tr>
          <!--<tr><td valign="top" align=center colspan=2> <button class="cartbuttonbig" onclick="window.location.href='/logout?conf=y';"> Logout </button> </td></tr>-->
          </table>   
          """.format(orderlinkhtml, firstorderhtml)
        html += """
            </td></tr></table>
            </div>
          </section>
          """
        resp = make_response(
          render_template('template.html',
                          contenthtml=html,
                          useraccounthtml=GetUserAccountHTML(userid, ctoken)))
      elif which == 'a':
        orders = thisuser["orders"]
        if (orders != None) or (orders != '') or (orders != 'NA'):
          if ',' in orders:
            orderlist = orders.split(',')
          else:
            orderlist = [orders]
          orddict = {}
          statdict = {}
          sugarlimitdict = {}
          totalordersugar = {}
          totalordercalorie = {}
          totalordercosts = {}
          for ord in orderlist:
            (dt, sm, us, em, st) = GetSessionInfo(ord)
            (currentsugar, currentcalor, currentcosts,
             firstorderhtml) = AllDetailsOfAnOrder(ord)
            orddict[ord] = dt
            statdict[ord] = st
            sugarlimitdict[ord] = sm
            totalordersugar[ord] = currentsugar
            totalordercalorie[ord] = currentcalor
            totalordercosts[ord] = currentcosts
          orddict = dict(sorted(orddict.items(), key=lambda x: x[1]))

        chart = request.args.get("ch")
        if chart is None:
          chart = 'sl'
        selected = {'sl': '', 'msc': '', 'id': '', 'mcc': '', 'me': ''}
        title = {
          'sl': 'Sugar Consumption By Date',
          'msc': 'Sugar Consumption By Month',
          'id': 'Item Distribution',
          'mcc': 'Calorie Consumption By Month',
          'me': 'Bakery Expense By Month'
        }

        predescription = {
          'sl':
          """
                        We show here the your order history and how much sugar you have ordered per order. We also show the sugarlimit, either imposed by yourself
                        or our system has recommended. <br/>It will be a good thing if you have not crossed the sugar limit (because it shows your health consciousness and we 
                        reward that with a 50% off coupon). 
                        """,
          'msc':
          'Sugar consumption by month shows how much total sugar you have consumed in a month. Over time if it is going lower then it is a good sign.',
          'id':
          'Item distribution shows what kind of items you ordered how many times. This shows your preferences for our awesome bakery products.',
          'mcc':
          'Calorie consumption is also important. Here we show a monthly total of your calorie consumption from our baker products.',
          'me':
          'Your expense over the month is shown here. We encourage you to buy our awesome products but at the same time we do not hide how much you are spending.'
        }

        postdescription = {
          'sl':
          'Thank you for being a great customer. ',
          'msc':
          'Please let us know if you have any question. ',
          'id':
          'Let us see what your favorite product is. ',
          'mcc':
          'Contact us for more calorie related questions. ',
          'me':
          'Our products are not just low in sugar, they are also low in price. Hope you continue to enjoy our deliciousness. '
        }

        selected[chart] = "class='b'"
        linksrows = "<tr><td align=right><a href=/account?w=a&ch=sl {0}>{1}</a></td></tr>".format(
          selected['sl'], title['sl'])
        linksrows += "<tr><td align=right><a href=/account?w=a&ch=msc {0}>{1}</a></td></tr>".format(
          selected['msc'], title['msc'])
        #linksrows += "<tr><td align=right><a href=/account?w=a&ch=mcc {0}>{1}</a></td></tr>".format(selected['mcc'],title['mcc'])
        linksrows += "<tr><td align=right><a href=/account?w=a&ch=id {0}>{1}</a></td></tr>".format(
          selected['id'], title['id'])
        linksrows += "<tr><td align=right><a href=/account?w=a&ch=me {0}>{1}</a></td></tr>".format(
          selected['me'], title['me'])

        charttitle = title[chart]
        orderlinkhtml = '<div class="acctab_v"><table border=0 cellspacing=2 width=100% height=100% >'
        orderlinkhtml += linksrows
        orderlinkhtml += "<tr><td></td></tr>"
        orderlinkhtml += "</table></div>"
        charthtml = "<center><canvas id='chart' width='600' height='400'></canvas></center>"
        html += """
        <table border="0" cellpadding="5" cellspacing="5" width="90%">
        <tr><td valign=top align=right width=35%><b></b></td><td valign="top" align=left style="border-bottom: solid 1px;"> <b>{0} </b></td></tr>
        <tr><td valign=top align=right style="border-right: solid 1px;"> {1} </td><td valign=top align=left> <br/> {2} <br/><br/><br/> {3} 
        
        """.format(charttitle, orderlinkhtml, predescription[chart], charthtml)

        scripthtml = ''
        if chart == 'sl':
          firstordernum = 0
          goodcustomer = True

          if (orders != None) or (orders != '') or (orders != 'NA'):
            sugardata = []
            sugarlimitdata = []
            caloriedata = []
            labels = []
            chartvalmax = -1
            for ord, dt in orddict.items():
              st = statdict[ord]
              if st == '':  #not complete
                st = "*"
              else:
                st = ''  #do not write anything
                print("if float({0}) > float({1}):".format(
                  totalordersugar[ord], sugarlimitdict[ord]))
                if float(totalordersugar[ord]) > float(sugarlimitdict[ord]):
                  goodcustomer = False
                dt = "\"" + dt[0:10] + "\""
                labels.append(dt)
                #(currentsugar, currentcalor, currentcosts, firstorderhtml) = AllDetailsOfAnOrder(ord)
                sugardata.append(totalordersugar[ord])
                if totalordersugar[ord] > chartvalmax:
                  chartvalmax = totalordersugar[ord]
                sugarlimitdata.append(sugarlimitdict[ord])
                caloriedata.append(totalordercalorie[ord])

            if goodcustomer == True:
              postdescription[
                'sl'] = "Thank you for being a great customer.  You are always less than sugar limit. You have been awarded a 50% off coupon."
            else:
              postdescription[
                'sl'] = "Thank you for being a great customer. You have crossed sugarlimit in the past. Let's try to improve next time."
            labeltext = ', '.join(labels)
            datatext = ', '.join(map(str, sugardata))
            datatext2 = ', '.join(map(str, sugarlimitdata))
            #print(labeltext)
            #print(datatext)
            scripthtml = """
            <script>
                new Chart(document.getElementById('chart'), 
                {{  type : 'line',
                    data : 
                      {{
                        labels : [ {0} ],
                        datasets : [
                          {{ 
                            data : [ {1} ], 
                            label : "{3}",
                            borderColor : "#3cba9f",
                            fill : false 
                          }},
                          {{ 
                            data : [ {2} ], 
                            label : "{4}",
                            borderColor : "#e43202",
                            fill : false 
                          }},
                          
                        ] 
                      }},
                      options : 
                        {{
                          title : {{display : true, text : "{3}"}}
                        }}
                  }});
              </script>
            """.format(labeltext, datatext, datatext2, "Sugar Ordered (in gm)",
                       "Sugar Limit (in gm)",
                       "Sugar Line from Past Orders (completed orders)")
        if chart == 'msc':
          if (orders != None) or (orders != '') or (orders != 'NA'):
            sugardata = []
            sugarlimitdata = []
            caloriedata = []
            labels = []
            chartvalmax = -1
            labels = [
              'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
              'Oct', 'Nov', 'Dec'
            ]
            monthsugar = {
              1: 0,
              2: 0,
              3: 0,
              4: 0,
              5: 0,
              6: 0,
              7: 0,
              8: 0,
              9: 0,
              10: 0,
              11: 0,
              12: 0
            }
            for ord, dt in orddict.items():
              st = statdict[ord]
              if st == '':  #not complete
                st = "*"
              else:
                st = ''  #do not write anything

                dt = dt[0:10]
                month = datetime.strptime(dt,
                                          '%m/%d/%Y').month  #strftime("%B")
                monthsugar[month] = monthsugar[month] + totalordersugar[ord]

            for k, v in monthsugar.items():
              sugardata.append(v)
            #labeltext = ', '.join(labels)
            labeltext = ''
            for l in labels:
              labeltext += "'" + l + "',"
            labeltext = labeltext.rstrip()
            datatext = ', '.join(map(str, sugardata))
            #datatext2 = ', '.join(map(str, sugarlimitdata))
            #print(labeltext)
            #print(datatext)
            scripthtml = """
            <script>
                new Chart(document.getElementById('chart'), 
                {{  type : 'bar',
                    data : 
                      {{
                        labels : [ {0} ],
                        datasets : [
                          {{ 
                            data : [ {1} ], 
                            label : "{2}",
                            backgroundColor: ["#51EAEA"]
                            //borderColor : "#3cba9f",
                            //fill : false 
                          }}
                          //,
                          //{{ 
                          //  data : [ {2} ], 
                          //  label : "{4}",
                          //  borderColor : "#e43202",
                          //  fill : false 
                          //}},
                        ] 
                      }},
                      options : 
                        {{
                          title : {{display : true, text : "{3}"}}
                        }}
                  }});
              </script>
            """.format(labeltext, datatext, "Sugar Ordered (in gm)", '', '')
        if chart == 'mcc':
          if (orders != None) or (orders != '') or (orders != 'NA'):
            sugardata = []
            sugarlimitdata = []
            caloriedata = []
            labels = []
            chartvalmax = -1
            labels = [
              'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
              'Oct', 'Nov', 'Dec'
            ]
            monthcalorie = {
              1: 0,
              2: 0,
              3: 0,
              4: 0,
              5: 0,
              6: 0,
              7: 0,
              8: 0,
              9: 0,
              10: 0,
              11: 0,
              12: 0
            }
            for ord, dt in orddict.items():
              st = statdict[ord]
              if st == '':  #not complete
                st = "*"
              else:
                st = ''  #do not write anything

                dt = dt[0:10]
                month = datetime.strptime(dt,
                                          '%m/%d/%Y').month  #strftime("%B")
                monthcalorie[
                  month] = monthcalorie[month] + totalordercalorie[ord]

            for k, v in monthcalorie.items():
              caloriedata.append(v)
            #labeltext = ', '.join(labels)
            labeltext = ''
            for l in labels:
              labeltext += "'" + l + "',"
            labeltext = labeltext.rstrip()
            datatext = ', '.join(map(str, caloriedata))
            #datatext2 = ', '.join(map(str, sugarlimitdata))
            #print(labeltext)
            #print(datatext)
            scripthtml = """
            <script>
                new Chart(document.getElementById('chart'), 
                {{  type : 'bar',
                    data : 
                      {{
                        labels : [ {0} ],
                        datasets : [
                          {{ 
                            data : [ {1} ], 
                            label : "{2}",
                            backgroundColor: ["#ff9900"]
                            //borderColor : "#ff9900",
                            //fill : false 
                          }}
                          //,
                          //{{ 
                          //  data : [ {2} ], 
                          //  label : "{4}",
                          //  borderColor : "#e43202",
                          //  fill : false 
                          //}},
                        ] 
                      }},
                      options : 
                        {{
                          title : {{display : true, text : "{3}"}}
                        }}
                  }});
              </script>
            """.format(labeltext, datatext, "Calorie Consumption (in KCal)",
                       '', '')
        if chart == 'id':
          if (orders != None) and (orders != '') and (orders != 'NA'):
            itemdict = {}
            for ord, dt in orddict.items():
              st = statdict[ord]
              if st == '':  #not complete
                st = "*"
              else:
                st = ''  #do not write anything
                tempdict = AllItemsOfAnOrder(ord)
                for k, v in tempdict.items():
                  if k in itemdict:
                    itemdict[k] = itemdict[k] + v
                  else:
                    itemdict[k] = v

            datatext = ''
            labeltext = ''
            for k, v in itemdict.items():
              labeltext += "'" + k + "',"
              datatext += str(v) + ","
            labeltext = labeltext.rstrip()
            datatext = datatext.rstrip()

            (it, qt) = sorted(itemdict.items(),
                              key=lambda x: x[1],
                              reverse=True)[0]
            postdescription[chart] = postdescription[
              chart] + " Looks like " + it + " is your most favorite item from our bakery."

            scripthtml = """
            <script>
                new Chart(document.getElementById('chart'), 
                {{  type : 'doughnut',
                    data : 
                      {{
                        labels : [ {0} ],
                        datasets : [
                          {{ 
                            data : [ {1} ], 
                            label : "{2}",
                            //backgroundColor: ["#ff9900"]
                            //borderColor : "#ff9900",
                            //fill : false 
                          }}
                          //,
                          //{{ 
                          //  data : [ {2} ], 
                          //  label : "{4}",
                          //  borderColor : "#e43202",
                          //  fill : false 
                          //}},
                        ] 
                      }},
                      options : 
                        {{
                          title : {{display : true, text : "{3}"}}
                        }}
                  }});
              </script>
            """.format(labeltext, datatext, "Item Distribution", '', '')
        if chart == 'me':
          if (orders != None) or (orders != '') or (orders != 'NA'):
            sugardata = []
            sugarlimitdata = []
            caloriedata = []
            labels = []
            chartvalmax = -1
            labels = [
              'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
              'Oct', 'Nov', 'Dec'
            ]
            monthcalorie = {
              1: 0,
              2: 0,
              3: 0,
              4: 0,
              5: 0,
              6: 0,
              7: 0,
              8: 0,
              9: 0,
              10: 0,
              11: 0,
              12: 0
            }
            for ord, dt in orddict.items():
              st = statdict[ord]
              if st == '':  #not complete
                st = "*"
              else:
                st = ''  #do not write anything

                dt = dt[0:10]
                month = datetime.strptime(dt,
                                          '%m/%d/%Y').month  #strftime("%B")
                monthcalorie[
                  month] = monthcalorie[month] + totalordercosts[ord]

            for k, v in monthcalorie.items():
              caloriedata.append(v)
            #labeltext = ', '.join(labels)
            labeltext = ''
            for l in labels:
              labeltext += "'" + l + "',"
            labeltext = labeltext.rstrip()
            datatext = ', '.join(map(str, caloriedata))
            #datatext2 = ', '.join(map(str, sugarlimitdata))
            #print(labeltext)
            #print(datatext)
            scripthtml = """
            <script>
                new Chart(document.getElementById('chart'), 
                {{  type : 'line',
                    data : 
                      {{
                        labels : [ {0} ],
                        datasets : [
                          {{ 
                            data : [ {1} ], 
                            label : "{2}",
                            backgroundColor: ["#ff0099"]
                            //borderColor : "#ff9900",
                            //fill : false 
                          }}
                          //,
                          //{{ 
                          //  data : [ {2} ], 
                          //  label : "{4}",
                          //  borderColor : "#e43202",
                          //  fill : false 
                          //}},
                        ] 
                      }},
                      options : 
                        {{
                          title : {{display : true, text : "{3}"}}
                        }}
                  }});
              </script>
            """.format(labeltext, datatext, "Cost in US $", '', '')
        # this part is put here as we do data analysis and some of the result description/analysis would be shown here
        # and that can be written only after doing the data analysis
        html += """
          <br/><br/>
          {0} <br/><br/><br/>
          </td></tr>
         </table>   
        """.format(postdescription[chart])
        html += """
          </td></tr></table>
          </div>
        </section>
        """
        #print("what")
        resp = make_response(
          render_template('template.html',
                          contenthtml=html,
                          useraccounthtml=GetUserAccountHTML(userid, ctoken),
                          scripthtml=scripthtml))
    #password did not match
    else:
      html += """
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td valign=top colspan=2>You have been logged out </td></tr>
      </table> 
      <br/><br/>
      <img src="/static/images/bakery_exit.png">
      <br/><br/>
      """
      html += """
        </div>
      </section>
      """
      resp = make_response(
        render_template('template.html',
                        contenthtml=html,
                        useraccounthtml=GetUserAccountHTML(None, None)))
  else:
    html += LoginFormHTML()
    html += """
    </div>
      </section>
      """
    resp = make_response(
      render_template('template.html',
                      contenthtml=html,
                      useraccounthtml=GetUserAccountHTML(None, None)))

  return resp


#### LOGIN PAGE ###############################################
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  html = """<section class="about_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
        User Account Set Up 
        </h2>
      </div>
      <br/>
    """

  if request.method == 'POST':
    user = request.form.get('user')
    pwds = request.form.get('pwds')

    pwds2 = request.form.get('pwds2')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    gender = request.form.get('gender')
    age = request.form.get('age')
    email = request.form.get('email')
    addr = request.form.get('address')

    success = True
    message = ''
    status = ''

    #TODO:
    #check user name exists or not
    if (len(user_list_of_dict) > 0):
      for line in user_list_of_dict:
        if user == line["username"]:
          success = False
          message = 'User name exists. Please use a different one.'
    #check email exists or not
    #if false no need to do this step
    if success == True:
      if (len(user_list_of_dict) > 0):
        for line in user_list_of_dict:
          if email == line["email"]:
            success = False
            message = 'Email account exists. If you forgot the account information, please click <a href=/forgot?f=p>Forgot Password</a>.'
    #check pwds and pwds2 are same or not
    if success == True:
      if (len(pwds) == 0) or (pwds == '') or (pwds != pwds2):
        success = False
        message = "Passwords empty or do not match."

    #check age is an integer (already done in HTML)
    #email send verificationcode and then another form to verify
    if success == True:
      verificationcode = random.randint(1000000, 9000000)
      newuser = user + "|" + pwds + "|" + fname + "|" + lname + "|" + gender + "|" + str(
        age) + "|" + email + "|" + addr + "|" + str(
          verificationcode) + "|||NA|NA|"
      filename = "accounts/allusers.txt"
      with open(filename, "a+") as fa:
        fa.write(newuser + "\n")

      RefreshUsers()

      html += """
        <table border="0" cellpadding="5" cellspacing="5" width="100%">
        <tr><td valign=top colspan=2><font color=green><b>Sign Up was successful </font> <br/><br/></td></tr>
        <tr><td valign=top colspan=2><img src=/static/images/donut.png width=150px height=150px> <br/><br/>
        <font color=green> Message: Please check your email to get the verification code and use it to verify your account <a href="/verify">here</a></font> <br/><br/>
        </td></tr>
      </table> 
        </div>
      </section>
      """
      resp = make_response(
        render_template('template.html',
                        contenthtml=html,
                        useraccounthtml=GetUserAccountHTML(None, None)))
    #password did not match
    else:
      html += """
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td valign=top colspan=2><font color=red><b>Sign Up was unsuccessful </font> <br/><br/></td></tr>
      <tr><td valign=top colspan=2><img src=/static/images/pretzel.png width=150px height=150px> <br/><br/>
      <font color=red>Message: {0} </font> <br/><br/>
        </td></tr>
      </table> 
      """.format(message)
      html += """
       </div>
      </section>
      """
      resp = make_response(
        render_template('template.html',
                        contenthtml=html,
                        useraccounthtml=GetUserAccountHTML(None, None)))
  else:
    html += SignupFormHTML()
    html += """
     <br/><br/>
     </div>
      </section>
      """
    resp = make_response(
      render_template('template.html',
                      contenthtml=html,
                      useraccounthtml=GetUserAccountHTML(None, None)))
  return resp


##### LOGIN PAGE ###############################################
@app.route('/login', methods=['GET', 'POST'])
def login():
  html = """<section class="about_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
        User Account Verification / Set Up
        </h2>
      </div>
      <br/>
    """

  if request.method == 'POST':
    user = request.form.get('user')
    pwds = request.form.get('pwds')
    #tokn = request.form.get('tokn')

    sessionid = ''
    if 'sessid' in request.cookies:
      sessionid = request.cookies.get("sessid")
    cookietokn = ''
    if 'tokn' in request.cookies:
      cookietokn = request.cookies.get("tokn")

    sessionidtosave = ''
    tokentosave = ''
    success = False
    status = ''
    #read the password
    if VerifyCurrentUserWithPassword(user, pwds) == True:
      success = True
      #check if the sessid is indeed done by this user. Read user.txt file (this can happen if order started and then user logged in)
      if sessionid == sessionidinfile:
        #if it is keep it
        print("Same session in cookie and in file")

      #else delete it from cookie as that was from a different user and take the one saved in alluser.txt
      else:
        print("Set the sessionid read from the file")
        sessionidtosave = sessionidinfile

      #check if cookietokn is NOT available
      #if not available then create a new tokn and save in both cookie as well as in user.txt (currenttoken)
      if cookietokn == '':
        tokentosave = str(uuid.uuid4())
        UpdateTokenForUser(user, tokentosave)
      #else if available
      else:
        #check if cookietokn is same as currenttoken in user.txt file
        if cookietokn == tokeninfile:
          #if it is keep it
          print("Same token in cookie and in file")

        #else
        else:
          #1) tell user it is logging you out of other devices, 2)  create a new tokn and save in both cookie as well as in user.txt (currenttoken)
          tokentosave = str(uuid.uuid4())
          UpdateTokenForUser(user, tokentosave)

      thisuser["lastlogin"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
      ret = SaveAllUsers()
      status = "0"

      html += """
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td align=center  style="border-bottom: solid 1px;"> 
        <div class="acctab_h">
          <a href="/account" class='b'>Account Profile</a>
          <a href="/account?w=o" >Activity/Past Orders</a>
          <a href="/account?w=a" >Order Data Analysis</a>
        </div>
      </td></tr>
      <tr><td>
      """

      html += """
      <table border="0" cellpadding="5" cellspacing="5" width="90%">
        <tr><td valign=top align=right width=50%><b>Username:</b> </td><td valign="top" align=left> {0} </td></tr>
        <tr><td valign=top align=right><b>First Name: </b></td><td valign="top" align=left> {1} </td></tr>
        <tr><td valign=top align=right><b>Last Name: </b></td><td valign="top" align=left> {2} </td></tr>
        <tr><td valign=top align=right><b>Email: </b></td><td valign="top" align=left> {3} </td></tr>
        <tr><td valign=top align=right><b>Address: </b></td><td valign="top" align=left> {4} </td></tr>
        
        <tr><td valign="top" align=center colspan=2> <button class="cartbuttonbig" onclick="window.location.href='/logout?conf=y';"> Logout </button> </td></tr>
        </table>   
      """.format(thisuser["username"], thisuser["firstname"],
                 thisuser["lastname"], thisuser["email"], thisuser["address"],
                 thisuser["orders"])

      html += """
        </td></tr></table>
        </div>
      </section>
      """

      resp = make_response(
        render_template('template.html',
                        contenthtml=html,
                        useraccounthtml=GetUserAccountHTML(user, tokentosave)))
      resp.set_cookie("user", user, max_age=30 * 60)  #30 minutes max
      resp.set_cookie("tokn", tokentosave, max_age=30 * 60)
      resp.set_cookie("sessid", sessionidtosave, max_age=30 * 60)

    #password did not match
    else:
      html += """
      <table border=0 cellpadding=5 cellspacing=5 width=100%>
      <tr><td colspan=2 style="border-top: solid 1px;"></tr>
      </table>
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td valign=top colspan=2>Login unsuccessful </td></tr>
      <tr><td valign=top colspan=2><img src=/static/images/cakeslice.png width=150px><br/> </td></tr>
      <tr><td valign=top align=right><a href=/forgot?f=p>Forgot password ? </a> |</td>
          <td valign=top  align=left><a href=/forgot?f=u>Forgot username ? </td></tr>
      </table> <br/><br/><br/>
      """
      html += """
       </div>
      </section>
      """
      resp = make_response(
        render_template('template.html',
                        contenthtml=html,
                        useraccounthtml=GetUserAccountHTML(None, None)))
  else:
    html += LoginFormHTML()
    html += """
     <br/><br/>
     <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td valign=top align=right><a href=/forgot?f=p>Forgot password ? </a> |</td>
          <td valign=top align=left><a href=/forgot?f=u>Forgot username ? </td></tr>
      </table> <br/><br/>
    </div>
      </section>
      """
    resp = make_response(
      render_template('template.html',
                      contenthtml=html,
                      useraccounthtml=GetUserAccountHTML(None, None)))
  return resp


##### LOGIN PAGE ###############################################
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
  html = """<section class="about_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
        User Account Retrieval 
        </h2>
      </div>
      <br/>
    """

  if request.method == 'POST':
    fuser = request.form.get('user')
    femail = request.form.get('email')
    what = request.form.get('what')
    #tokn = request.form.get('tokn')

    success = False
    status = ''
    #read the password
    msg = "Thank you!"
    if what == "forgotuser":
      if (len(user_list_of_dict) > 0):
        for line in user_list_of_dict:
          if femail.lower() == line["email"].lower():
            subj = "Bake N' Take - Forgot Username"
            mesg = "Your Bake N' Take Username Is: " + line["username"] + "\n"
            SendEmail(toemail=femail, tosubj=subj, totext=mesg, tohtml=mesg)
      msg = "Your username has beeen sent to your email, if you are registered with that email."
    if what == "forgotpass":
      if (len(user_list_of_dict) > 0):
        for line in user_list_of_dict:
          if fuser.lower() == line["username"].lower():

            subj = "Bake N' Take - Forgot Password"
            mesg = "Your Bake N' Take Password Is: " + line["password"] + "\n"
            SendEmail(toemail=line["email"],
                      tosubj=subj,
                      totext=mesg,
                      tohtml=mesg)
      msg = "Your password has beeen sent to your email, associated with your given username."

    html += """
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td align=center style="border-bottom: solid 1px;"  colspan=2> 
        <div class="acctab_h">
          <a href="/forgot?f=u" >Forgot Username </a>
          <a href="/forgot?f=p" class='b'>Forgot Password</a>
        </div>
      </td></tr>
      <tr><td align=center  colspan=2>
      <tr><td valign=top colspan=2>Please Check Your Email. <br/>{0} </td></tr>
      <tr><td valign=top colspan=2><img src=/static/images/pretzel.png width=150px><br/> </td></tr>
      <tr><td valign=top align=right><a href=/forgot?f=p>Forgot password ? </a> |</td>
          <td valign=top  align=left><a href=/forgot?f=u>Forgot username ? </td></tr>
      </table> 
      """.format(msg)
    html += """
       </div>
      </section>
      """
    resp = make_response(
      render_template('template.html',
                      contenthtml=html,
                      useraccounthtml=GetUserAccountHTML(None, None)))
  else:
    forgotwhat = request.args.get("f")
    if forgotwhat == 'u':
      html += ForgotUsernameFormHTML()
    else:
      html += ForgotPasswordFormHTML()
    html += """
     <br/><br/>
     <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td valign=top align=right><a href=/login>Log In </a> | </td>
          <td valign=top align=left><a href=/signup>Sign Up </td></tr>
      </table> <br/><br/>
    </div>
      </section>
      """
    resp = make_response(
      render_template('template.html',
                      contenthtml=html,
                      useraccounthtml=GetUserAccountHTML(None, None)))
  return resp


##### ABOUT PAGE ###############################################
@app.route('/about')
def about():
  html = """
  <section class="about_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
          About Us
        </h2>
      </div>
      <br/>
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td colspan=2 style="border-top: solid 1px;"></tr>
      <tr><td valign=top width=40%>
      <div class="">
        <img src="/static/images/baker.jpg" alt="" width="350px" style="border-radius:5px">
      </div>
      </td><td valign="top" align="left">
      <div class="detail-box">
        <p>
          Welcome to our bakery, where every bite is a little slice of heaven. Starting a bakery can be a rewarding and fulfilling endeavor, but it also requires significant hard work, dedication, and planning. Our business aims to create unique flavors that customers can enjoy! We want you to feel delighted after tasting our baked goods. We also want to inspire bakers worldwide to follow their passions and bake healthy and tasty. 
        </p>
        
        <p>
          We are a team of passionate bakers who believe that great food starts with the best ingredients and a lot of love. Our mission is to create delicious baked goods low in sugar that satisfy both the stomach and the soul.
        </p>
        
        <p>
          At our bakery, we specialize in a variety of baked goods, from fresh bread to decadent pastries. All of our products are made from scratch, using only the highest quality ingredients. Whether you're in the mood for a warm croissant, a fluffy muffin, or a rich chocolate cake, we have something to satisfy your cravings.
        </p>
        
        <p>
        We pride ourselves on our commitment to quality and customer service. We believe that every customer deserves to be treated like family, and we strive to create a warm and welcoming atmosphere in our bakery. We are always happy to answer any questions you may have and offer recommendations based on your preferences.
        </p>

        <p>
        So come on in and treat yourself to something sweet. We promise you won't be disappointed. Thank you for choosing our bakery, and we look forward to serving you soon!
        </p>

      </div>
      </td></tr>
     </table>

    </div>
  </section>
  
  
  """

  #return 'Hello from Flask!'
  return render_template('template.html',
                         contenthtml=html,
                         useraccounthtml=GetUserAccountHTML(None, None))


###### CONTACT ##############################################################################################
@app.route("/contact", methods=['GET', 'POST'])
def contact():
  newentry = None
  if request.method == 'POST':
    email = request.form.get('email')
    subj = request.form.get('subj')
    mesg = request.form.get('mesg')
    newentry = "Yes"

  html = """<section class="about_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
        Contact Us
        </h2>
      </div>
      <br/>
      <table border=0 cellpadding=5 cellspacing=5 width=100%>
      <tr><td colspan=2 style="border-top: solid 1px;"></tr>
      </table>
  """

  if newentry != None:
    try:
      subj = subj + "From: " + email
      SendEmail(toemail="bakentake2007@gmail.com",
                tosubj=subj,
                totext=mesg,
                tohtml=mesg)
      reply = "Thank you for contacting us. We will get back to you as soon as we can. - Bake N' Take Team"
      SendEmail(toemail=email,
                tosubj="Acknowledgement",
                totext=reply,
                tohtml=reply)
      html += "<br/>Your message has been successfully sent. <br/>-Bake N' Take Team."
    except Exception as e:
      html += "<br/>Uh Oh! Some technical problem happened. Please contact us by other means or try a little later. Sorry about it. <br/>- Bake N' Take Team."

  email = GetUserAccountEmail(None, None)
  html += """
    <center>
    <table border="0" cellpadding="5" cellspacing="5" width="100%"> <tr><td colspan=2><form name=order action=/contact method=POST>
    <tr><td align=left> Your Email: </td><td align=left><input type=text size=30 name=email value={0}></td></tr>
    <tr><td align=left> Subject: </td><td align=left><input type=text size=30 name=subj></td></tr>
    <tr><td align=left valign=top> Your Message: </td><td align=left>
    <textarea id="idmesg" name="mesg" rows="4" cols="50">
    </textarea>
    </td></tr>
    <tr><td>&nbsp;</td><td><button class="cartbuttonbig" onclick=this.form.submit()> Send Email </button></form></td></tr>
    </table>
    </center>
    </div>
  </section><br/><br/><br/><br/><br/><br/><br/>
  """.format(email)
  return render_template('template.html',
                         contenthtml=html,
                         useraccounthtml=GetUserAccountHTML(None, None))


##### PRIVACY PAGE ###############################################
@app.route('/privacy')
def privacy():
  html = """
  <section class="about_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
          Privacy Policy
        </h2>
      </div>
      <br/>
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td colspan=2 style="border-top: solid 1px;"></tr>
      <tr><td valign=top>
      </td><td valign="top" align="left">
      <div class="detail-box">
        Effective Date: 2023-06-26 <br/><br/>

Thank you for visiting Bake N' Take's website and for your interest in our privacy practices. This Privacy Policy explains how we collect, use, disclose, and protect the personal information you provide when accessing or using our website. We are committed to respecting your privacy and safeguarding your personal information. Please read this Privacy Policy carefully to understand our practices regarding your personal data.<br/><br/>

<b>Information We Collect</b><br/><br/>
1.1 Personal Information: <br/>
When you visit our website, we may collect personal information that you voluntarily provide to us, such as your name, email address, phone number, and any other information you provide when contacting us through our website's forms or placing an order.
<br/>

1.2 Cookies and Other Tracking Technologies:<br/>
We may use cookies, web beacons, and similar technologies to collect information about your browsing activities on our website. This may include your IP address, browser type, operating system, referring URLs, and other technical information. These technologies help us analyze trends, administer the website, track users' movements, and gather demographic information.
<br/>
<br/>
<b>Use of Information</b><br/><br/>
2.1 Personal Information:<br/>
We may use the personal information you provide to us to:
<br/>

Respond to your inquiries and fulfill your requests.
<br/>Process and deliver your orders for our bakery products.
<br/>Send you important administrative information, such as order confirmations, updates, and notifications.
<br/>Communicate with you about our products, services, promotions, and offers, if you have opted to receive such communications.
<br/>Improve and personalize your website experience.
<br/>
<br/>2.2 Cookies and Other Tracking Technologies:
<br/>We may use cookies and similar technologies to:

<br/>Remember your preferences and settings for a more personalized experience.
<br/>Analyze website usage and improve our website's functionality.
<br/>Provide relevant advertising based on your interests.
<br/><br/>
<b>Disclosure of Information</b><br/>
<br/>3.1 Service Providers:
<br/>We may share your personal information with third-party service providers who help us operate our business and provide services on our behalf. These service providers are obligated to protect your information and may only use it to perform services for us.
<br/>
<br/>3.2 Legal Requirements:
<br/>We may disclose your personal information if required to do so by law or if we believe such action is necessary to comply with legal obligations, protect our rights, or prevent any fraudulent or illegal activities.
<br/>
<br/>3.3 Business Transfers:
<br/>In the event of a merger, acquisition, or sale of all or a portion of our assets, your personal information may be transferred to the acquiring entity as part of the transaction. We will notify you via email or a prominent notice on our website of any change in ownership or use of your personal information.
<br/>
<br/>
<b>Data Security</b>
<br/>We implement reasonable security measures to protect your personal information from unauthorized access, use, or disclosure. However, please note that no method of transmission over the internet or electronic storage is completely secure. While we strive to protect your personal information, we cannot guarantee its absolute security.
<br/>
<br/>
<b>Your Choices</b>
<br/>5.1 Communications:
<br/>You may choose to receive promotional communications from us by subscribing to our newsletter or similar services. If you wish to opt out of receiving such communications, you can unsubscribe using the instructions provided in the communication or by contacting us directly.
<br/>
<br/>5.2 Cookies:
<br/>Most web browsers are set to accept cookies by default. However, you can usually modify your browser settings to decline cookies or alert you when a cookie is being sent. Please note that if you choose to disable cookies, some parts of our website may not function properly.
<br/>
<br/>
<b>Children's Privacy</b>
<br/>Our website is not intended for children under the age of 13. We do not knowingly collect personal information from children under the age of 13. If you believe we have inadvertently collected personal information from a child under 13, please contact us immediately, and we will delete them.
<br/><br/>If you have any questions or concerns regarding these Terms of Use, please contact us at <a href=mailto:bakentake2007@gmail.com>bakentake2007@gmail.com</a>.

<br/><br/>Thank you for using Bake N' Take's  website. Enjoy your browsing experience!


      </div>
      </td></tr>
     </table>

    </div>
  </section>
  
  
  """

  #return 'Hello from Flask!'
  return render_template('template.html',
                         contenthtml=html,
                         useraccounthtml=GetUserAccountHTML(None, None))


##### TERMS OF USE PAGE ###############################################
@app.route('/terms')
def terms():
  html = """
  <section class="about_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
          Terms Of Use
        </h2>
      </div>
      <br/>
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td colspan=2 style="border-top: solid 1px;"></tr>
      <tr><td valign=top>
      </td><td valign="top" align="left">
      <div class="detail-box">
Effective Date: 2023-06-26

<br/><br/>Please read these Terms of Use carefully before using [Bakery Name]'s website. By accessing or using our website, you agree to be bound by these Terms of Use. If you do not agree with any part of these terms, please refrain from using our website.

<br/><br/><b>1. Website Use</b>

<br/><br/>1.1 Acceptable Use:
<br/>You agree to use our website for lawful purposes and in a manner that does not violate any applicable laws, regulations, or third-party rights. You are solely responsible for your conduct while using the website and for any content you submit or transmit through it.

<br/><br/>1.2 User Account:
<br/>Some features of our website may require you to create a user account. You are responsible for maintaining the confidentiality of your account information and for all activities that occur under your account. You must promptly notify us of any unauthorized access or use of your account.

<br/><br/><b>2. Intellectual Property</b>

<br/><br/>2.1 Ownership:
<br/>All content on our website, including text, images, logos, designs, and other materials, are the property of [Bakery Name] or its licensors and are protected by intellectual property laws. You may not use, copy, distribute, modify, or reproduce any content from our website without our prior written consent.

<br/><br/>2.2 Trademarks:
<br/>The [Bakery Name] name, logo, and any other trademarks or service marks displayed on our website are the exclusive property of [Bakery Name]. You may not use these trademarks without our prior written permission.

<br/><br/><b>3. Third-Party Content and Links</b>
<br/>Our website may contain links to third-party websites or display content from third parties. These links and content are provided for your convenience and do not imply endorsement or responsibility on our part. We do not control or assume any liability for the content or practices of these third-party websites. You access and use them at your own risk.

<br/><br/><b>4. Disclaimer of Warranties</b>

<br/><br/>4.1 Information Accuracy:
<br/>We strive to provide accurate and up-to-date information on our website. However, we do not warrant or guarantee the accuracy, completeness, or reliability of any information or content on our website. You use the information provided on our website at your own risk.

<br/><br/>4.2 Website Availability:
<br/>We make reasonable efforts to ensure our website is available and functioning properly. However, we do not guarantee uninterrupted access to our website or its error-free operation. We may temporarily suspend or restrict access to our website for maintenance or other reasons without prior notice.

<br/><br/><b>5. Limitation of Liability</b>
<br/>To the extent permitted by applicable law, [Bakery Name] and its affiliates, officers, directors, employees, agents, and representatives shall not be liable for any direct, indirect, incidental, consequential, or special damages arising out of or in connection with your use or inability to use our website, even if advised of the possibility of such damages.

<br/><br/><b>6. Indemnification</b>
<br/>You agree to indemnify, defend, and hold [Bakery Name] and its affiliates, officers, directors, employees, agents, and representatives harmless from any claims, liabilities, damages, losses, costs, or expenses arising out of or in connection with your use of our website or violation of these Terms of Use.

<br/><br/><b>7. Modifications</b>

<br/>We reserve the right to modify, amend, or update these Terms of Use at any time without prior notice. Any changes will be effective immediately upon posting on our website. Your continued use of our website after such changes constitutes your acceptance of the revised terms.

<br/><br/><b>8. Governing Law</b>

<br/>These Terms of Use shall be governed by and construed in accordance with the laws of [Jurisdiction]. Any legal actions or proceedings arising out of or relating to these Terms of Use shall be brought exclusively in the courts of [Jurisdiction].

<br/><br/>If you have any questions or concerns regarding these Terms of Use, please contact us at <a href=mailto:bakentake2007@gmail.com>bakentake2007@gmail.com</a>.

<br/><br/>Thank you for using Bake N' Take's  website. Enjoy your browsing experience!


      </div>
      </td></tr>
     </table>

    </div>
  </section>
  
  
  """

  #return 'Hello from Flask!'
  return render_template('template.html',
                         contenthtml=html,
                         useraccounthtml=GetUserAccountHTML(None, None))


##### COOKIE USE PAGE ###############################################
@app.route('/cookie', methods=['GET', 'POST'])
def cookie():
  confirm = ""
  if request.method == 'GET':
    confirm = request.args.get("accept")

  if 'bakentakecookie' in request.cookies:
    msg = "<b>Functional Cookie Was Accepted In The Past</b>"
    confirm = "fc"  #once more
  else:
    msg = "<a href=/cookie?accept=fc>Accept Minimal Functional Cookie</a> <br/>(by default it is accepted if you place order)"

  html = """
  <section class="about_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
          Cookie Preferences
        </h2>
      </div>
      <br/>
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td colspan=2 style="border-top: solid 1px;"></tr>
      <tr><td valign=top>
      </td><td valign="top" align="left">
      <div class="detail-box">
      <br/> <center>{0}</center>
<br/>A cookie preferences policy, also known as a cookie policy or cookie consent policy, is a document that outlines how a website or online service uses cookies and similar tracking technologies, and how it obtains and manages user consent for their use.
<br/>
<br/>Here are some key points that are typically covered in a cookie preferences policy:
<br/>
<br/>Explanation of cookies: The policy should provide a clear and understandable explanation of what cookies are, how they work, and why they are used on the website.
<br/>
<br/>Types of cookies: The policy should list and describe the different types of cookies used on the website, such as functional cookies, analytical cookies, advertising cookies, and third-party cookies.
<br/>
<br/>Purpose of cookies: The policy should explain the purposes for which cookies are used, such as improving website functionality, analyzing user behavior, personalizing content, and displaying targeted advertisements.
<br/>
<br/>Cookie management: The policy should explain how users can manage their cookie preferences, including options for accepting or rejecting cookies, withdrawing consent, and deleting cookies from their devices.
<br/>
<br/>Third-party cookies and tracking: If the website uses third-party cookies or allows third-party tracking, the policy should disclose this information and provide details on the specific third-party services involved.
<br/>
<br/>Data collection and privacy: The policy should explain how the website collects, processes, and protects user data in relation to cookies, including any data sharing practices with third parties.
<br/>
<br/>Changes to the policy: The policy should state that it may be updated from time to time and provide information on how users will be notified of changes.
<br/>
<br/>It's important to note that cookie preferences and policies may be subject to regional or national regulations, such as the General Data Protection Regulation (GDPR) in the European Union. Compliance with these regulations is crucial for websites that have users from those regions.
<br/>
<br/>To create a comprehensive and compliant cookie preferences policy for your website, it is advisable to consult with legal professionals or seek guidance from relevant regulatory authorities to ensure you meet the requirements specific to your jurisdiction.
      </div>
      </td></tr>
     </table>

    </div>
  </section>
  
  
  """.format(msg)

  #return 'Hello from Flask!'
  resp = make_response(
    render_template('template.html',
                    contenthtml=html,
                    useraccounthtml=GetUserAccountHTML(None, None)))

  if confirm == "fc":
    resp.set_cookie("bakentakecookie", '',
                    max_age=10 * 365 * 24 * 60 * 60)  #10 years

  return resp


##### SOCIAL MEDIA USE PAGE ###############################################
@app.route('/social', methods=['GET', 'POST'])
def csocial():
  which = ""
  if request.method == 'GET':
    which = request.args.get("w")

    if which == "f":
      title = "Facebook"
      img = '<img src=/static/images/facebook.png width="32px" height="32px" style="background-color: #ffffff;" title="Facebook">'
    if which == "t":
      title = "Twitter"
      img = '<img src=/static/images/twitter.png width="32px" height="32px"  style="background-color: #ffffff;" title="Twitter">'
    if which == "p":
      title = "Pinterest"
      img = '<img src=/static/images/pinterest.png width="32px" height="32px" style="background-color: #ffffff;" title="Pinterest">'
    if which == "i":
      title = "Instagram"
      img = '<img src=/static/images/instagram.png width="32px" height="32px" style="background-color: #ffffff;" title="Instagram">'

  html = """
  <section class="about_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
          Social Media Integration : {0}
        </h2>
      </div>
      <br/>
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td colspan=2 style="border-top: solid 1px;"></tr>
      <tr><td valign=top>
      </td><td valign="top" align="left">
      <div class="detail-box">
      <br/> <center>{1}<br/><br/>

      <table class=table-rounded-corners style="background:#9f6f00; color:#ffffff" cellpadding=20px width=80%><tr><td> 
      Hello, We do not have a social presence as we have not actually built a company yet. We created 
      this website as a Proof-Of-Concept and to show the capabilities and feature it can offer. <br/><br/>If we build a company later we
      can always open social media accounts/pages and then can link them here or integrate them
      inside this page for a smooth experience under one banner. Thank you!
      </td></tr></table> </center>
      <br/><br/><br/><br/><br/><br/><br/><br/><br/>
      </div>
      </td></tr>
     </table>

    </div>
  </section>
  """.format(title, img)

  #return 'Hello from Flask!'
  resp = make_response(
    render_template('template.html',
                    contenthtml=html,
                    useraccounthtml=GetUserAccountHTML(None, None)))
  return resp


##### SITE MAP PAGE ###############################################
@app.route('/site')
def site():
  html = """
  <section class="health_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
          Site Map
        </h2>
      </div>
      <br/>
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td colspan=2 style="border-top: solid 1px;"></tr>
      <tr><td valign=top>
      </td><td valign="top" align="left">
      <div class="detail-box">
      <center>
      <table cellpadding="5" cellspacing = "5" width="80%" font-size="12px" class="table-rounded-corners">
      <tr style="color:#ffffff" font-size="12px"><td bgcolor="#71322E" font-size="12px" colspan=2 align=center>Site Map Links </td></tr>
      <tr><td width=40%  bgcolor="#cccccc" > <b> Main Navigation Link  </td><td  bgcolor="#cccccc" ><b> Sub Links Under It (If Any)</td><tr>
      <tr><td width=20%> <b><a href="/" style=""> Home </a> >> </td><td></td><tr>
        <tr><td> </td><td><a href="/privacy" style=""> Privacy Policy </a> </td><tr>
        <tr><td> </td><td><a href="/terms" style=""> Terms Of Use </a> </td><tr>
        <tr><td> </td><td><a href="/cookie" style=""> Cookie Preferences </a> </td><tr>
        <tr><td> </td><td><a href="/site" style=""> Site Map (this document) </a> </td><tr>
      <tr><td width=20%> <b><a href="/about" style=""> About </a>  </td><td></td><tr>
      <tr><td width=20%> <b><a href="/principle" style=""> Out Principle </a>  </td><td></td><tr>
      <tr><td width=20%> <b><a href="/menu" style=""> Menu </a>  >> </td><td></td><tr>
        <tr><td> </td><td><a href="/menu?iid=bt0014" style="">  Pita Bread </a> </td><tr>
        <tr><td> </td><td><a href="/menu?iid=bt0009" style=""> Croissant </a> </td><tr>
        <tr><td> </td><td><a href="/menu?iid=bt0016" style=""> 	Baguette </a> </td><tr>
        <tr><td> </td><td><a href="/menu?iid=bt0001" style=""> 	Fresh Sourdough </a> </td><tr>
        <tr><td> </td><td><a href="/menu?iid=bt0007" style=""> Cinnamon Rolls </a> </td><tr>
        <tr><td> </td><td><a href="/menu?iid=bt0013" style=""> Donut </a> </td><tr>
        <tr><td> </td><td><a href="/menu?iid=bt0010" style=""> Churros(3 per pac) </a> </td><tr>
        <tr><td> </td><td><a href="/menu?iid=bt0011" style=""> Macaroons(3 per pac) </a> </td><tr>
        <tr><td> </td><td><a href="/menu?iid=bt0015" style=""> Hot Chocolate </a> </td><tr>
        <tr><td> </td><td><a href="/menu?iid=bt0004" style=""> Muffins </a> </td><tr>
        <tr><td> </td><td><a href="/menu?iid=bt0003" style=""> Cupcake </a> </td><tr>
        <tr><td> </td><td><a href="/menu?iid=bt0005" style=""> Classic Brownies </a> </td><tr>
        <tr><td> </td><td><a href="/menu?iid=bt0002" style=""> Chocolate Chip Cookies </a> </td><tr>
        <tr><td> </td><td><a href="/menu?iid=bt0008" style=""> Pie </a> </td><tr>
        <tr><td> </td><td><a href="/menu?iid=bt0012" style=""> Cake </a> </td><tr>
      <tr><td width=20%> <b><a href="/order" style=""> Order </a>  </td><td></td><tr>
      <tr><td width=20%> <b><a href="/reviews" style=""> Reviews </a>  </td><td></td><tr>
      <tr><td width=20%> <b><a href="/contact" style=""> Contact Us </a>  >> </td><td></td><tr>
        <tr><td> </td><td><a href="/chat" style=""> Chat </a> </td><tr>
        <tr><td> </td><td><a href="mailto:bakentake2007@gmail.com" style=""> bakentake2007@gmail.com </a> </td><tr>
      <tr><td width=20%> <b><a href="/search?q=cake" style=""> Search (for a keyword)</a>  </td><td></td><tr>
      <tr><td width=20%> <b><a href="/account" style=""> Account </a>  >> </td><td></td><tr>     
        <tr><td> </td><td><a href="/login" style=""> Login </a> </td><tr>
        <tr><td> </td><td><a href="/signup" style=""> Sign Up </a> </td><tr>
        <tr><td> </td><td><a href="/account?w=o" style=""> Past Orders </a> </td><tr>
        <tr><td> </td><td><a href="/account?w=a" style=""> Order Data Analysis </a> </td><tr>
      </table>
      <center>
      </div>
      </td></tr>
     </table>

    </div>
  </section>
  
  
  """

  #return 'Hello from Flask!'
  return render_template('template.html',
                         contenthtml=html,
                         useraccounthtml=GetUserAccountHTML(None, None))


############################################################################################################
@app.route('/news')
def news():
  html = """
  <section class="about_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>News </h2>
      </div>
      <br/>
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td>
      <div class="">
        <img src="/static/images/bakingnews.jpg" alt="" width="80%">
      </div>
      </td><td valign="top">
      </td></tr>
     </table>

    </div>
  </section>
  
  
  """

  #return 'Hello from Flask!'
  return render_template('template.html',
                         contenthtml=html,
                         useraccounthtml=GetUserAccountHTML(None, None))


############################################################################################################
@app.route("/search", methods=['GET'])
def search():
  itemid = 'NA'
  if request.method == 'GET':
    keyword = request.args.get("q")

  item_listdict = readitems()
  flav_listdict = readflavors()
  topp_listdict = readtoppings()
  type_listdict = readtypes()
  print(itemid)
  html = ShowMenu(item_listdict, flav_listdict, topp_listdict, type_listdict,
                  itemid, keyword)
  return render_template('template.html',
                         contenthtml=html,
                         useraccounthtml=GetUserAccountHTML(None, None))


############################################################################################################
@app.route("/menu", methods=['GET', 'POST'])
def menu():
  itemid = 'NA'
  if request.method == 'GET':
    itemid = request.args.get("iid")

  item_listdict = readitems()
  flav_listdict = readflavors()
  topp_listdict = readtoppings()
  type_listdict = readtypes()
  print(itemid)
  html = ShowMenu(item_listdict, flav_listdict, topp_listdict, type_listdict,
                  itemid, '')
  return render_template('template.html',
                         contenthtml=html,
                         useraccounthtml=GetUserAccountHTML(None, None))


############################################################################################################
@app.route('/principle')
def principle():

  html = """
  <section class="about_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
          Our Principle
        </h2>
      </div>
      <br/>
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td colspan=2 style="border-top: solid 1px;"></tr>
      <tr><td valign=top width=40%>
        <img src="/static/images/1.jpg" alt="" width="350px"  style="border-radius:5px">
      </td><td valign="top" align="left">
      <div class="detail-box">
        <p>
        At our establishment, we believe in providing our customers with delicious and healthy baked goods that don't compromise on taste. Our principle is rooted in our commitment to promoting a healthier lifestyle by offering baked goods that are low in sugar but high in flavor.
        </p>

        <p>
        <b>Health is our Priority:</b> We believe that a healthy diet is essential for a happy and fulfilling life. That's why we offer baked goods that are low in sugar, using alternative sweeteners that are natural and healthier for our bodies.
        </p>

        <p>
        <b>Natural Ingredients:</b> We use only natural and high-quality ingredients in our baked goods. Our ingredients are sourced locally and are free from artificial flavors, preservatives, and additives.
        </p>

        <p>
        <b>Flavor Matters:</b> We believe that healthy baked goods can still be flavorful and enjoyable. We use creative and innovative techniques to make our products taste just as delicious as traditional baked goods while keeping the sugar content low.
        </p>

        <p>
        <b>Transparency:</b> We are committed to being transparent about the ingredients we use and the nutritional information of our products. We believe that our customers have the right to know what they're eating, and we provide detailed information on the sugar content of our products.
        </p>

        <p>
        <b>Customer Satisfaction:</b> We value our customers and their satisfaction. We are dedicated to providing excellent customer service and a welcoming environment that makes our customers feel good about their choices.
        </p>

        <p>
        At our low-sugar bakery, we uphold these principles in everything we do. We believe that we can make a positive impact on the health and well-being of our customers by offering delicious and healthy baked goods that are low in sugar. Come and visit us to try our unique and flavorful treats that will satisfy your cravings without sacrificing your health.
        </p>

      </div>
      </td></tr>
     </table>

    </div>
  </section>
  
  
  """

  #return 'Hello from Flask!'
  return render_template('template.html',
                         contenthtml=html,
                         useraccounthtml=GetUserAccountHTML(None, None))


###############################################################
@app.route('/newsletter', methods=['POST'])
def newsletter():
  if request.method == 'POST':
    toemail = request.form.get('email')

    try:
      totext = "Hello {0}, \nThank you for signing up for our newsletter!".format(
        toemail)
      tohtml = """
      Hello {0}, <br/><br/>
      
      Thank you for signing up for our Bake N'Take newsletter service!<br/>
      You should be receving our newsletters from now on.<br/><br/>

      If you have any questions, please feel free to reach us.<br/><br/>

      Thanks,<br/>
      Bake N' Take Team 
      """.format(toemail)

      SendEmail(toemail=toemail,
                tosubj="Acknowledgement",
                totext=totext,
                tohtml=tohtml)

      html = """<section class="about_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
        Newsletter Subscription        
        </h2>
      </div>
      <br/><center>
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td valign="top">
      <div class="detail-box">
        <p>
          Thank you for subscribing. Please check your email.
        </p>
      
      </div>
      </td></tr><tr><td valign=top>
        <img src="/static/images/icon-baked.png" alt="" width="80%">
      </td></tr>
     </table> </center>
    </div>
  </section>
  """

      return render_template('template.html',
                             contenthtml=html,
                             useraccounthtml=GetUserAccountHTML(None, None))
    except:
      html = """<section class="about_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
        Newsletter Subscription        
        </h2>
      </div>
      <br/><center>
      <table border="0" cellpadding="5" cellspacing="5" width="100%">
      <tr><td valign=top>
        <img src="/static/images/icon-baked.png" alt="" width="80%">
      </td><td valign="top">
      <div class="detail-box">
        <p>
          <font color=red>It's not you. It's us. We will get back to you as soon as we can.</font> 
        </p>
      
      </div>
      </td></tr>
     </table> </center>
    </div>
  </section>
  """
      return render_template('template.html',
                             contenthtml=html,
                             useraccounthtml=GetUserAccountHTML(None, None))


##############################################################
def SendEmail(toemail, tosubj, totext, tohtml):
  sender_email = "bakentake2007@gmail.com"
  password = "vynnyhrqtynskfjo"

  message = MIMEMultipart("alternative")
  message["Subject"] = tosubj
  message["From"] = sender_email
  message["To"] = toemail

  part1 = MIMEText(totext, "plain")
  part2 = MIMEText(tohtml, "html")

  # Add HTML/plain-text parts to MIMEMultipart message
  # The email client will try to render the last part first
  message.attach(part1)
  message.attach(part2)

  # Create secure connection with server and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, toemail, message.as_string())


###############################################################
def readitems():
  filename = "itemdb/items.txt"
  item_list_of_dict = []
  with open(filename, 'r') as file:
    for linedict in csv.DictReader(file, delimiter='|'):
      item_list_of_dict.append(linedict)

  item_list_of_dict = sorted(item_list_of_dict,
                             key=lambda d: float(d['itemsugar']))
  return item_list_of_dict


###############################################################
def readflavors():
  filename = "itemdb/flavors.txt"
  flav_list_of_dict = []
  with open(filename, 'r') as file:
    for linedict in csv.DictReader(file, delimiter='|'):
      flav_list_of_dict.append(linedict)
  return flav_list_of_dict


###############################################################
def readtoppings():
  filename = "itemdb/toppings.txt"
  topp_list_of_dict = []
  with open(filename, 'r') as file:
    for linedict in csv.DictReader(file, delimiter='|'):
      topp_list_of_dict.append(linedict)
  return topp_list_of_dict


###############################################################
def readtypes():
  filename = "itemdb/types.txt"
  type_list_of_dict = []
  with open(filename, 'r') as file:
    for linedict in csv.DictReader(file, delimiter='|'):
      type_list_of_dict.append(linedict)
  return type_list_of_dict


###############################################################
def GetSessionInfo(sessid):
  infofilename = "sessions/{0}-info.txt".format(sessid)
  datime = None
  suglim = ''
  user = ''
  email = ''
  status = ''
  if exists(infofilename) == True:
    lines = []
    with open(infofilename, "r") as fr:
      lines = fr.readlines()
    for index, line in enumerate(lines):
      line = line.strip()
      if "DateTime:" in line:
        datime = line.replace("DateTime:", "").strip()
      if "SugarLimit:" in line:
        suglim = line.replace("SugarLimit:", "").strip()
      if "User:" in line:
        user = line.replace("User:", "").strip()
      if "Email:" in line:
        email = line.replace("Email:", "").strip()
      if "Status:" in line:
        status = line.replace("Status:", "").strip()

  return (datime, suglim, user, email, status)


###########################################################################
def ShowMenu(item_listdict, flav_listdict, topp_listdict, type_listdict, iid,
             searchkey):  #, sessid, suglim):
  #READ FROM THE ITEMS.TXT AND BUILD CARDS FOR EACH ITEM AND THEN ADD THEM
  html = ""
  counter = 0

  if iid != None:  # "NA":
    header = """
  <section class="health_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>Our Menu (Item Details)</h2>
      </div>
      <br/>
      <table border=0 cellpadding=5 cellspacing=5 width=100%>
      <tr><td colspan=2 style="border-top: solid 1px;"></tr>
      </table>
      <center><br/><table cellpadding="5" cellspacing = "5" width="90%" font-size="12px" class="table-rounded-corners">
  """
    if searchkey != '':
      header += """
      <tr style="color:#ffffff" font-size="12px"><td bgcolor="#71322E" font-size="12px">Image</td><td bgcolor="#71322E" width=25%>Item</td><td bgcolor="#71322E" width=20%>Varieties</td><td bgcolor="#71322E" width=15%>Sugar </td><td bgcolor="#71322E" width=15%>Calorie </td><td bgcolor="#71322E" width=10%>Price</td></tr>
      """
  else:
    header = """
  <section class="health_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>Our Menu</h2>
      </div>
      <br/>
      <table border=0 cellpadding=5 cellspacing=5 width=100%>
      <tr><td colspan=2 style="border-top: solid 1px;"></tr>
      </table> 
      <center><br/><table cellpadding="5" cellspacing = "5" width="90%" font-size="12px" class="table-rounded-corners">
      <tr style="color:#ffffff" font-size="12px"><td bgcolor="#71322E" font-size="12px">Image</td><td bgcolor="#71322E" width=25%>Item</td><td bgcolor="#71322E" width=20%>Varieties</td><td bgcolor="#71322E" width=15%>Sugar </td><td bgcolor="#71322E" width=15%>Calorie </td><td bgcolor="#71322E" width=10%>Price</td></tr>
  """

  html += header

  for item in item_listdict:
    #itemid|itemname|itemdescription|itemunitprice|itemsugar|itemunitcalorie|itemavailableunits|itemflavorids|itemtypeids|itemtoppingids|itemimage
    iiden = item["itemid"]
    iname = item["itemname"]
    idesc = item["itemdescription"]
    ipric = item["itemunitprice"]
    isuga = item["itemsugar"]
    icalo = item["itemunitcalorie"]
    iunit = item["itemavailableunits"]
    iflas = item["itemflavorids"]
    ityps = item["itemtypeids"]
    itops = item["itemtoppingids"]
    iimag = item["itemimage"]

    #creating the select drop down menu for flavors - IF ANY
    flavhtml = ""
    if iflas != "NA":
      flavids = iflas.split(',')
      for flavo in flav_listdict:
        #flavorid|flavorname|flavorprice|flavorsugar|flavorcalorie|flavoravailableunits|flavorimage
        fiden = flavo["flavorid"]
        fname = flavo["flavorname"]
        fpric = flavo["flavorprice"]
        fsuga = flavo["flavorsugar"]
        fcalo = flavo["flavorcalorie"]
        funit = flavo["flavoravailableunits"]
        fimag = flavo["flavorimage"]
        if fiden in flavids:
          flavhtml += '{0}, '.format(fname)
      flavhtml += "&nbsp;"

    #creating the select drop down menu for types - IF ANY
    typehtml = ""
    if ityps != "NA":
      typehtml = ''
      typeids = ityps.split(',')
      for typeo in type_listdict:
        #typeid|typename|typeprice|typesugar|typecalorie|typeavailableunits|typeimage
        tiden = typeo["typeid"]
        tname = typeo["typename"]
        tpric = typeo["typeprice"]
        tsuga = typeo["typesugar"]
        tcalo = typeo["typecalorie"]
        tunit = typeo["typeavailableunits"]
        timag = typeo["typeimage"]
        if tiden in typeids:
          typehtml += '{0}, '.format(tname)
      typehtml += "&nbsp; "

    #creating the select drop down menu for toppings - IF ANY
    topphtml = ""
    if itops != "NA":
      topphtml = ''
      toppids = itops.split(',')
      for toppo in topp_listdict:
        #toppingid|toppingname|toppingprice|toppingsugar|toppingcalorie|toppingavailableunits|toppingimage
        piden = toppo["toppingid"]
        pname = toppo["toppingname"]
        ppric = toppo["toppingprice"]
        psuga = toppo["toppingsugar"]
        pcalo = toppo["toppingcalorie"]
        punit = toppo["toppingavailableunits"]
        pimag = toppo["toppingimage"]
        if piden in toppids:
          topphtml += '{0}, '.format(pname)
      topphtml += "&nbsp; "

    if len(searchkey) > 0:
      searchkey = searchkey.lower()
      if (searchkey in iname.lower()) or (searchkey in flavhtml.lower()) or (
          searchkey in typehtml.lower()) or (searchkey in topphtml.lower()):
        if len(flavhtml) > 0:
          flavhtml = "<b>Flavors:</b> " + flavhtml
        if len(typehtml) > 0:
          typehtml = "<b>Types:</b>" + typehtml
        if len(topphtml) > 0:
          topphtml = "<b>Toppings: </b>" + topphtml

        warn = ""
        if float(isuga) > 10:
          partyn = int(float(isuga) / 10)
          warn = "<br/>(Suitable for party of {0}+)".format(partyn)
        counter += 1
        itemhtml = """
            <tr>
            <td valign=center><img src="/static/images/{0}" alt=""  width=150px style="border-radius:5px"></td>
            <td><font size=+1><a href="/menu?iid={4}">{1}</a></font> {10} </td>
            <td>{5} <br/>{6} <br/>{7} </td>
            <td> {8} gm </td>
            <td> {9} Kcal</td>
            <td>${3}</td>
            </tr>
            """.format(iimag, iname, idesc, ipric, iiden, typehtml, flavhtml,
                       topphtml, isuga, icalo, warn)
        html += itemhtml
    else:
      if idesc == "NA":
        idesc = iname
      if iid != None:  #"NA":
        if (iid == iiden):
          if len(flavhtml) > 0:
            flavhtml = "<b>Flavors:</b> " + flavhtml
          if len(typehtml) > 0:
            typehtml = "<b>Types:</b>" + typehtml
          if len(topphtml) > 0:
            topphtml = "<b>Toppings: </b>" + topphtml

          warn = ""
          if float(isuga) > 10:
            partyn = int(float(isuga) / 10)
            warn = "<br/>(Suitable for party of {0}+)".format(partyn)
          allergy = ''
          if ("nut" in idesc.lower()) or ("nut" in flavhtml.lower()) or (
              "nut" in topphtml.lower()):
            allergy = "<font color=red><b>Allergy Information: May contain nuts. </b></font>"
          itemhtml = """
            <tr style="color:#ffffff" font-size="12px"><td bgcolor="#71322E"><b><font size=+2>{1}</font></b> {10} </td><td bgcolor="#71322E" width=20%>Health Info</td><td bgcolor="#71322E">Price</td></tr>
            <tr>
            <td><img src="/static/images/{0}" alt=""  width=300px style="border-radius:5px"><br/><br/> {2}<br/>
            <br/>{5} <br/>{6} <br/>{7} </td>
            <td valign=top><b>Sugar: {8}gm<br/>Calorie: {9}Kcal</b><br/> {11}</td>
            <td valign=top><b>${3}</td>
            </tr>
            """.format(iimag, iname, idesc, ipric, iiden, typehtml, flavhtml,
                       topphtml, isuga, icalo, warn, allergy)
          html += itemhtml
          counter = 1
          break
      else:
        if len(flavhtml) > 0:
          flavhtml = "<b>Flavors:</b> " + flavhtml
        if len(typehtml) > 0:
          typehtml = "<b>Types:</b>" + typehtml
        if len(topphtml) > 0:
          topphtml = "<b>Toppings: </b>" + topphtml
        warn = ""
        if float(isuga) > 10:
          partyn = int(float(isuga) / 10)
          warn = "<br/>(Suitable for party of {0}+)".format(partyn)
        itemhtml = """
            <tr>
            <td valign=center><img src="/static/images/{0}" alt=""  width=150px style="border-radius:5px"></td>
            <td><b><font size=+1><a href="/menu?iid={4}">{1}</a></font></b>{10}</td>
            <td>{5} <br/>{6} <br/>{7} </td>
            <td><b> {8} gm </b></td>
            <td><b> {9} Kcal</b></td>
            <td><b>${3}</td>
            </tr>
            """.format(iimag, iname, idesc, ipric, iiden, typehtml, flavhtml,
                       topphtml, isuga, icalo, warn)
        html += itemhtml

  if iid != None:  # "NA":
    if counter == 0:
      #no search results
      html += "<tr><td colspan=6>Sorry, we could not find any item in our menu matching the given keyword.</td></tr>"
    html += "</table></div><br/><br/><center><a href='/menu'><button class=cartbuttonbig> &larr; Back </button></a></center></section><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>"
  #html += "</ul></form></div>"
  else:
    html += "</table></div></section>"
  return html


###############################################################
def CurrentSugar(item_listdict, flav_listdict, topp_listdict, type_listdict,
                 sessid):
  currentsugar = 0
  currentcalor = 0
  currentcosts = 0
  filename = "sessions/{0}.txt".format(sessid)
  if exists(filename):
    cart_list_of_dict = []
    with open(filename, 'r') as file:
      for linedict in csv.DictReader(file, delimiter='|'):
        cart_list_of_dict.append(linedict)

  if (len(cart_list_of_dict) > 0):
    for line in cart_list_of_dict:
      entrid_ = line["id"]
      itemid_ = line["itemid"]
      flavid_ = line["flavid"]
      typeid_ = line["typeid"]
      toppid_ = line["toppid"]
      quanti_ = int(line["quanti"])

      if itemid_ != "None":
        for item in item_listdict:
          #itemid|itemname|itemdescription|itemunitprice|itemsugar|itemunitcalorie|itemavailableunits|itemflavorids|itemtypeids|itemtoppingids|itemimage
          iiden = item["itemid"]
          iname = item["itemname"]
          #idesc = item["itemdescription"]
          ipric = item["itemunitprice"]
          isuga = item["itemsugar"]
          icalo = item["itemunitcalorie"]
          iunit = item["itemavailableunits"]
          if itemid_ == iiden:
            sugar = float(isuga) * quanti_
            calor = float(icalo) * quanti_
            costs = float(ipric) * quanti_

            currentsugar += sugar
            currentcalor += calor
            currentcosts += costs

            if flavid_ != "None":
              for flavo in flav_listdict:
                #flavorid|flavorname|flavorprice|flavorsugar|flavorcalorie|flavoravailableunits|flavorimage
                fiden = flavo["flavorid"]
                fpric = flavo["flavorprice"]
                fsuga = flavo["flavorsugar"]
                fcalo = flavo["flavorcalorie"]

                if flavid_ == fiden:
                  sugar = float(fsuga) * quanti_
                  calor = float(fcalo) * quanti_
                  costs = float(fpric) * quanti_

                  currentsugar += sugar
                  currentcalor += calor
                  currentcosts += costs

            if typeid_ != "None":
              for typeo in type_listdict:
                #typeid|typename|typeprice|typesugar|typecalorie|typeavailableunits|typeimage
                tiden = typeo["typeid"]
                tname = typeo["typename"]
                tpric = typeo["typeprice"]
                tsuga = typeo["typesugar"]
                tcalo = typeo["typecalorie"]

                if typeid_ == tiden:
                  sugar = float(tsuga) * quanti_
                  calor = float(tcalo) * quanti_
                  costs = float(tpric) * quanti_

                  currentsugar += sugar
                  currentcalor += calor
                  currentcosts += costs

            if toppid_ != "None":
              for toppo in topp_listdict:
                #toppingid|toppingname|toppingprice|toppingsugar|toppingcalorie|toppingavailableunits|toppingimage
                piden = toppo["toppingid"]
                pname = toppo["toppingname"]
                ppric = toppo["toppingprice"]
                psuga = toppo["toppingsugar"]
                pcalo = toppo["toppingcalorie"]

                if toppid_ == piden:
                  sugar = float(psuga) * quanti_
                  calor = float(pcalo) * quanti_
                  costs = float(ppric) * quanti_

                  currentsugar += sugar
                  currentcalor += calor
                  currentcosts += costs

  return currentsugar


###############################################################
def ShowCartHTML(item_listdict, flav_listdict, topp_listdict, type_listdict,
                 itemid, flavid, typeid, toppid, quanti, sessid, suglim,
                 cartupdate, entrid):
  #READ FROM THE ITEMS.TXT AND BUILD CARDS FOR EACH ITEM AND THEN ADD THEM
  currentsugar = 0  #gm
  currentcalor = 0  #kcal
  currentcosts = 0  #$

  infofilename = "sessions/{0}-info.txt".format(sessid)
  if exists(infofilename) == False:
    line1 = "DateTime:" + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n"
    line2 = "SugarLimit:" + str(suglim) + "\n"
    username = "Guest"
    if thisuser != None:
      #user logged in
      username = thisuser["username"]
    line3 = "User:" + username + "\n"
    with open(infofilename, "w+") as fw:
      fw.write(line1)
      fw.write(line2)
      fw.write(line3)

  filename = "sessions/{0}.txt".format(sessid)
  #updating the cart based on user choice
  if cartupdate == "Update":
    print("chosen ones=")
    print(entrid)
    if (exists(filename) == True) & (len(entrid) > 0):
      cart_list_of_dict = []
      with open(filename, 'r') as file:
        for linedict in csv.DictReader(file, delimiter='|'):
          if linedict["id"] in entrid:  #if this happens then it is included
            #print(str(linedict["id"]) + " included ")
            cart_list_of_dict.append(linedict)

      line = "id|itemid|flavid|typeid|toppid|quanti"
      with open(filename, "w+") as fw:
        fw.write(line + "\n")
        for line in cart_list_of_dict:
          entrid_ = line["id"]
          itemid_ = line["itemid"]
          flavid_ = line["flavid"]
          typeid_ = line["typeid"]
          toppid_ = line["toppid"]
          quanti_ = line["quanti"]
          data = "{5}|{0}|{1}|{2}|{3}|{4}".format(itemid_, flavid_, typeid_,
                                                  toppid_, quanti_, entrid_)
          fw.write(data + "\n")

  if int(quanti) > 0:
    #first time entry with create header
    if exists(filename) == False:
      line = "id|itemid|flavid|typeid|toppid|quanti"
      data = "1|{0}|{1}|{2}|{3}|{4}".format(itemid, flavid, typeid, toppid,
                                            quanti)
      with open(filename, "w+") as fw:
        fw.write(line + "\n")
        fw.write(data + "\n")
    else:
      cart_list_of_dict = []
      with open(filename, 'r') as file:
        for linedict in csv.DictReader(file, delimiter='|'):
          cart_list_of_dict.append(linedict)
      counter = len(cart_list_of_dict) + 1
      data = "{5}|{0}|{1}|{2}|{3}|{4}".format(itemid, flavid, typeid, toppid,
                                              quanti, counter)
      with open(filename, "a+") as fa:
        fa.write(data + "\n")

  #first time create header with no quantity
  if int(quanti) == 0:
    if exists(filename) == False:
      line = "id|itemid|flavid|typeid|toppid|quanti"
      with open(filename, "w+") as fw:
        fw.write(line + "\n")

  #finally reading it...
  #we should not use else here - use if exists again...
  if exists(filename):
    cart_list_of_dict = []
    with open(filename, 'r') as file:
      for linedict in csv.DictReader(file, delimiter='|'):
        cart_list_of_dict.append(linedict)

  html = ""
  if (cartupdate == "Finalize") or (cartupdate == "Update") or (
      cartupdate == "SendEmail"):  #Finalize part
    header = """
        <a name="order"></a>
        <div class=orderheader><b>Order: {0} (Sugar limit: {1}gm)</b></div><hr/>
        <table border=0 cellpadding=5 cellspacing=5 width=100%>
    """.format(sessid, suglim)
  else:
    header = """
        <a name="order"></a>
        <div class=orderheader><b>Order: {0} (Sugar limit: {1}gm)</b></div><hr/>
        <table border=0 cellpadding=0 cellspacing=0 width=95%>
    """.format(sessid, suglim)
  html += header

  if cartupdate == "Update":
    html += "<form name=order action=/order method=POST>"

  if (len(cart_list_of_dict) > 0):
    for line in cart_list_of_dict:
      entrid_ = line["id"]
      itemid_ = line["itemid"]
      flavid_ = line["flavid"]
      typeid_ = line["typeid"]
      toppid_ = line["toppid"]
      quanti_ = int(line["quanti"])

      if itemid_ != "None":
        for item in item_listdict:
          #itemid|itemname|itemdescription|itemunitprice|itemsugar|itemunitcalorie|itemavailableunits|itemflavorids|itemtypeids|itemtoppingids|itemimage
          iiden = item["itemid"]
          iname = item["itemname"]
          #idesc = item["itemdescription"]
          ipric = item["itemunitprice"]
          isuga = item["itemsugar"]
          icalo = item["itemunitcalorie"]
          iunit = item["itemavailableunits"]
          #iflas = item["itemflavorids"]
          #ityps = item["itemtypeids"]
          #itops = item["itemtoppingids"]
          #iimag = item["itemimage"]

          if itemid_ == iiden:
            sugar = round(float(isuga) * quanti_, 2)
            calor = round(float(icalo) * quanti_, 2)
            costs = round(float(ipric) * quanti_, 2)
            if cartupdate == "Update":
              html += "<tr><td><input type=checkbox name=entrid value={5} checked> &nbsp;[{0}] <b>{1}</b> <br/>&nbsp;&nbsp;<i>(Sugar:{2}, Calorie:{3})</i></td><td>: ${4} </td></tr>".format(
                quanti_, iname, sugar, calor, costs, entrid_)
            else:
              html += "<tr><td> [{0}] <b>{1}</b> <br/>&nbsp;&nbsp;<i>(Sugar:{2}, Calorie:{3})</i></td><td>: ${4} </td></tr>".format(
                quanti_, iname, sugar, calor, costs)

            currentsugar += sugar
            currentcalor += calor
            currentcosts += costs

            if flavid_ != "None":
              for flavo in flav_listdict:
                #flavorid|flavorname|flavorprice|flavorsugar|flavorcalorie|flavoravailableunits|flavorimage
                fiden = flavo["flavorid"]
                fname = flavo["flavorname"]
                fpric = flavo["flavorprice"]
                fsuga = flavo["flavorsugar"]
                fcalo = flavo["flavorcalorie"]
                #funit = flavo["flavoravailableunits"]
                #fimag = flavo["flavorimage"]
                if flavid_ == fiden:
                  sugar = float(fsuga) * quanti_
                  calor = float(fcalo) * quanti_
                  costs = float(fpric) * quanti_
                  html += "<tr><td>&nbsp;&nbsp;of Flavor: {1}<br/>&nbsp;&nbsp;<i>(Sugar:{2}, Calorie:{3})</i></td><td>: ${4} </td></tr>".format(
                    quanti_, fname, sugar, calor, costs)

                  currentsugar += sugar
                  currentcalor += calor
                  currentcosts += costs

            if typeid_ != "None":
              for typeo in type_listdict:
                #typeid|typename|typeprice|typesugar|typecalorie|typeavailableunits|typeimage
                tiden = typeo["typeid"]
                tname = typeo["typename"]
                tpric = typeo["typeprice"]
                tsuga = typeo["typesugar"]
                tcalo = typeo["typecalorie"]
                #tunit = typeo["typeavailableunits"]
                #timag = typeo["typeimage"]
                if typeid_ == tiden:
                  sugar = float(tsuga) * quanti_
                  calor = float(tcalo) * quanti_
                  costs = float(tpric) * quanti_
                  html += "<tr><td>&nbsp;&nbsp;of Type: {1} <br/>&nbsp;&nbsp;<i>(Sugar:{2}, Calorie:{3})</i> </td><td>: ${4} </td></tr>".format(
                    quanti_, tname, sugar, calor, costs)

                  currentsugar += sugar
                  currentcalor += calor
                  currentcosts += costs

            if toppid_ != "None":
              for toppo in topp_listdict:
                #toppingid|toppingname|toppingprice|toppingsugar|toppingcalorie|toppingavailableunits|toppingimage
                piden = toppo["toppingid"]
                pname = toppo["toppingname"]
                ppric = toppo["toppingprice"]
                psuga = toppo["toppingsugar"]
                pcalo = toppo["toppingcalorie"]
                #punit = toppo["toppingavailableunits"]
                #pimag = toppo["toppingimage"]
                if toppid_ == piden:
                  sugar = float(psuga) * quanti_
                  calor = float(pcalo) * quanti_
                  costs = float(ppric) * quanti_
                  html += "<tr><td>&nbsp;&nbsp;with Topping: {1} <br/>&nbsp;&nbsp;<i>(Sugar:{2}, Calories:{3})</i> </td><td>: ${4} </td></tr>".format(
                    quanti_, pname, sugar, calor, costs)

                  currentsugar += sugar
                  currentcalor += calor
                  currentcosts += costs

    currentcosts = round(currentcosts, 2)
    html += "<tr><td colspan=2><hr></td></tr><tr><td><b>Total Sugar: </b></td><td>{0}gm </td></tr>".format(
      currentsugar)
    html += "<tr><td>Total Calories: </td><td>{0}Kcal </td></tr>".format(
      currentcalor)
    html += "<tr><td>Total Cost: </td><td>${0}</td></tr>".format(currentcosts)

    if cartupdate == "Update":
      cshtml = SugarProgress(currentsugar, suglim, 300, True)
      html += """<tr><td>
            <input type=hidden name=sessid value={0}>
            <input type=hidden name=cartup value={1}>
            <input type=hidden name=suglim value={2}>
            <button class="cartbuttonbig" onclick=this.form.submit()> Update the cart</button></form></td>
            """.format(sessid, "Update", suglim)
      html += """<td><form name=order action=/order method=GET>
              <input type=hidden name=sessid value={0}>
              <input type=hidden name=cartup value={1}>
              <input type=hidden name=suglim value={2}>
              <button onclick=this.form.submit()> Finalize </button></form></td></tr>
              """.format(sessid, "Finalize", suglim)
      html += "<tr><td colspan=2 align=center>{0}</td></tr>".format(cshtml)
      html += "<tr><td colspan=2 align=center><br/><a href=/order?sessid={0}&cartup=Started&suglim={1}><button class=cartbuttonbig>Back to Order Page</button></a></td></tr>".format(
        sessid, suglim)
    elif (cartupdate == "Finalize"):
      cshtml = SugarProgress(currentsugar, suglim, 300, True)
      html2 = """<tr><td colspan=2><form name=order action=/order method=GET>
            <input type=hidden name=sessid value={0}>
            <input type=hidden name=cartup value={1}>
            <input type=hidden name=suglim value={2}>
            <button class="cartbuttonbig" onclick=this.form.submit()> Update the cart</button></form></td></tr>
            """.format(sessid, "Update", suglim)

      html += "<tr><td colspan=2 align=center><hr/>{0}</td></tr>".format(
        cshtml)
      html += "<tr><td colspan=2 align=center><a href=/order?sessid={0}&cartup=Started&suglim={1}><button class=cartbuttonbig>Back to Order Page</button></a></td></tr>".format(
        sessid, suglim)

      useremail = None
      username = "Guest"
      emailinputshown = '<input type=text size=30 name=email>'
      usernameinputshown = '<input type=text size=30 name=user>'
      if thisuser != None:
        useremail = thisuser["email"]
        username = thisuser["username"]
        #print(username)
      if useremail != None:
        emailinputshown = '{0} <input type=hidden name=email value={0}> '.format(
          useremail)
        usernameinputshown = '{0} <input type=hidden name=user value={0}> '.format(
          username)

      html += """<tr><td colspan=2><hr><br/></td></tr>
            <tr><td colspan=2><form name=order action=/order method=GET>
            <input type=hidden name=sessid value={0}>
            <input type=hidden name=cartup value={1}>
            <input type=hidden name=suglim value={2}>
            
            <tr><td> Username: </td><td>{3}</td></tr>
            <tr><td> Email: </td><td>{4}</td></tr>
            <tr><td> Message: </td><td><input type=text size=30 name=mesg></td></tr>
            <tr><td colspan=2  align=center><button class="cartbuttonbig" onclick=this.form.submit()> Buy (Send Email) </button></form></td></tr>
            """.format(sessid, "SendEmail", suglim, usernameinputshown,
                       emailinputshown)
    elif (cartupdate == "SendEmail"):
      cshtml = SugarProgress(currentsugar, suglim, 300, True)

      html += "<tr><td colspan=2 align=center><hr/>{0}</td></tr>".format(
        cshtml)
      #html += "<tr><td colspan=2 align=center><a href=/order?sessid={0}&cartup=Started&suglim={1}><button class=cartbuttonbig>Back to Order Page</button></a></td></tr>".format(sessid,suglim)
    else:
      cshtml = SugarProgress(currentsugar, suglim, 250, True)
      html += """<tr><td><br/><form name=order action=/order method=GET>
              <input type=hidden name=sessid value={0}>
              <input type=hidden name=cartup value={1}>
              <input type=hidden name=suglim value={2}>
              <button class="cartbuttonsmall" onclick=this.form.submit()> Update </button></form><br/></td>
              """.format(sessid, "Update", suglim)

      html += """<td><form name=order action=/order method=GET>
              <input type=hidden name=sessid value={0}>
              <input type=hidden name=cartup value={1}>
              <input type=hidden name=suglim value={2}>
              <button class="cartbuttonsmall" onclick=this.form.submit()> Finalize </button></form></td></tr>
              """.format(sessid, "Finalize", suglim)
      html += "<tr><td colspan=2>{0}</td></tr>".format(cshtml)

    html += "</table>"
  else:
    html += '<tr><td colspan=2>Please Start Adding Items </td></tr></table>'
  return (currentsugar, currentcalor, currentcosts, html)


################################################################
def ShowAllItems(item_listdict, flav_listdict, topp_listdict, type_listdict,
                 sessid, suglim):
  #READ FROM THE ITEMS.TXT AND BUILD CARDS FOR EACH ITEM AND THEN ADD THEM
  html = ""
  header = """
  <section class="health_section layout_padding">
    <div class="container">
      <div class="custom_heading-container ">
        <h2>
        Bakery Order Form
        </h2>
      </div>
      <br/>
      <table border=0 cellpadding=5 cellspacing=5 width=100%>
      <tr><td colspan=2 style="border-top: solid 1px;"></tr>
      </table>
      <center>
      <table border=0 cellpadding="5" cellspacing = "5" width="100%">
  """
  html += header

  qtyselect = """
    <option value="1">1</option>
    <option value="2">2</option>
    <option value="3">3</option>
    <option value="4">4</option>
    <option value="5">5</option>
    <option value="6">6</option>
    <option value="7">7</option>
    <option value="8">8</option>
    <option value="9">9</option>
    <option value="10">10</option>
  """

  counter = 0
  for item in item_listdict:
    #itemid|itemname|itemdescription|itemunitprice|itemsugar|itemunitcalorie|itemavailableunits|itemflavorids|itemtypeids|itemtoppingids|itemimage
    iiden = item["itemid"]
    iname = item["itemname"]
    idesc = item["itemdescription"]
    ipric = item["itemunitprice"]
    isuga = item["itemsugar"]
    icalo = item["itemunitcalorie"]
    iunit = item["itemavailableunits"]
    iflas = item["itemflavorids"]
    ityps = item["itemtypeids"]
    itops = item["itemtoppingids"]
    iimag = item["itemimage"]

    #creating the select drop down menu for flavors - IF ANY
    flavhtml = ""
    if iflas != "NA":
      flavhtml = '<select name="flavor" id="id_flavor">'
      flavids = iflas.split(',')
      for flavo in flav_listdict:
        #flavorid|flavorname|flavorprice|flavorsugar|flavorcalorie|flavoravailableunits|flavorimage
        fiden = flavo["flavorid"]
        fname = flavo["flavorname"]
        fpric = flavo["flavorprice"]
        fsuga = flavo["flavorsugar"]
        fcalo = flavo["flavorcalorie"]
        funit = flavo["flavoravailableunits"]
        fimag = flavo["flavorimage"]
        if fiden in flavids:
          flavhtml += '<option value="{0}">{1}</option>'.format(fiden, fname)
      flavhtml += "</select>&nbsp;"

    #creating the select drop down menu for types - IF ANY
    typehtml = ""
    if ityps != "NA":
      typehtml = '<select name="type" id="id_type">'
      typeids = ityps.split(',')
      for typeo in type_listdict:
        #typeid|typename|typeprice|typesugar|typecalorie|typeavailableunits|typeimage
        tiden = typeo["typeid"]
        tname = typeo["typename"]
        tpric = typeo["typeprice"]
        tsuga = typeo["typesugar"]
        tcalo = typeo["typecalorie"]
        tunit = typeo["typeavailableunits"]
        timag = typeo["typeimage"]
        if tiden in typeids:
          typehtml += '<option value="{0}">{1}</option>'.format(tiden, tname)
      typehtml += "</select>&nbsp; "

    #creating the select drop down menu for toppings - IF ANY
    topphtml = ""
    if itops != "NA":
      topphtml = '<select name="topping" id="id_topping">'
      toppids = itops.split(',')
      for toppo in topp_listdict:
        #toppingid|toppingname|toppingprice|toppingsugar|toppingcalorie|toppingavailableunits|toppingimage
        piden = toppo["toppingid"]
        pname = toppo["toppingname"]
        ppric = toppo["toppingprice"]
        psuga = toppo["toppingsugar"]
        pcalo = toppo["toppingcalorie"]
        punit = toppo["toppingavailableunits"]
        pimag = toppo["toppingimage"]
        if piden in toppids:
          topphtml += '<option value="{0}">{1}</option>'.format(piden, pname)
      topphtml += "</select>&nbsp; "

    if idesc == "NA":
      idesc = iname
    if counter % 3 == 0:
      html += "<tr>"

    typeheader = ""
    flavheader = ""
    toppheader = ""
    if len(typehtml) > 0:
      typeheader = "Types:"
    if len(flavhtml) > 0:
      flavheader = "Flavors:"
    if len(topphtml) > 0:
      toppheader = "Toppings:"
    warn = ""
    if float(isuga) > 10:
      partyn = int(float(isuga) / 10)
      warn = "(Suitable for party of {0}+)".format(partyn)
    itemhtml = """
          <td>
          <div class="box">
            <div class="btn_container"><b>{9}gm / {10}Kcal</b></div>
            <div class="img-box"><img src="/static/images/{0}" alt=""></div>

            <form name="orderform" method="GET" action="/order">
              <input type=hidden name=itemid value={4}>
              <input type=hidden name=sessid value={11}>
              <input type=hidden name=suglim value={12}>
              <input type=hidden name=cartup value="Ongoing">
              <b><font size=+1>{1}</font></b> ${3} <i>{16}</i>
              <table cellpadding=1 cellspacing=2 width=80%>
              <tr><td>{13}</td><td>{6}</td></tr>
              <tr><td>{14}</td><td>{7}</td></tr>
              <tr><td>{15}</td><td>{8}</td></tr>
              <tr><td>Quantity:</td><td><select name=qty id=qty> {5} </select> &nbsp; <button> Add </a></button></td></tr>
              </table>                 
            </form>
          </div></td>
          """.format(iimag, iname, idesc, ipric, iiden, qtyselect, typehtml,
                     flavhtml, topphtml, isuga, icalo, sessid, suglim,
                     typeheader, flavheader, toppheader, warn)
    html += itemhtml
    counter += 1
    if counter % 3 == 0:
      html += "</tr>"

  #html += "</ul></form></div>"
  html += "</table></div></section>"
  return html


########################################################################
def SugarProgress(cs, suglim, size, warningShow):
  perc = int((int(cs) * 100) / (int(suglim)))
  #print(cs)
  #print(suglim)
  #print(perc)
  warning = ''
  if warningShow == True:
    if (int(cs) > int(suglim)):
      warning += "<tr><td><font color=red>You are over your Sugar quota by: {0}gm. Please consider removing some item(s).</font>".format(
        (int(cs) - int(suglim)))
    if (perc >= 40) & (perc < 50):
      warning += "<tr><td><font>You are almost halfway of your sugar limit.</font>"
    if (perc >= 50) & (perc < 75):
      warning += "<tr><td><font>You are over halfway of your sugar limit.</font>"
    if (perc >= 75) & (perc < 90):
      warning += "<tr><td><font>You are over 3/4 th of your sugar limit.</font>"
    if (perc >= 90) & (perc < 100):
      warning += "<tr><td><font color=darkred>You are getting close to your limit.</font>"

  html = ""
  if size > 250:
    html = """
     <table width={3}px><tr><td>
          SugarBar:  {0}% of {1}gm total<br/>
          <progress max="100" value="{0}" class="html5" style="height:20px">
          <div class="progress-bar"><span style="width: {0}%">{0}%</span</div>
          </progress>
        </td></tr>
        {2}
        </table>
    """.format(perc, suglim, warning, size)

  if size <= 250:
    html = """
     <table width={3}px><tr><td>
          SugarBar:  {0}% of {1}gm total<br/>
          <progress max="100" value="{0}" class="html5" style="height:15px">
          <div class="progress-bar"><span style="width: {0}%">{0}%</span</div>
          </progress>
        </td></tr>
        {2}
        </table>
    """.format(perc, suglim, warning, size)

  return html


################################################################
@app.route('/order', methods=['GET', 'POST'])
def order():
  cartupdate = ""
  if request.method == 'POST':
    cartupdate = request.form.get('cartup')
    sessionid = request.form.get('sessid')
    sugarlimit = request.form.get('suglim')
    entryids = request.form.getlist('entrid')

  if request.method == 'GET':
    cartupdate = request.args.get('cartup')
    itemid = request.args.get("itemid")
    flavid = request.args.get("flavor")
    typeid = request.args.get("type")
    toppid = request.args.get("topping")
    quanti = request.args.get("qty")

    sessionid = request.args.get('sessid')
    sugarlimit = request.args.get("suglim")

    user = request.args.get('user')
    email = request.args.get('email')
    mesg = request.args.get('mesg')

    entryids = []

  item_listdict = readitems()
  flav_listdict = readflavors()
  topp_listdict = readtoppings()
  type_listdict = readtypes()

  suglim = 0
  #sugarlimit has to be an integer
  try:
    suglim = int(sugarlimit)
  except:
    suglim = 0

  #this is the beginning of creating an order session or in other words, starting the order. All order ids are basically same as sessionid
  #so, in all purposes in this project, "order id" is also called "session id"
  if suglim == 0:
    #show the form to enter sugarlimit
    html = """
          <section class="about_section layout_padding">
          <div class="container">
          <div class="custom_heading-container ">
            <h2>
              Bakery Products Order Form
            </h2>
          </div>
        <br/>
        <table border=0 cellpadding=5 cellspacing=5 width=100%>
        <tr><td colspan=2 style="border-top: solid 1px;"></tr>
        </table>
        """
    sessionid = request.cookies.get("sessid")

    if (sessionid != None):
      if (len(sessionid) > 0):
        (dt, sm, us, em, st) = GetSessionInfo(sessionid)

        html += """
            <b> <h4>Continue with existing order</h4></b><br/>We see that you started an order on {2} with order id = <b>{0}</b><br/>
            {3}
            <div class="d-flex justify-content-center">
            <a href="/order?sessid={0}&cartup=Started&suglim={1}">
              <button class=cartbuttonbig>Continue With This Order </button> 
          </a>
          </div><br/>
          <h4>OR</h4>
        """.format(
          sessionid, sm, dt,
          SugarProgress(
            CurrentSugar(item_listdict, flav_listdict, topp_listdict,
                         type_listdict, sessionid), sm, 300, False))

    newsessionid = random.randint(10000000000000, 90000000000000)
    filename = "sessions/{0}.txt".format(newsessionid)
    #making sure it does not exist already
    while exists(filename):
      newsessionid = random.randint(10000000000000, 90000000000000)
      filename = "sessions/{0}.txt".format(newsessionid)

    html += """    
          <form name="orderform" method="POST" action="/order">
          <input type=hidden name=sessid value={0}>
          <input type=hidden name=cartup value="Started">
          <table cellpadding="5" cellspacing="5" width="100%" id="login" border=0>
            <tr><td colspan=2><b> <h4>Start a new order. </h4> <br/>To start a new order please mention your health goal (regarding sugar) </b></td></tr>

            <tr><td colspan=2 align=center>
            
            <table cellpadding="10" cellspacing="5" width="100%" id="login" border=0><tr>
               <td valign=top  align=center > 
               <b>Sugar Suggestion calculator :</b><br/>
              (Here is a quick calculator for you. Please mention how many people you are ordering for and we can suggest the amount.)<br/>
              Number of people you are ordering for: 
              <select name="sc" onchange="if (this.selectedIndex) document.getElementById('suggest').value = 10 * this.selectedIndex; ">
                <option value="-1">--</option>
                <option value="1">1 Person</option> 
                <option value="2">2 People</option>
                <option value="3"> 3 People</option>
                <option value="4"> 4 People</option> 
                <option value="5"> 5 People</option>
                <option value="6"> 6 People</option>
                <option value="7"> 7 People</option> 
                <option value="8"> 8 People</option>
                <option value="9"> 9 People</option>
                <option value="10"> 10 People</option> 
                <option value="11"> 11 People</option>
                <option value="12"> 12 People</option>
                <option value="13"> 13 People</option> 
                <option value="14"> 14 People</option>
                <option value="15"> 15 People</option>
                <option value="16"> 16 People</option> 
                <option value="17"> 17 People</option>
                <option value="18"> 18 People</option>
                <option value="19"> 19 People</option> 
                <option value="20"> 20 People</option>
                <option value="21"> 21 People</option>
                <option value="22"> 22 People</option> 
                <option value="23"> 23 People</option>
                <option value="24"> 24 People</option>
                <option value="25"> 25 People</option>

             </select>
               </td>
               
               <td align=center width=50% valign=top>
               <b>How much sugar you want to consume (from this order):</b> <br/> 
               <input type="text" placeholder="Enter amount in" name="suglim" id="suggest" required size=12> gm  &nbsp; &nbsp; <button onclick=this.form.submit()> Start Order </a></button></td>
               
               
               </tr>
            </table>

            <tr><td colspan=2> <br/><br/> <table class=table-rounded-corners style="background:#cccccc"><tr><td> 
            We feel it is worth mentioning a guideline regarding a healthy sugar
            consumption of human being. <br/>
            We should intake between 20-36gms of added sugar per day. Added sugar is any sugar that is not 
            found naturally in foods (like in a fruit). <br/><br/>

            When you buy from us and you are asked to mention above how much sugar you want to limit yourself for this order,
            it is not meant to restrict you between 20-36gms of sugar. This is because we understand that this order might be
            meant for a party or for all your family members/friends. So if you are buying for more than one person and/or for 
            consumption by one person spanning several days then you are free to enter whatever number suits your need. <br/><br/>

            However, once the sugar limit is entered, we will keep track of the sugar from the added items in cart and will give you friendly 
            alert(s) if the total sugar content from all the items in cart comes close to or goes beyond
            the limit you yourself set here. <br/><br/>

            And we are happy to help you in a friendly manner like this.</td></tr></table>
            </td></tr>
            </table></form>
          </center>
          </div>
          
          </div></section>
      """.format(newsessionid)

    #return render_template('order.html', orderformhtml=html, carthtml='')
    return render_template('template.html',
                           contenthtml=html,
                           carthtml='',
                           useraccounthtml=GetUserAccountHTML(None, None))

  else:
    #create cart and keep track of sugar (mainly) and calorie
    currentsugar = 0  #gm
    currentcalor = 0  #kcal
    currentcosts = 0  #$

    if cartupdate == "Started":
      (currentsugar, currentcalor, currentcosts, carthtml) = ShowCartHTML(item_listdict, flav_listdict, topp_listdict, type_listdict,\
                                                                          "NA", "NA","NA","NA",0, sessionid,suglim, "Started", [])
      if len(carthtml) > 0:
        carthtml = '<div class="cartdiv">{0}</div>'.format(carthtml)

      #READ FROM THE ITEMS.TXT AND BUILD CARDS FOR EACH ITEM AND THEN ADD THEM
      html = ShowAllItems(item_listdict, flav_listdict, topp_listdict,
                          type_listdict, sessionid, suglim)
      resp = make_response(
        #render_template('order.html', orderformhtml=html, carthtml=carthtml))
        render_template('template.html',
                        contenthtml=html,
                        carthtml=carthtml,
                        useraccounthtml=GetUserAccountHTML(None, None)))
      resp.set_cookie("sessid", sessionid, max_age=30 * 60)
      #resp.set_cookie("suglim", suglim)

      #update the useraccount for currentsessionif and orders list
      username = "Guest"
      if thisuser != None:
        username = thisuser["username"]
        if (username != None) & (username != "Guest"):
          #update the order info
          thisuser["currentsessionid"] = sessionid
          oldorders = thisuser["orders"]
          if sessionid not in oldorders:
            thisuser["orders"] = oldorders + "," + sessionid
          ret = SaveAllUsers()
      ## TODO: if ret = SaveAllUsers() fails the we need to show an error message
      return resp

    if cartupdate == "Ongoing":
      (currentsugar, currentcalor, currentcosts, carthtml) = ShowCartHTML(item_listdict, flav_listdict, topp_listdict, type_listdict,\
                                                                          itemid, flavid,typeid,toppid,quanti, sessionid,suglim, "Ongoing", [])
      carthtml = '<div class="cartdiv">{0}</div>'.format(carthtml)
      #READ FROM THE ITEMS.TXT AND BUILD CARDS FOR EACH ITEM AND THEN ADD THEM
      html = ShowAllItems(item_listdict, flav_listdict, topp_listdict,
                          type_listdict, sessionid, suglim)
      #print(html)
      #return render_template('order.html', orderformhtml=html, carthtml=carthtml)
      return render_template('template.html',
                             contenthtml=html,
                             carthtml=carthtml,
                             useraccounthtml=GetUserAccountHTML(None, None))

    if cartupdate == "Update":
      #we should create a form to send email
      (currentsugar, currentcalor, currentcosts, carthtml) = ShowCartHTML(item_listdict, flav_listdict, topp_listdict, type_listdict,\
                                                                          "NA", "NA","NA","NA", 0, sessionid,suglim, "Update", entryids )
      html = """
          <section class="about_section layout_padding">
          <div class="container">
          <div class="custom_heading-container ">
            <h2>
              Your Current Order With Us (Order: {0})
            </h2>
          </div>
        <br/>
        <table border=0 cellpadding=5 cellspacing=5 width=100%>
        <tr><td colspan=2 style="border-top: solid 1px;"></tr>
        </table>
        """.format(sessionid, suglim)

      carthtml_ = html + '<center><div class="cartdivfinal"><table width=80%><tr><td>{0}</td></tr></table><br/></center></div></section><br/><br/>'.format(
        carthtml)
      #return render_template('order.html',orderformhtml=carthtml_,carthtml='')
      return render_template('template.html',
                             contenthtml=carthtml_,
                             carthtml='',
                             useraccounthtml=GetUserAccountHTML(None, None))

    if cartupdate == "Finalize":
      #we should create a form to send email
      (currentsugar, currentcalor, currentcosts, carthtml) = ShowCartHTML(item_listdict, flav_listdict, topp_listdict, type_listdict,\
                                                                          "NA", "NA","NA","NA", 0, sessionid,suglim, "Finalize", [] )
      html = """
          <section class="about_section layout_padding">
          <div class="container">
          <div class="custom_heading-container ">
            <h2>
              Final Step (Send Your Order) (# {0})
            </h2>
          </div>
        <br/>
        <table border=0 cellpadding=5 cellspacing=5 width=100%>
        <tr><td colspan=2 style="border-top: solid 1px;"></tr>
        </table>
        """.format(sessionid, suglim)
      carthtml_ = html + '<center><div class="cartdivfinal"><table width=80%><tr><td>{0}</td></tr></table><br/></center></div></section><br/><br/>'.format(
        carthtml)
      #return render_template('order.html',orderformhtml=carthtml_, carthtml='')
      return render_template('template.html',
                             contenthtml=carthtml_,
                             carthtml='',
                             useraccounthtml=GetUserAccountHTML(None, None))

    if cartupdate == "SendEmail":
      #we should create a form to send email
      (currentsugar, currentcalor, currentcosts, carthtml) = ShowCartHTML(item_listdict, flav_listdict, topp_listdict, type_listdict,\
                                                                          "NA", "NA","NA","NA", 0, sessionid,suglim, "SendEmail", [] )
      html = """
          <section class="about_section layout_padding">
          <div class="container">
          <div class="custom_heading-container ">
            <h2>
              Your Order Is Being Submitted
            </h2>
          </div>
        <br/>
        <table border=0 cellpadding=5 cellspacing=5 width=100%>
        <tr><td colspan=2 style="border-top: solid 1px;"></tr>
        </table>
        """
      emailhtml = '<table width=80%><tr><td>{0}</td></tr></table><br/><br/>-Yours Truly<br/>Bake N\'Take Team<br/>'.format(
        carthtml)

      try:
        SendEmail(toemail=email,
                  tosubj="Order #" + sessionid,
                  totext="Your order has been submitted",
                  tohtml=emailhtml)

        infofilename = "sessions/{0}-info.txt".format(sessionid)
        if exists(infofilename) == True:
          (dat_, sug_, use_, emai_, sta_) = GetSessionInfo(sessionid)
          line1 = "DateTime:" + datetime.now().strftime(
            "%m/%d/%Y, %H:%M:%S") + "\n"
          line2 = "SugarLimit:" + str(sug_) + "\n"
          line3 = "User:" + use_ + "\n"
          line4 = "Email:" + email + "\n"
          line5 = "Status: Complete\n"
          with open(infofilename, "w+") as fw:
            fw.write(line1)
            fw.write(line2)
            fw.write(line3)
            fw.write(line4)
            fw.write(line5)

          if thisuser != None:
            UpdateCurrentSessionIdForUser(thisuser["username"], 'NA')

        finalhtml_ = html + """
          Thank you for your patience. The order has been submitted and you will receive an email from Bake N' Take team.<br/><br/>
          It has been a pleasure serving you. <br/><br/>Please come again. <br/> <img src="/static/images/donut.png" width=150px></div></section><br/><br/><br/><br/><br/><br/><br/><br/>
          """
        resp = make_response(
          #render_template('order.html', orderformhtml=finalhtml_, carthtml=''))
          render_template('template.html',
                          contenthtml=finalhtml_,
                          carthtml='',
                          useraccounthtml=GetUserAccountHTML(None, None)))

        resp.set_cookie("sessid", '', max_age=0)
      except Exception as e:
        finalhtml_ = html + """<font color=red>Uh-Oh!!!! It's not you. It's us. There is a technical difficulty  <br/><br/>We will get back to you as soon as we can. 
          {0}</font><img src="/static/images/donut.png" width=150px></div></section><br/><br/><br/><br/><br/><br/><br/><br/>""".format(
          str(e))
        resp = make_response(
          #render_template('order.html', orderformhtml=finalhtml_, carthtml=''))
          render_template('template.html',
                          contenthtml=finalhtml_,
                          carthtml='',
                          useraccounthtml=GetUserAccountHTML(None, None)))

      return resp


################################################################
def RatingHtml(rating):
  html = """
  <div class="star_container">
    """
  fullval = float(rating)
  fraction = float(rating) - int(fullval)
  fullval = int(fullval)

  for r in range(0, fullval):
    html += '<i class="fa fa-star" aria-hidden="true"></i>'

  if fraction > 0:
    html += '<i class="fa fa-star-half-o" aria-hidden="true"></i>'

  for r in range(fullval + 1, 5):
    html += '<i class="fa fa-star-o" aria-hidden="true"></i>'

  html += """
  </div>
  """
  return html


###################################################################
def ReviewFormHTML():
  user = GetUserAccountName(None, None)
  email = GetUserAccountEmail(None, None)
  html = """
      <hr/><form action=/reviews method=POST>
      <table border=0 cellpadding=30 cellspacing=0 width=90%>
      <tr><td width=100%><table border=0 cellpadding=5 cellspacing=5 width=100%>
      <tr><td colspan=2><b><h3>Please write a review for us </h3></b></td></tr>
      <tr><td> Username: </td><td><input type=text size=30 name=user value={0}></td></tr>
      <tr><td> Email: </td><td><input type=text size=30 name=email value={1}></td></tr>
      <tr><td> Rating: </td><td><select name=rating>
        <option value="0">0</option>
        <option value="0.5">0.5</option>
        <option value="1">1</option>
        <option value="1.5">1.5</option>
        <option value="2">2</option>
        <option value="2.5">2.5</option>
        <option value="3">3</option>
        <option value="3">3.5</option>
        <option value="4">4</option>
        <option value="4.5">4.5</option>
        <option value="5">5</option>
      </select>
      </td></tr>
      <tr><td> Review Text: </td><td><input type=text size=100 name=message></td></tr>
      <tr><td>&nbsp; </td><td><button class="cartbuttonbig" onclick=this.form.submit()> Send Your Review </button></td></tr>
      </table></td></tr>
      </table></form>
  """.format(user, email)
  return html


################################################################
@app.route('/reviews', methods=['GET', 'POST'])
def reviews():

  filename = "reviews/reviews.txt"
  newreviewcame = False
  if request.method == 'POST':
    newuser = request.form.get('user')
    newemail = request.form.get('email')
    newrating = request.form.get('rating')
    newmessage = request.form.get('message')
    newreviewcame = True

  if newreviewcame == True:
    #add the review
    #username|email|datetime|rating|message
    dt = date.today()
    dts = dt.strftime("%m/%d/%Y")
    data = "{0}|{1}|{2}|{3}|{4}".format(newuser, newemail, dts, newrating,
                                        newmessage)
    with open(filename, "a+") as fa:
      fa.write(data + "\n")
    done = True

  ### show all the reviews
  html = ""
  header = """
<section class="health_section layout_padding">
  <div class="container">
    <div class="custom_heading-container ">
      <h2>Your Comments Inspire Us</h2>
    </div>
    <br/>
    <table border=0 cellpadding=5 cellspacing=5 width=100%>
      <tr><td colspan=2 style="border-top: solid 1px;"></tr>
    </table>
    <center><br/><table cellpadding="5" cellspacing = "5" width="90%" font-size="12px" class="table-rounded-corners">
    <tr style="color:#ffffff" font-size:12px><td bgcolor="#71322E" width=15%>Rating</td><td bgcolor="#71322E" width=20%>Date</td><td bgcolor="#71322E" width=65%>Message </td></tr>
"""
  html += header

  if exists(filename):
    review_list_of_dict = []
    with open(filename, 'r') as file:
      for linedict in csv.DictReader(file, delimiter='|'):
        review_list_of_dict.append(linedict)
    for review in review_list_of_dict:
      #username|email|datetime|rating|message
      user = review["username"]
      email = review["email"]
      datetime = review["datetime"]
      rating = review["rating"]
      message = review["message"]

      ratinghtml = RatingHtml(rating=rating)

      reviewhtml = """
      <tr><td>{0}</td><td>{1}</td><td><b>{2}</b> Wrote: <br/><br/> <font color=blue><i>"{3}"</i></font></td></tr>
      """.format(ratinghtml, datetime, user, message)

      html += reviewhtml

    html += "</table></center><br/>"
    html += ReviewFormHTML()

    html += "</div></section>"
    return render_template('template.html',
                           contenthtml=html,
                           useraccounthtml=GetUserAccountHTML(None, None))
  else:
    html += "<tr><td colspan=3>Sorry! Currently, no reviews are available for view.</td></tr></table></center><br/>"
    html += ReviewFormHTML()
    html += "</div></section>"
    return render_template('template.html',
                           contenthtml=html,
                           useraccounthtml=GetUserAccountHTML(None, None))


def AreMostPhrasesThereInMessage(phraselist, tokens):
  print("---------------------------------------------------------")
  print(phraselist)
  print(" -- in -- ")
  print(tokens)
  totalphrases = len(phraselist)
  counter = 0
  for phrase in phraselist:
    if phrase in tokens:
      counter += 1
  print(counter)
  return counter  #(totalphrases/2)


def IsImportantPhraseInMessage(phrase, tokens):
  return phrase in tokens


@app.route("/get", methods=["GET", "POST"])
def chatbot_response():
  msg = request.form["msg"]
  #response = chatbot.get_response(msg)
  response = "Actually I am not sure what to tell you. Sorry! I am still learning. "
  #rule based messaging - first breaking the sentence into tokens
  msg = re.sub('\!|\?|\.|,|\'|\"', r'', msg)
  tokens = re.split(r'\s+', msg.lower())

  #match the tokens
  #location related

  #contact related

  #menu related

  #order related

  #account related

  alltuples = [
    (['hello', 'hola', 'hey', 'hi'], "Hello! How are you doing?"),
    (['how', 'you', 'are'], "Doing good! Thanks! How may I help you?"),
    (['doing', 'good', 'am'], "Good good! What can I help you with today?"),
    (['need', 'help', 'please'],
     "I am a bot and not a human. I have a small set of answers for you. I will try my best to help you."
     ),
    (['low', 'sugar', 'items', 'really'],
     "All our items are low sugar. On average our items have 70% less sugar than their market counterparts."
     ),
    (['bye', 'goodbye', 'adios', 'see',
      'soon'], "Nice chatting with you! See you soon!"),
    (['where', 'what', 'located', 'location', 'address', 'situated', 'are'],
     "We are located in 'Jackson M High School in Everett School District in WA'. You can also find us online."
     ),
    ([
      'how', 'what', 'email', 'can', 'contact', 'mail', 'get', 'touch',
      'address'
    ], """
      You can reach us at <a href=# onclick='top.window.opener.location.href="mailto:bakentake2007@gmail.com" '>bakentake2007@gmail.com</a>.
      """),
    (['where', 'what', 'how', 'menu', 'list', 'items', 'sell', 'on',
      'sale'], """
      You can check our menu here: <a href=# onclick='top.window.opener.location.href="/menu"'> Menu link </a>
      """),
    (['where', 'what', 'how', 'order', 'start', 'add', 'cart', 'ordering'], """
      You can start ordering here: <a href=# onclick='top.window.opener.location.href="/order"'> Order link </a>
    """),
    ([
      'old', 'order', 'how', 'history', 'past', 'list', 'items', 'where', 'my'
    ], """
      You can see your order history in your account. Please click here: <a href=# onclick='top.window.opener.location.href="/account"'> Account link </a><br/>
    """),
    (['principle', 'your', 'idea', 'behind', 'website'], """
      Our principle is taking care of your health. You can see our detailed principle here: <a href=# onclick='top.window.opener.location.href="/principle"'> Our Principle </a><br/>
    """),
    (['review', 'reviews', 'how', 'like', 'people', 'write', 'talk'], """
      Well, we are getting good reviews. You can see them here and write your review as well: <a href=# onclick='top.window.opener.location.href="/reviews"'> Reviews </a><br/>
    """),
    (['thank', 'thanks', 'awesome', 'much', 'you', 'great', 'amazing'], """
      Thank you so much.
       """),
    (['see', 'bye', 'goodbye', 'adios', 'good', 'you'], """
      Bye now! Come again!
       """),
    (['complaint', 'not', 'happy', 'bad', 'horrible', 'you'], """
      We are sorry to hear that! Please write to us (<a href=# onclick='top.window.opener.location.href="mailto:bakentake2007@gmail.com" '>bakentake2007@gmail.com</a>.) before putting it in review! We will correct it.
       """),
  ]

  maxrank = -100000
  maxtuple = ()
  for tuple_ in alltuples:
    rank = AreMostPhrasesThereInMessage(tuple_[0], tokens)
    if rank > maxrank:
      maxrank = rank
      maxtuple = tuple_

  if maxrank > 0:
    response = maxtuple[1]

  return str(response)


@app.route('/chat')  #, methods = ["GET", "POST"])
def chat():

  user = GetUserAccountName(None, None)
  html = """
  <!DOCTYPE html>
<html>

<head>
      <link rel="stylesheet" type="text/css"
    href="https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.1.3/assets/owl.carousel.min.css" />
      <!-- font awesome style -->
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
      <!-- bootstrap core css -->
      <link rel="stylesheet" type="text/css" href="/static/css/bootstrap.css" />
      <!-- fonts style -->
      <link href="https://fonts.googleapis.com/css?family=Poppins:400,600,700|Roboto:400,700&display=swap" rel="stylesheet">
        <!-- Custom styles for this template -->
      <link href="/static/css/style.css" rel="stylesheet" />
      <!-- responsive style -->
      <link href="/static/css/responsive.css" rel="stylesheet" />

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
</head>

<body>
  <section style="width:100%;background-color:#1a0503;align:center;padding:15px;">
  <img src="/static/images/logo-bakery.png" height=52px width=227px>&nbsp;<span style="color:#ffffff; text-align:right;font-size:24px;vertical-align:middle">CHATBOT</span>
  </section>
  <section class="chat_section layout_padding">
  <div class="container">
    <!--<div class="custom_heading-container "><h2>Bake N' Take ChatBot</h2></div><br/>-->
    
    <div class="row">
        <div class="col-md-10 mr-auto ml-auto">
    
    <form>
        <div id="chatbox">
                <p class="botText"><span class=botTitle>Bake 'N Take Chatbot:</span> 
                <span>Hello, 
                 
  """
  html += user

  html += """       
          ! <br/>Please ask your question here. I am a bot and have limited knowledge. I will try my best to answer your questions. </span></p>
        </div>
        <div id="userInput" class="row">
            <div class="col-md-10">
                <input id="text" type="text" name="msg" placeholder="Message" class="form-control">
                <button type="submit" id="send" class="modalbutton">Send</button>
            </div>
        </div>
      </form>
     </div>
    </div>
  </div>
  </section>
<script>
    $(document).ready(function() {
        $("form").on("submit", function(event) {
            var rawText = $("#text").val();
            var userHtml = '<p class="userText"><span><span class=userTitle> """
  html += user.strip()
  html += """ :</span>' + rawText + "</span></p>";
            if ( rawText.length >0 ) {
             $("#text").val("");
             $("#chatbox").append(userHtml);
             document.getElementById("userInput").scrollIntoView({
                block: "start",
                behavior: "smooth",
             });
            }
            $.ajax({
                data: {
                    msg: rawText,
                },
                type: "POST",
                url: "/get",
            }).done(function(data) {
                var botHtml = '<p class="botText"><span class=botTitle>Chatbot:</span><br/><span>' + data + "</span></p>";
                $("#chatbox").append($.parseHTML(botHtml));
                document.getElementById("userInput").scrollIntoView({
                    block: "start",
                    behavior: "smooth",
                });
            });
            event.preventDefault();
           
        });
    });
</script>

</html>
  """
  return html


###############################################################
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81, debug=True)
