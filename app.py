from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    features = ["server", "user-interface"]
    return render_template("index.html", features=features)

@app.route("/admin")
def admin():
    return "Admin control panel"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/auth", methods=["POST"])
def auth():
    print("args:")
    for arg in request.args:
        print(arg)
    if request.form["username"] == "Admin" and request.form["password"] == "Qwerty":
        return render_template("login_success.html", username=request.form["username"])
    else:
        return render_template("login_failed.html"), 401

class Resource:
    def __init__(self, resource_id, name):
        self.id = resource_id
        self.name = name

resources = [
    Resource("001", "Room A"),
    Resource("002", "Room B"),
    Resource("003", "Room C"),
]

class Booking:
    bookings = {}

    def __init__(self, booking_id=0, title="", user="",
                 description="", start="", end="", resources=None):

        self.id = booking_id
        self.title = title
        self.user = user
        self.description = description
        self.start = start
        self.end = end
        self.resources = resources if resources is not None else []

    def get_resource_list(self):
        res = []
        for resource in resources:
            print(resource)
            if resource.id in self.resources:
                res.append(("checked", resource))
            else:
                res.append(("", resource))

        return res

    def create(title="", user="", description="", start="", end="", resources=None):
        resources = resources if resources is not None else []

        id = len(dict.keys(Booking.bookings))
        booking = Booking(id, title, user, description, start, end, resources)
        Booking.bookings[id] = booking

        return booking

@app.route("/bookings")
def bookings_list():
    return render_template("bookings_list.html",
        bookings=dict.values(Booking.bookings))


@app.route("/bookings/edit/")
def edit_booking():
    booking = Booking()
    return render_template("edit_booking.html",
        page_title="Create new booking", id=booking.id, title=booking.id,
        user=booking.user, description=booking.description,
        start=booking.start, end=booking.end,
        resources=booking.get_resource_list())

@app.route("/bookings/edit/<id>")
def edit_booking_with_id(id):
    id = int(id)
    if id in Booking.bookings:
        booking = Booking.bookings[id]
        return render_template("edit_booking.html",
            page_title="Modify booking", id=booking.id, title=booking.title,
            user=booking.user, description=booking.description,
            start=booking.start, end=booking.end,
            resources=booking.get_resource_list())

    return "Booking not found<br><a href='/bookings'>List of bookings</a>", 404

@app.route("/bookings/update", methods=["POST"])
def update_booking():
    id = int(request.form["id"])
    if id not in Booking.bookings:
        Booking.create(request.form["title"], request.form["user"],
            request.form["description"], request.form["start"],
            request.form["end"], request.form["resources"])
    else:
        Booking.bookings[id] = Booking(
                request.form["id"], request.form["title"],
                request.form["user"], request.form["description"],
                request.form["start"], request.form["end"],
                request.form["resources"])

    return "Success!<br><a href='/bookings'>List of bookings</a>"









