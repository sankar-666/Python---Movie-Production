from flask import *
from database import *


public=Blueprint('public',__name__)

@public.route('/',methods=['post','get'])
def home():
    if 'btn' in request.form:
        uname=request.form['uname']
        pasw =request.form['pasw']

        q="select * from login where username='%s' and password='%s'"%(uname,pasw)
        res=select(q)


        if res:
            session['loginid']=res[0]["login_id"]
            utype=res[0]["usertype"]
            if utype == "admin":
                return redirect(url_for("admin.adminhome"))
            elif utype == "staff":
                q="select * from staff where login_id='%s'"%(session['loginid'])
                val=select(q)
                if val:
                    session['sid']=val[0]['staff_id']
                    return redirect(url_for("staff.staffhome"))
            elif utype == "crew":
                q="select * from crew where login_id='%s'"%(session['loginid'])
                cval=select(q)
                if cval:
                    session['cid']=cval[0]['crew_id']
                    return redirect(url_for("crew.crewhome"))
               
            
            else:
                flash("failed try again")
                return redirect(url_for("home./"))
    return render_template('home.html')


@public.route('/login',methods=['post','get'])
def login():

    


    return render_template("login.html")