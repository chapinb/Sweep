import os
import sys
from peewee import *
from passlib.hash import pbkdf2_sha256
from flask import Flask, render_template
app = Flask(__name__)
db = SqliteDatabase('sweep.sqlite3')

# Database Tables/Classes
class BaseModel(Model):

    class Meta:
        database = db

class Patrollers(BaseModel):
    name = TextField()
    status = TextField()
    code = TextField() # Just in case the used passcode is re-used, we will store a hash :)

class Locations(BaseModel):
    name = TextField()

class Activity(BaseModel):
    patroller = ForeignKeyField(Patrollers, related_name='patroller_name')
    location = ForeignKeyField(Locations, related_name='patroller_name')
    signon = DateTimeField()
    signoff = DateTimeField()

@app.route("/")
def main():
    needs = check_for_db()
    if len(needs) == 0:
        msg = ""
    else:
        msg = 'Welcome to Sweep! <br />'
        if 'patrollers' in needs:
            msg += ' Please add <a href="patollers.html">patrollers</a>'
        if 'locations' in needs:
            if len(msg) > 17:
                msg += ' and '
            else:
                msg += " Please add "
            msg += '<a href="locations.html">locations</a> before you begin.'
    return render_template("index.html", message=msg)

@app.route("/index.html")
def index():
    return main()

@app.route("/patrollers.html")
def update_patrollers():
    return render_template("patrollers.html")

@app.route("/locations.html")
def update_locations():
    return render_template("locations.html")

@app.route("/reports.html")
def reports():
    return render_template("reports.html")

def check_for_db():
    need = []
    try:
        Patrollers.get(Patroller.id == 1)
    except:
        need.append('patrollers')
    try:
        Locations.get(Patroller.id == 1)
    except:
        need.append('locations')

    return need

def create_db_connection():
    db.connect()

if __name__ == "__main__":
    app.run(debug=True)
