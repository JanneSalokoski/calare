"""app.py - Provide server backend for Calare"""

# from dataclasses import dataclass
from flask import Flask, render_template, request
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import text

# from result import Result, Ok, Err
from maybe import Maybe, Some, Nothing  # pyright: ignore[reportUnusedImport]

from db import DataBase

# from resource import Resource, Resources
from bookings import Bookings, Booking

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///calare"
# db = SQLAlchemy(app)

database = DataBase(app)


@app.route("/")
def index() -> str:
    """Placeholder for actual / endpoint implementation"""
    features = ["server", "user-interface"]
    return render_template("index.html", features=features)


@app.route("/admin")
def admin() -> str:
    """Placeholder for actual admin control panel implementation"""
    return "Admin control panel"


@app.route("/login")
def login() -> str:
    """Serve login.html at endpoint /login"""
    return render_template("login.html")


@app.route("/auth", methods=["POST"])
def auth() -> str | tuple[str, int]:
    """Authenticate user"""
    print("args:")
    for arg in request.args:
        print(arg)
    if request.form["username"] == "Admin" and request.form["password"] == "Qwerty":
        return render_template("login_success.html", username=request.form["username"])

    return render_template("login_failed.html"), 401


bookings = Bookings(database)


@app.route("/bookings")
def serve_bookings() -> str:
    """Serve a list of all the bookings"""
    return render_template("bookings_list.html", resources=bookings.list())


@app.route("/bookings/edit/")
def new_booking():
    """Create a new booking"""
    return render_template(
        "edit_booking.html",
        page_title="Create new booking",
        id="",
        title="",
        user="",
        description="",
        start="",
        end="",
        resources=[],
    )


@app.route("/bookings/edit/<booking_id>")
def edit_booking_with_id(booking_id: int) -> str | tuple[str, int]:
    """Edit the booking with the id"""

    match bookings.edit(booking_id):
        case Some(booking):
            print(booking.resources)
            return render_template(
                "edit_booking.html", page_title="Modify booking", booking=booking
            )
        case Nothing():
            return (
                "Booking not found<br><a href='/bookings'>List of bookings</a>",
                404,
            )

    return ""


@app.route("/bookings/update", methods=["POST"])
def update_booking():
    """Update a single booking"""
    booking_id = int(request.form["id"])
    if booking_id not in Booking.bookings:
        Booking.create(
            request.form["title"],
            request.form["user"],
            request.form["description"],
            request.form["start"],
            request.form["end"],
            request.form["resources"],
        )
    else:
        Booking.bookings[booking_id] = Booking(
            request.form["id"],
            request.form["title"],
            request.form["user"],
            request.form["description"],
            request.form["start"],
            request.form["end"],
            request.form["resources"],
        )

    return "Success!<br><a href='/bookings'>List of bookings</a>"


resources = Resources(database)  # to-do: this could be somewhere else?


@app.route("/resources/")
def serve_resources():
    return render_template("resources.html", resources=resources.list())
