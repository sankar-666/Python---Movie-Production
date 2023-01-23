from flask import *
from database import *


admin=Blueprint('admin',__name__)

@admin.route('/adminhome')
def adminhome():
    return render_template('adminhome.html')



@admin.route('/adminmanagestaff',methods=['get','post'])
def adminmanagestaff():
    data={}

    if 'add' in request.form:
        fname=request.form['fname']
        lname=request.form['lname']
        place=request.form['place']
        num=request.form['num']
        email=request.form['email']
        uname=request.form['uname']
        pasw=request.form['pasw']

        q="insert into login values(null,'%s','%s','staff')"%(uname,pasw)
        lid=insert(q)
        q="insert into staff values(null,'%s','%s','%s','%s','%s','%s') "%(lid,fname,lname,place,num,email)
        insert(q)
        return redirect(url_for("admin.adminmanagestaff"))

    q="select * from staff"
    data['res']=select(q)

    if 'action' in request.args:
        action=request.args['action']
        sid=request.args['sid']
        logid=request.args['logid']
    
    else:
        action=None

    if action == "update":
        q="select * from staff where staff_id='%s'"%(sid)
        data['changeval']=select(q)

        if 'update' in request.form:
            fname=request.form['fname']
            lname=request.form['lname']
            place=request.form['place']
            num=request.form['num']
            email=request.form['email']
          

            q="update staff set fname='%s', lname='%s', place='%s', phone='%s', email='%s' where smaster_id='%s' "%(fname,lname,place,num,email,sid)
            update(q)
            return redirect(url_for("admin.adminmanagestaff"))

    if action=='delete':
        q="delete from staff where staff_id='%s'"%(sid)
        delete(q)
        q="delete from login where login_id='%s'"%(logid)
        delete(q)
        return redirect(url_for("admin.adminmanagestaff"))
    return render_template('adminmanagestaff.html',data=data)

@admin.route("/adminviewcrewmembers")
def adminviewcrewmembers():
    data={}
    q="select * from crew"
    data['res']=select(q)
    return render_template("adminviewcrewmembers.html",data=data)


@admin.route("/adminviewfilimdetails")
def adminviewfilimdetails():
    data={}
    q="select * from filim"
    data['res']=select(q)
    return render_template("adminviewfilimdetails.html",data=data)


@admin.route("/adminviewpaymentdetails")
def adminviewpaymentdetails():
    data={}
    q="SELECT * FROM `crew`,`assigncrew`,`payment`,`filim` WHERE `crew`.`crew_id`=`assigncrew`.`crew_id` AND `assigncrew`.`assigncrew_id`=`payment`.`assigncrew_id`  AND  `assigncrew`.`filim_id`=`filim`.`filim_id`"
    data['res']=select(q)
    return render_template("adminviewpaymentdetails.html",data=data)