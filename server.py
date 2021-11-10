import random

from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# CONSTANTS
RIDLES = ['David’s parents have three sons: Snap, Crackle, and what’s the name of the third son?',
          'If you’ve got me, you want to share me; if you share me, you haven’t kept me. What am I?',
          'Where does today come before yesterday?',
          'What has one eye, but can’t see?',
          'What building has the most stories?']
ANSWERS = ['david', 'secret', 'dictionary', 'needle', 'library']


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=True)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)


# Home Page
@app.route("/")
def home():
    cafes = db.session.query(Cafe).all()
    cafe_list = []
    for cafe in cafes:
        cafe_dict = {
         "id": cafe.id,
            "name": cafe.name,
            "map_url": cafe.map_url,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "seats": cafe.seats,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "has_sockets": cafe.has_sockets,
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price,
            "id_accordion": "cafe" + str(cafe.id),
            "nid_accordion": "#cafe" + str(cafe.id),
        }
        cafe_list.append(cafe_dict)
    return render_template('index.html', cafes=cafe_list)


@app.route("/update/<int:cafe_id>",  methods=['GET', 'POST'])
def update(cafe_id):
    message = ''
    cafe_to_update = Cafe.query.get(cafe_id)
    if request.method == 'GET':
        global ridle
        global answer
        ridle = random.choice(RIDLES)
        answer = ANSWERS[RIDLES.index(ridle)]
    if request.method == 'POST':
        clave = request.form.get('clave').lower()
        if clave == answer:
            if request.form.get("name"):
                cafe_to_update.name = request.form.get("name")
            if request.form.get("mapa"):
                cafe_to_update.map_url= request.form.get("mapa")
            if request.form.get("imagen"):
                cafe_to_update.img_url = request.form.get("imagen")
            if request.form.get("location"):
                cafe_to_update.location = request.form.get("location")
            if request.form.get("seats"):
                cafe_to_update.seats = request.form.get("seats")
            if request.form.get("toilet"):
                if request.form.get("toilet").lower() == 'yes':
                    cafe_to_update.has_toilet = 1
                elif request.form.get("toilet").lower() == 'no':
                    cafe_to_update.has_toilet = 0
            if request.form.get("wifi"):
                if request.form.get("wifi").lower() == 'yes':
                    cafe_to_update.has_wifi = 1
                elif request.form.get("wifi").lower() == 'no':
                    cafe_to_update.has_wifi = 0
            if request.form.get("sockets"):
                if request.form.get("sockets").lower() == 'yes':
                    cafe_to_update.has_sockets = 1
                elif request.form.get("sockets").lower() == 'no':
                    cafe_to_update.has_sockets = 0
            if request.form.get("calls"):
                if request.form.get("calls").lower() == 'yes':
                    cafe_to_update.has_calls = 1
                elif request.form.get("calls").lower() == 'no':
                    cafe_to_update.has_calls = 0
            if request.form.get("price"):
                cafe_to_update.coffee_price = request.form.get("price")
            db.session.commit()
            message = f"{cafe_to_update.name} has been updated on the database"
        else:
            message = 'The key provided was incorrect. You will not be able to update this cafe'
    return render_template('update.html', cafe=cafe_to_update, msg=message, rd=ridle)


@app.route("/add",  methods=['GET', 'POST'])
def add():
    message = ''
    if request.method == 'GET':
        global ridle
        global answer
        ridle = random.choice(RIDLES)
        answer = ANSWERS[RIDLES.index(ridle)]
    if request.method == 'POST':
        clave = request.form.get('clave').lower()
        if clave == answer:
            if request.form.get("toilet"):
                if request.form.get("toilet").lower() == 'yes':
                    toilet = 1
                else:
                    toilet = 0
            if request.form.get("wifi"):
                if request.form.get("wifi").lower() == 'yes':
                    wifi = 1
                else:
                    wifi = 0
            if request.form.get("sockets"):
                if request.form.get("sockets").lower() == 'yes':
                    sockets = 1
                else:
                    sockets = 0
            if request.form.get("calls"):
                if request.form.get("calls").lower() == 'yes':
                    calls = 1
                else:
                    calls = 0
            new_cafe = Cafe(
                name=request.form.get('nombre'),
                map_url=request.form.get('mapa'),
                img_url=request.form.get("imagen"),
                location=request.form.get("location"),
                seats=request.form.get("seats"),
                has_toilet=bool(toilet),
                has_wifi=bool(wifi),
                has_sockets=bool(sockets),
                can_take_calls=bool(calls),
                coffee_price=request.form.get("price"),
            )
            db.session.add(new_cafe)
            db.session.commit()
            message = f"A new cafe has been added on the database"
        else:
            message = 'The key provided was incorrect. You will not be able to update this cafe'
    return render_template('add.html', msg=message, rd=ridle)


@app.route("/delete/<int:cafe_id>",  methods=['GET', 'POST'])
def delete(cafe_id):
    message = ''
    cafe_to_delete = Cafe.query.get(cafe_id)
    if request.method == 'GET':
        global ridle
        global answer
        ridle = random.choice(RIDLES)
        answer = ANSWERS[RIDLES.index(ridle)]
    if request.method == 'POST':
        clave = request.form.get('clave').lower()
        if clave == answer:
            message = f"{cafe_to_delete.name} has been deleted from the database"
            db.session.delete(cafe_to_delete)
            db.session.commit()
        else:
            message = 'The key provided was incorrect. You will not be able to delete this cafe'
    return render_template('delete.html', cafe=cafe_to_delete, msg=message, rd=ridle)


if __name__ == "__main__":
    app.run(debug=True)