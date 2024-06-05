""" app.py - Provide server backend for Calare """

from dataclasses import dataclass
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from result import Result, Ok, Err

from db import DataBase
from resource import Resource, Resources

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///calare"
#db = SQLAlchemy(app)

database = DataBase(app)

@app.route("/")
def index():
    """Placeholder for actual / endpoint implementation"""
    features = ["server", "user-interface"]
    return render_template("index.html", features=features)

@app.route("/admin")
def admin():
    """Placeholder for actual admin control panel implementation"""
    return "Admin control panel"

@app.route("/login")
def login():
    """Serve login.html at endpoint /login"""
    return render_template("login.html")

@app.route("/auth", methods=["POST"])
def auth():
    """Authenticate user"""
    print("args:")
    for arg in request.args:
        print(arg)
    if request.form["username"] == "Admin" and request.form["password"] == "Qwerty":
        return render_template("login_success.html", username=request.form["username"])

    return render_template("login_failed.html"), 401

@dataclass
class Resource:
    """Implement a bookable resource

    Corresponds to a row in the resources table
    """
    id: str
    name: str

collection_resources = [
    Resource("001", "Room A"),
    Resource("002", "Room B"),
    Resource("003", "Room C"),
]

class Booking:
    """Implement a booking object

    Corresponds to a row in the bookings table
    """
    bookings = {}

    def __init__(self, booking_id=0, title="", user="", #pylint: disable=too-many-arguments
                 description="", start="", end="", resources=None):

        self.id = booking_id
        self.title = title
        self.user = user
        self.description = description
        self.start = start
        self.end = end
        self.resources = resources if resources is not None else []

    def get_resource_list(self):
        """Return a list of tuples containing all
        of the resources in the system and whether
        they should be checked or not checked"""
        res = []
        for resource in collection_resources:
            print(resource)
            if resource.id in self.resources:
                res.append(("checked", resource))
            else:
                res.append(("", resource))

        return res

    @classmethod
    def create(cls, title="", user="", description="", #pylint: disable=too-many-arguments
        start="", end="", resources=None):
        """Create a new Booking instance with correct id"""
        resources = resources if resources is not None else []

        booking_id = len(dict.keys(Booking.bookings))
        booking = Booking(booking_id, title, user, description, start, end, resources)
        Booking.bookings[booking_id] = booking

        return booking


@app.route("/bookings")
def bookings_list():
    """Serve a list of all the bookings"""

    query = text("SELECT uuid_id, title FROM bookings")
    res = db.session.execute(query).fetchall()

    print(res)

    return render_template("bookings_list.html",
        bookings=res)


@app.route("/bookings/edit/")
def new_booking():
    """Create a new booking"""

    return render_template("edit_booking.html",
        page_title="Create new booking", id="", title="",
        user="", description="", start="", end="", resources=[])

@app.route("/bookings/edit/<booking_id>")
def edit_booking_with_id(booking_id):
    """Edit the booking with the id"""

    query = text("SELECT serial_id, uuid_id, title, description, user, start_time, end_time FROM bookings WHERE uuid_id=:id")
    res = db.session.execute(query, {"id": booking_id})
    x = res.fetchone()

    print(x.serial_id)

    query = text("SELECT resources.name FROM resource_bookings JOIN resources ON resources.serial_id=resource_bookings.resource_id WHERE resource_bookings.booking_id=:id;")
    res = db.session.execute(query, {"id": x.serial_id})
    booked_resources = [ x.name for x in res.fetchall()]

    query = text("SELECT uuid_id, name FROM resources")
    res = db.session.execute(query)
    resource_ids = res.fetchall()

    # There probably is a way to combine the last two queries: select all resource.name,
    # join with result of is resource.sreial_id in the booking_id

    print(booked_resources)

    resources = [{'uuid_id': str(x.uuid_id), 'name': x.name,
                  'checked': 'checked' if x.name in booked_resources else ''}
                 for x in resource_ids]

    print(resources)

    booking = {'uuid_display': str(x.uuid_id)[:6],
                'uuid_id': str(x.uuid_id),
                'title': x.title,
                'description': x.description,
                'user': x.user,
                'start_time': x.start_time,
                'end_time': x.end_time,
                'resources': resources # Resources are broken and need a new database-table anyway
                }

    return render_template("edit_booking.html",
        page_title="Modify booking", booking=booking)

    return "Booking not found<br><a href='/bookings'>List of bookings</a>", 404

@app.route("/bookings/update", methods=["POST"])
def update_booking():
    """Update a single booking"""
    booking_id = int(request.form["id"])
    if booking_id not in Booking.bookings:
        Booking.create(request.form["title"], request.form["user"],
            request.form["description"], request.form["start"],
            request.form["end"], request.form["resources"])
    else:
        Booking.bookings[booking_id] = Booking(
                request.form["id"], request.form["title"],
                request.form["user"], request.form["description"],
                request.form["start"], request.form["end"],
                request.form["resources"])

    return "Success!<br><a href='/bookings'>List of bookings</a>"

resources = Resources(database)

@app.route("/resources/")
def serve_resources():
    return render_template("resources.html", resources=resources.list())

