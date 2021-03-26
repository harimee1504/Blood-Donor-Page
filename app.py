from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import smtplib
import urllib
from sqlalchemy import text
from email.message import EmailMessage
from datetime import datetime, date
from dateutil.relativedelta import *


app = Flask(__name__)

app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="your username",
    password="your password",
    hostname="your hostname",
    databasename="your database name",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


def execute(query):
    t = text(query)
    result = db.session.execute(t)
    res = result.fetchall()
    return res


cities = []
groups = ['A +ve', 'A -ve', 'B +ve', 'B -ve',
          'AB +ve', 'AB -ve', 'O +ve', 'O -ve']


def status(group):
    fn = "SELECT fname FROM "+group
    ln = "SELECT lname FROM "+group
    t = "SELECT active FROM "+group
    s = "SELECT NextDonate FROM "+group
    ci = "SELECT city FROM "+group
    t = execute(t)
    fn = execute(fn)
    ln = execute(ln)
    s = execute(s)
    ci = execute(ci)
    t1, s1, fn1, ln1 = [], [], [], []
    for i in range(len(t)):
        for j in t[i].values():
            t1.append(j)
        for k in s[i].values():
            s1.append(k)
        for l in fn[i].values():
            fn1.append(l)
        for n in ln[i].values():
            ln1.append(n)
        for m in ci[i].values():
            if m not in cities:
                cities.append(m)
    tot = len(t)
    act = 0
    for i in range(len(t)):
        if t1[i] == 'active':
            act += 1
        else:
            today = list(map(int, str(date.today()).split('-')))
            y = list(map(int, str(s1[i]).split('-')))
            d1 = datetime(y[0], y[1], y[2])
            d2 = datetime(today[0], today[1], today[2])
            x = text("update "+group+" set active=:act WHERE fname=:fname AND lname=:lname")\
                .bindparams(act="active", fname=fn1[i], lname=ln1[i])
            if d2 > d1:
                db.session.execute
                db.session.commit()
    res = [tot, act]
    return res


@app.route('/')
def bloodindex():
    blood = ['apositive', 'anegative', 'bpositive', 'bnegative',
             'abpositive', 'abnegative', 'opositive', 'onegative']
    total, active, inactive = [], [], []
    for i in blood:
        res = status(i)
        if len(res) != 0:
            total.append(str(res[0]))
            active.append(str(res[1]))
            inactive.append(str(res[0]-res[1]))
    td = sum([int(i) for i in total])
    ad = sum([int(i) for i in active])
    id1 = sum([int(i) for i in inactive])
    cities.sort()
    return render_template("bloodindex.html", total=total, active=active, inactive=inactive, td=td, ad=ad, id1=id1, cities=cities, groups=groups)


@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        group = request.form.get("group")
        area = request.form.get("area")
        city = request.form.get("city")
        state = request.form.get("state")
        country = request.form.get("country")
        dob = request.form.get("dob")
        phone = request.form.get("phone")
        email = request.form.get("email")
        firstDonate = request.form.get("first")
        if firstDonate == 'no':
            LastDonate = request.form.get("LastDonate")
            ld = datetime.strptime(LastDonate, '%Y-%m-%d').date()
            NextDonate = ld+relativedelta(months=+4)
            today = list(map(int, str(date.today()).split('-')))
            NextDonate = list(map(int, str(NextDonate).split('-')))
            d1 = datetime(NextDonate[0], NextDonate[1], NextDonate[2])
            d2 = datetime(today[0], today[1], today[2])
            ldtemp = str(NextDonate[0])+'-' + \
                str(NextDonate[1])+'-'+str(NextDonate[2])
            if d2 > d1:
                stat = 'active'
            else:
                stat = 'inactive'
        else:
            stat = 'active'
            LastDonate = 'Donor-Time-First'
            ldtemp = 'First'

        table = text("INSERT INTO "+group+" (fname,lname,area,city,state,country,dob,phone,email,LastDonate,active,NextDonate) VALUES(:fname,:lname,:area,:city,:state,:country,:dob,:phone,:email,:LastDonate,:active,:NextDonate)")\
            .bindparams(fname=fname, lname=lname, area=area, city=city, state=state, country=country, dob=dob, phone=phone, email=email, LastDonate=LastDonate, active=stat, NextDonate=ldtemp)
        db.session.execute(table)
        db.session.commit()
        return redirect('/')


@app.route('/apositive')
def apositive():
    t = execute('SELECT * FROM apositive')
    return render_template('details.html', t=t, n=len(t), group='A positive ')


@app.route('/bpositive')
def bpositive():
    t = execute('SELECT * FROM bpositive')
    return render_template('details.html', t=t, n=len(t), group='B positive ')


@app.route('/abpositive')
def abpositive():
    t = execute('SELECT * FROM abpositive')
    return render_template('details.html', t=t, n=len(t), group='AB positive ')


@app.route('/opositive')
def opositive():
    t = execute('SELECT * FROM opositive')
    return render_template('details.html', t=t, n=len(t), group='O positive ')


@app.route('/anegative')
def anegative():
    t = execute('SELECT * FROM anegative')
    return render_template('details.html', t=t, n=len(t), group='A negative ')


@app.route('/bnegative')
def bnegative():
    t = execute('SELECT * FROM bnegative')
    return render_template('details.html', t=t, n=len(t), group='B negative ')


@app.route('/abnegative')
def abnegative():
    t = execute('SELECT * FROM abnegative')
    return render_template('details.html', t=t, n=len(t), group='AB negative ')


@app.route('/onegative')
def onegative():
    t = execute('SELECT * FROM onegative')
    return render_template('details.html', t=t, n=len(t), group='O negative ')


@app.route('/search', methods=["GET", "POST"])
def find():
    grp = ['apositive', 'anegative', 'bpositive', 'bnegative',
           'abpositive', 'abnegative', 'opositive', 'onegative']
    if request.method == "GET":
        return redirect('/blood-index')
    else:
        s1 = request.form.get("city")
        s2 = request.form.get("groups")
        if s2 == 'Select Group' or s1 == 'Select City':
            return redirect('/')
        else:
            ind = groups.index(s2)
            val = 'SELECT * FROM '+grp[ind]+' WHERE city="'+s1+'";'
        t = execute(val)
        c1, c2 = 0, 0
        for i in range(len(t)):
            if t[i]['active'] == 'active':
                c1 += 1
            else:
                c2 += 1
        grp[ind] = grp[ind].lower().capitalize()
        grp[ind] = grp[ind][:1]+' '+grp[ind][1:]
        return render_template('details.html', t=t, n=len(t), group=grp[ind], c1=c1, c2=c2)
