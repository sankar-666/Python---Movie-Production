from flask import *
from database import *


crew=Blueprint('crew',__name__)

@crew.route('/crewhome')
def crewhome():
    return render_template('crewhome.html')


@crew.route("/crewviewfilimdetails")
def crewviewfilimdetails():
    data={}
    q="select * from filim"
    data['res']=select(q)
    return render_template("crewviewfilimdetails.html",data=data)


@crew.route("/crewviewassignedfilims")
def crewviewassignedfilims():
    data={}
    q="select * from filim inner join assigcrew using (filim_id) where crew_id='%s'"%(session['cid'])
    data['res']=select(q)

    if 'action' in request.args:
        action=request.args['action']
        aid=request.args['aid']
    else:
        action=None

    q="select * from requirment inner join assigncrew using (assigncrew_id) where crew_id='%s' and assigncrew_id='%s'"%(session['cid'],aid)
    data['val']=select(q)
    
    if action == "reqadd":
        data['reqadd']=True
        if 'btn' in request.form:
            req=request.form['req']
            q="insert into requirment values(null,'%s','%s',curdate(),'pending')"%(aid,req)
            insert(q)
            return redirect(url_for("crew.crewviewassignedfilims")) 

    return render_template("crewviewassignedfilims.html",data=data)



@crew.route("/crewviewassignedworks")
def crewviewassignedworks():
    data={}
    q="SELECT *,work.date as date FROM works INNER JOIN assigncrew USING (assigncrew_id) where crew_id='%s'"%(session['cid'])
    data['res']=select(q)

    if 'action' in request.args:
        action=request.args['action']
        wid=request.args['wid']
    else:
        action=None

    if action == "completed":
        q="update works set status='work completed' where work_id='%s' "%(wid)
        insert(q)
        return redirect(url_for("crew.crewviewassignedworks")) 

    return render_template("crewviewassignedworks.html",data=data)


@crew.route("/crewviewpayments")
def crewviewpayments():
    data={}
    q="SELECT * FROM `crew`,`assigncrew`,`payment`,`filim` WHERE `crew`.`crew_id`=`assigncrew`.`crew_id` AND `assigncrew`.`assigncrew_id`=`payment`.`assigncrew_id`  AND  `assigncrew`.`filim_id`=`filim`.`filim_id` and crew_id='%s'"%(session['cid'])
    data['res']=select(q)
    return render_template("crewviewpayments.html",data=data)