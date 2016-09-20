from __future__ import print_function
import os
import sys
import datetime
from peewee import *
from flask import Flask, render_template, request, abort, redirect, url_for
app = Flask(__name__)
db = SqliteDatabase('sweep.sqlite3')

# Database Tables/Classes
class BaseModel(Model):

    class Meta:
        database = db

class Patroller(BaseModel):
    name = TextField()
    status = TextField()

class Location(BaseModel):
    name = TextField()

class Activity(BaseModel):
    patroller = ForeignKeyField(Patroller, related_name='patroller_name')
    location = ForeignKeyField(Location, related_name='patroller_name')
    is_leader = BooleanField(null=True)
    signon = DateTimeField(null=True)
    signoff = DateTimeField(null=True)

@app.route("/")
def main():
    needs = check_for_db()
    registered = generate_active_patrollers()
    if len(needs) == 0:
        msg = ""
    else:
        msg = 'Welcome to Sweep! <br />'
        if 'patrollers' in needs:
            msg += ' Please add <a href="patrollers.html">patrollers</a>'
        if 'locations' in needs:
            if len(msg) > 24:
                msg += ' and '
            else:
                msg += " Please add "
            msg += '<a href="locations.html">locations</a> before you begin.'
    return render_template("index.html", message=msg, Patroller=Patroller,
        Location=Location, registered=registered)

@app.route("/index.html")
def index():
    return main()

@app.route("/patrollers.html")
def update_patrollers():
    p = Patroller.select().dicts()
    return render_template("patrollers.html", patrollers=p)

@app.route("/locations.html")
def update_locations():
    l = Location.select().dicts()
    return render_template("locations.html", locations=l)

@app.route("/update_patrollers", methods=["POST"])
def db_patrollers():
    if request.method == "POST":
        if request.form['button'] == 'update':
            if request.form['patroller-select'] == "new-patroller":
                print(request.form['patroller-name'])
                p = Patroller.create(name=request.form['patroller-name'],
                    status=request.form['status'])
            else:
                p = Patroller.get(Patroller.name == request.form['patroller-select'])
                if len(request.form['patroller-name']) > 0:
                    p.name = request.form['patroller-name']
                p.status = request.form['status']
                p.save()
        elif request.form['button'] == 'delete':
            if request.form['patroller-select'] != "new-patroller":
                p = Patroller.get(Patroller.name == request.form['patroller-select'])
                p.delete_instance()
        else:
            return "Error posting data. Please report this issue to the developer."
    else:
        return "Error posting data. Please report this issue to the developer."
    return redirect("/patrollers.html")

@app.route("/update_locations", methods=["POST"])
def db_locations():
    if request.method == "POST":
        if request.form['button'] == 'update':
            if request.form['select-location'] == "new-location":
                print(request.form['location-name'])
                l = Location.create(name=request.form['location-name'])
            else:
                l = Location.get(Location.name == request.form['select-location'])
                if len(request.form['location-name']) > 0:
                    p.name = request.form['location-name']
                l.save()
        elif request.form['button'] == 'delete':
            if request.form['select-location'] != "new-location":
                l = Location.get(Location.name == request.form['select-location'])
                l.delete_instance()
        else:
            return "Error posting data. Please report this issue to the developer."
    else:
        return "Error posting data. Please report this issue to the developer."
    return redirect('/locations.html')

@app.route("/activity", methods=["POST"])
def db_activity():
    if request.method == "POST":
        print(request.form)
        patroller_name = request.form.get("patroller-name", None)
        location_name = request.form.get("location-name", None)
        leader = request.form.get("is_leader", False)
        is_leader = leader == u"on"
        print(is_leader)
        if request.form['button'] == 'sign-in':
            p = Patroller.get(Patroller.name == patroller_name)
            l = Location.get(Location.name == location_name)
            Activity.create(patroller=p, location=l,
                is_leader=is_leader, signon=datetime.datetime.now())
        elif request.form['button'] == 'sign-out':
            p = Patroller.get(Patroller.name == patroller_name)
            a = Activity.get((Activity.patroller==p) & (Activity.signoff==None))
            a.signoff=datetime.datetime.now()
            a.save()
    return redirect("/index.html")

def generate_active_patrollers():
    # Since Jinja2 wont allow the "&" operator
    registered = dict()
    for l in Location.select():
        records = []
        for a in Activity.select().where((Activity.location==l)
            & (Activity.signoff==None)):
            records.append(a)
        registered[l.name] = records
    return registered


@app.route("/reports.html")
def reports():
    return render_template("reports.html")

def check_for_db():
    need = []
    db.create_tables([Patroller, Location, Activity], safe=True)
    p = Patroller.select().count()
    l = Location.select().count()

    if p == 0:
        need.append('patrollers')
    if l == 0:
        need.append('locations')
    return need

def create_db_connection():
    db.connect()

if __name__ == "__main__":
    app.run(debug=True)
