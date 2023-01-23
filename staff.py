from flask import *
from database import *


staff=Blueprint('staff',__name__)

@staff.route('/staffhome')
def staffhome():
    return render_template('staffhome.html')



@staff.route('/staffmanagecrew',methods=['get','post'])
def staffmanagecrew():
    data={}

    if 'add' in request.form:
        fname=request.form['fname']
        lname=request.form['lname']
        place=request.form['place']
        num=request.form['num']
        email=request.form['email']
        uname=request.form['uname']
        pasw=request.form['pasw']

        q="insert into login values(null,'%s','%s','crew')"%(uname,pasw)
        lid=insert(q)
        q="insert into crew values(null,'%s','%s','%s','%s','%s','%s') "%(lid,fname,lname,place,num,email)
        insert(q)
        return redirect(url_for("staff.staffmanagecrew"))

    q="select * from crew"
    data['res']=select(q)

    if 'action' in request.args:
        action=request.args['action']
        cid=request.args['cid']
        logid=request.args['logid']
    
    else:
        action=None

    if action == "update":
        q="select * from crew where crew_id='%s'"%(cid)
        data['changeval']=select(q)

        if 'update' in request.form:
            fname=request.form['fname']
            lname=request.form['lname']
            place=request.form['place']
            num=request.form['num']
            email=request.form['email']
          

            q="update crew set fname='%s', lname='%s', place='%s', phone='%s', email='%s' where crew_id='%s' "%(fname,lname,place,num,email,cid)
            update(q)
            return redirect(url_for("staff.staffmanagecrew"))

    if action=='delete':
        q="delete from crew where crew_id='%s'"%(cid)
        delete(q)
        q="delete from login where login_id='%s'"%(logid)
        delete(q)
        return redirect(url_for("staff.staffmanagecrew"))
    return render_template('staffmanagecrew.html',data=data)


@staff.route("/staffaddfilim",methods=['get','post'])
def staffaddfilim():
    data={}
    if 'btn' in request.form:
        filim=request.form['filim']
        details=request.form['details']
        desc=request.form['desc']
        date=request.form['date']

        q="insert into filim values (null,'%s','%s','%s','%s')"%(filim,details,desc,date)
        insert(q)
        return redirect(url_for("staff.staffaddfilim"))


    q="select * from filim"
    data['res']=select(q)

    if 'action' in request.args:
        action=request.args['action']
        fid=request.args['fid']
    else:
        action=None

    if action == "update":
        q="select * from filim where filim_id='%s'"%(fid)
        data['filim']=select(q)

        if 'update' in request.form:
            filim=request.form['filim']
            details=request.form['details']
            desc=request.form['desc']
            date=request.form['date']

            q="update filim set filim='%s', details='%s', `desc`='%s', `date`='%s' where filim_id='%s' "%(filim,details,desc,date,fid)
            print(q)
            update(q)
            return redirect(url_for("staff.staffaddfilim"))
    if action=='delete':
        q="delete from filim where filim_id='%s'"%(fid)
        delete(q)
        return redirect(url_for("staff.staffaddfilim"))
    return render_template("staffaddfilim.html",data=data)


@staff.route("/staffaddcrewmembers",methods=['get','post'])
def staffaddcrewmembers():
    data={}
    fid=request.args['fid']
    filim=request.args['filim']
    q="select * from crew"
    data['res']=select(q)

    if 'btn' in request.form:
        cr_id=request.form['cr_id']
        q="insert into assigncrew values(null,'%s','%s',curdate(),'pending')"%(fid,cr_id)
        insert(q)
        return redirect(url_for("staff.staffaddcrewmembers",fid=fid,filim=filim))
    q="select * from crew inner join assigncrew using (crew_id) where filim_id='%s'"%(fid)
    data['crew']=select(q)

    if 'action' in request.args:
        action=request.args['action']
        cid=request.args['cid']
    else:
        action=None

    if action=='delete':
        q="delete from assigncrew where crew_id='%s'"%(cid)
        delete(q)
        return redirect(url_for("staff.staffaddcrewmembers",fid=fid,filim=filim))
    return render_template("staffaddcrewmembers.html",data=data,filim=filim,fid=fid)


@staff.route("/staffassignworkstocrew",methods=['get','post'])
def staffassignworkstocrew():
    data={}
    q="select * from crew inner join assigncrew using (crew_id)"
    data['res']=select(q)

    if 'action' in request.args:
        action=request.args['action']
        asigid=request.args['asigid']
    else:
        action=None

    if action == "add":
        data['addwrk']=True

        if 'btn' in request.form:
            work=request.form['work']
            details=request.form['details']

            q="insert into works values (null,'%s','%s','%s',curdate(),'pending')"%(asigid,work,details)
            insert(q)
            return redirect(url_for("staff.staffassignworkstocrew"))
        
    if action == "viewwork":
        q="select * from works where assigncrew_id='%s'"%(asigid)
        data['viewsec']=True
        data['viewwrk']=select(q)
        print(len(select(q)))
        data['count']=len(select(q))

    return render_template("staffassignworkstocrew.html",data=data)



@staff.route("/staffviewcrewrequirment",methods=['get','post'])
def staffviewcrewrequirment():
    data={}
    q="SELECT *,requirment.status as status FROM `requirment`,`assigncrew`,`crew` WHERE `requirment`.`assigncrew_id`=`assigncrew`.`assigncrew_id` AND `assigncrew`.`crew_id`=`crew`.`crew_id`"
    data['res']=select(q)

    if 'action' in request.args:
        action=request.args['action']
        rid=request.args['rid']
        aid=request.args['aid']
    else:
        action=None

    if action == "approve":
        q="update requirment set status='approved' where requirment_id='%s'"%(rid)
        update(q)
        return redirect(url_for("staff.staffviewcrewrequirment"))
        
    if action == "reject":
        q="update requirment set status='rejected' where requirment_id='%s'"%(rid)
        update(q)
        return redirect(url_for("staff.staffviewcrewrequirment"))
    
    
    if action == "payment":
        data['pay']=True
        if 'btn' in request.form:
            amount=request.form['amount']
            q="insert into payment values(null,'%s','%s',curdate())"%(aid,amount)
            insert(q)
            q="update requirment set status='Payment Completed' where requirment_id='%s'"%(rid)
            update(q)
            return redirect(url_for("staff.staffviewcrewrequirment"))
       

    return render_template("staffviewcrewrequirment.html",data=data)