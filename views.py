import json
from datetime import datetime
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from Fake_currency.cnn_predict import predict
from Fake_currency.models import *
# Create your views here.
def login(request):
    return render(request,"login_index.html")

def logout(request):
    auth.logout(request)
    return render(request,"login_index.html")

def login_post(request):
    uname=request.POST["textfield"]
    password=request.POST["textfield2"]
    q=login_table.objects.get(username=uname,password=password)
    try:
        if q.type=="admin":
            auth_obj = auth.authenticate(username='admin', password='admin')
            if auth_obj is not None:
                auth.login(request, auth_obj)
            return HttpResponse('''<script>alert('Login Success');window.location='/admin_home'</script>''')
        elif q.type=="staff":
            auth_obj = auth.authenticate(username='admin', password='admin')
            if auth_obj is not None:
                auth.login(request, auth_obj)

            request.session["lid"]=q.id
            return HttpResponse('''<script>alert('Staff Login Success');window.location='/staff'</script>''')

        else:
            return HttpResponse('''<script>alert('Invalid');window.location='/'</script>''')
    except:
        return HttpResponse('''<script>alert('Error');window.location='/'</script>''')

@login_required(login_url="/")
def addstaff(request):
    return render(request,"admin/Add Staff.html")


@login_required(login_url="/")
def editstaff(request, id):
    ob = staff_table.objects.get(id=id)
    request.session['s_id'] = id
    return render(request,"admin/Edit Staff.html", {'val': ob, 'dob': str(ob.dob)})


def staff_edit_post(request):
    try:
        fn=request.POST['textfield']
        sn=request.POST['textfield2']
        ge=request.POST['RadioGroup1']
        dt=request.POST['date']
        pl=request.POST['textfield3']
        po=request.POST['textfield4']
        pi=request.POST['textfield5']
        ph=request.FILES['file']
        fs=FileSystemStorage()
        fnn=fs.save(ph.name,ph)
        pn=request.POST['textfield6']
        em=request.POST['textfield7']

        oj=staff_table.objects.get(id=request.session['s_id'])
        oj.place=pl
        oj.fname=fn
        oj.lname=sn
        oj.gender=ge
        oj.dob=dt
        oj.post=po
        oj.pin=pi
        oj.phone=pn
        oj.photo=fnn
        oj.email=em
        oj.save()
        return HttpResponse('''<script>alert('edited successfully');window.location='/viewandmanagestaff'</script>''')
    except:
        fn = request.POST['textfield']
        sn = request.POST['textfield2']
        ge = request.POST['RadioGroup1']
        dt = request.POST['date']
        pl = request.POST['textfield3']
        po = request.POST['textfield4']
        pi = request.POST['textfield5']
        pn = request.POST['textfield6']
        em = request.POST['textfield7']

        oj = staff_table.objects.get(id=request.session['s_id'])
        oj.place = pl
        oj.fname = fn
        oj.lname = sn
        oj.gender = ge
        oj.dob = dt
        oj.post = po
        oj.pin = pi
        oj.phone = pn
        oj.email = em
        oj.save()
        return HttpResponse('''<script>alert('edited successfully');window.location='/viewandmanagestaff'</script>''')


def admin_home(request):
    return render(request,"admin/admin_index.html")

def assignwork(request,id):
    ob=staff_table.objects.all()
    request.session['mid']=id
    return render(request,"admin/Assign work.html",{'val':ob})

def assign(request):
    ob = assignwork_table.objects.all()
    return render(request,"admin/Assign.html",{'val':ob})

def notification(request):
    return render(request,"admin/Notification.html")
def notification_1(request):
    noti=request.POST['textfield']
    ob=notification_table()
    ob.notification=noti
    ob.date=datetime.today()
    ob.save()
    return HttpResponse('''<script>alert('Notification sended');window.location='/admin_home'</script>''')

def viewandmanagestaff(request):
    ob=staff_table.objects.all()
    return render(request,"admin/View and manage staff.html",{'val':ob})
def viewandmanagestaff_delete(request,id):
    ob=login_table.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Deleted');window.location='/viewandmanagestaff'</script>''')


def staff_1(request):
    fn=request.POST['textfield']
    sn=request.POST['textfield2']
    ge=request.POST['RadioGroup1']
    dt=request.POST['date']
    pl=request.POST['textfield3']
    po=request.POST['textfield4']
    pi=request.POST['textfield5']
    ph=request.FILES['file']
    fs=FileSystemStorage()
    fnn=fs.save(ph.name,ph)
    pn=request.POST['textfield6']
    em=request.POST['textfield7']
    un=request.POST['textfield8']
    ps=request.POST['textfield9']

    ob=login_table()
    ob.username=un
    ob.password=ps
    ob.type="staff"
    ob.save()

    oj=staff_table()
    oj.LOGIN=ob
    oj.place=pl
    oj.fname=fn
    oj.lname=sn
    oj.gender=ge
    oj.dob=dt
    oj.post=po
    oj.pin=pi
    oj.phone=pn
    oj.photo=fnn
    oj.email=em
    oj.save()
    return HttpResponse('''<script>alert('Added successfully');window.location='/viewandmanagestaff'</script>''')





def viewcomplaint(request):
    ob = complaint_table.objects.all()
    return render(request,"admin/View Complaint.html",{'val':ob})

def replay(request,id):
    request.session['coid']=id
    return render(request,"admin/Replay.html")


def replay_post(request):
    reply = request.POST['textfield']
    ob = complaint_table.objects.get(id=request.session['coid'])
    ob.replay=reply
    ob.save()
    return HttpResponse('''<script>alert('Replay sended');window.location='/viewcomplaint'</script>''')

def status_post(request):
    status = request.POST['textfield']
    ob = assignwork_table.objects.get(id=request.session['assignid'])
    ob.status=status
    ob.save()
    return HttpResponse('''<script>alert('Status updated');window.location='/viewworkandupdate'</script>''')

def viewfeedback(request):
    ob = feedback_table.objects.all()
    return render(request,"admin/View feedback.html",{'val':ob})

def viewuser(request):
    ob=user_table.objects.all()
    return render(request,"admin/View user.html",{'val':ob})

def feedbackview(request):
    ob=feedback_table.objects.all()
    return render(request,"staff/Feedback view(staff).html",{'val':ob})

def notificationuser(request):
    ob =usernotification_table.objects.filter(staff__LOGIN=request.session["lid"])
    return render(request,"staff/Notification user(staff).html",{'val':ob})

def notificationviewadmin(request):
    ob=notification_table.objects.all()
    return render(request,"staff/Notification view admin (staff).html",{'val':ob})

def staff(request):
    return render(request,"staff/staff_index.html")

def updatestatus(request,id):
    request.session['assignid']=id
    return render(request,"staff/Update status(stafff).html")

def viewworkandupdate(request):
    ob = assignwork_table.objects.filter(staff__LOGIN=request.session["lid"])
    return render(request,"staff/View work and update(staff).html",{'val':ob})

def work_1(request):

    stff=request.POST['select']
    wr=request.POST['textfield']
    de=request.POST['textfield2']
    dl=request.POST['textfield3']
    dly=request.POST['textfield38']

    ob=assignwork_table.objects.get(id=request.session['mid'])
    ob.staff=staff_table.objects.get(id=stff)
    ob.work=wr
    ob.description=de
    ob.date=dl
    ob.deadline=dly
    ob.status='pending'
    ob.save()
    return HttpResponse('''<script>alert('Work assigned');window.location='/assign'</script>''')







"==========================ANDROID==============================="
def logincode1(request):
    print(request.POST)
    un = request.POST['uname']
    pwd = request.POST['pswd']
    print(un, pwd)
    try:
        ob = login_table.objects.get(username=un, password=pwd)

        if ob is None:
            data = {"task": "invalid"}
        else:
            print("in user function")
            data = {"task": "valid", "id": ob.id,"type":ob.type}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)
    except:
        data = {"task": "invalid"}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)







def viewcomplaint_android(request):
    lid=request.POST['lid']
    ob=complaint_table.objects.filter(user__LOGIN__id=lid)

    print(ob,"HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'complaint': i.complain, 'date': str(i.date),'reply':i.replay,'id':i.id}
        mdata.append(data)
        print(mdata)
    r = json.dumps(mdata)
    return HttpResponse(r)


def viewcomplaintsearch(request):
    lid=request.POST['lid']
    date=request.POST['date']
    ob=complaint_table.objects.filter(date=date,user__LOGIN__id=lid)

    print(ob,"HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'complaint': i.complain, 'date': str(i.date), 'reply': i.replay, 'id': i.id}
        mdata.append(data)
        print(mdata)
    r = json.dumps(mdata)
    return HttpResponse(r)

def sendcomplaint(request):
    comp=request.POST['complaint']
    lid=request.POST['lid']
    lob = complaint_table()
    lob. complain= comp
    lob. user= user_table.objects.get(LOGIN__id=lid)
    lob.replay = 'pending'
    lob.date = datetime.today()
    lob.save()

    data = {"task": "valid"}
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)

def sendrating(request):
    feed=request.POST['feedback']

    lid=request.POST['lid']
    lob =feedback_table()
    lob. Feedback= feed
    lob. user= user_table.objects.get(LOGIN__id=lid)
    lob.date = datetime.today()
    lob.save()

    data = {"task": "valid"}
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)




def view_notification(request):
    ob=notification_table.objects.all()

    data = []
    for i in ob:
        res = {'date': str(i.date), 'notification': i.notification}
        data.append(res)
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)






def registration(request):
    try:
        Fname=request.POST['Fname']
        lname=request.POST['Lname']
        dob=request.POST['age']
        image=request.FILES['file']
        fs = FileSystemStorage()
        fsave = fs.save(image.name, image)
        place= request.POST['place']
        post_office = request.POST['post']
        pin_code = request.POST['pin_code']
        gender = request.POST['gender']
        phone = request.POST['phone_number']
        email_id = request.POST['emil_id']
        uname = request.POST['username']
        passwd = request.POST['password']
        lob = login_table()
        lob.username = uname
        lob.password = passwd
        lob.type = 'user'
        lob.save()
        userob = user_table()
        userob.fname = Fname
        userob.lname = lname
        userob.dob = dob
        userob.gender = gender
        userob.place = place
        userob.post = post_office
        userob.pin = pin_code
        userob.phone = phone
        userob.email = email_id
        userob.photo = fsave
        userob.LOGIN=lob
        userob.save()
        data = {"task": "valid"}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)
    except:

        data = {"task": "Duplicate"}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)



def uploadimage(request):
    img=request.FILES['file']
    fs=FileSystemStorage()
    fn=fs.save(img.name,img)
    res=predict(r"C:\Users\Amishazzz\Desktop\final back\fake_currency_detection\fake_currency_detection\media/"+fn)
    return JsonResponse({"task":res,"fn":fn})




