from dataclasses import dataclass
from sqlalchemy import text

from result import Result, Ok, Err
from maybe import Nothing, Some, Maybe

from resource import Resource

@dataclass
class Booking:
    serial_id: int
    uuid_full: str
    title: str
    resources: list[Resource]

    def __post_init__(self):
        self.uuid_full = str(self.uuid_full)
        self.uuid = self.uuid_full[:6]

    @classmethod
    def from_dict(cls, d: dict):
        serial_id = d.serial_id
        uuid_full = d.uuid_id
        title = d.title if d.title is not None else ""
        resources = []

        return Booking(serial_id, uuid_full, title, resources)
        
    
    
class Bookings:
    def __init__(self, database):
        self.database = database

    def list(self) -> list[Booking]:
        """Fetch bookings from database"""
        match self.database.fetch(text("SELECT serial_id, uuid_id, title FROM bookings")):
            case Ok(data):
                return [Booking.from_dict(row) for row in data]

            case Err(msg):
                print(f"Error: {msg}")
                return []

    def find(self, booking_id: str) -> Maybe[Booking]:
        """Find a booking with given id"""
        match self.database.fetch(text(
            "SELECT serial_id, uuid_id, title, description, user, start_time, end_time FROM bookings WHERE uuid_id=:id"
            ),
            {"id": booking_id},
            single=True
            ):
            case Ok(result):
                return Some(Booking.from_dict(result))

            case Err(msg):
                return Nothing()
    
    type ResourceList = list[Resource]
    def get_resources(self, serial_id: str) -> Maybe[ResourceList]:
        """Find a booking with given id"""
        match self.database.fetch(text(
            # Select uuid_id and name from resource
            # and add a column indicating whether the 
            # resource_id is found in the resource_bookings
            # that have booking_id matching the given serial_id
            """
            SELECT 
                resources.uuid_id, resources.name, 
                (resources.serial_id IN 
                    (SELECT resource_bookings.resource_id 
                     FROM resource_bookings WHERE resource_bookings.booking_id=:id)) as booked 
            FROM 
                resources;
            """
            ),
            {"id": serial_id},
            ):
            case Ok(result):
                print(result)
                return Some([Resource.from_dict(row) for row in result])

            case Err(msg):
                print(f"No resources found for '{serial_id}'")
                return Nothing
    

    def edit(self, booking_id):
        """Edit a booking"""
        match self.find(booking_id):
            case Some(booking):
                match self.get_resources(booking.serial_id):
                    case Some(resources):
                        booking.resources = resources

                    case Nothing:
                        booking.resources = []

                print(booking)
                return Some(booking)

            case Nothing():
                print("Booking not found")

        return Nothing
    

    
    # query = text("SELECT uuid_id, name FROM resources")
    # res = db.session.execute(query)
    # resource_ids = res.fetchall()
    #
    # # There probably is a way to combine the last two queries: select all resource.name,
    # # join with result of is resource.sreial_id in the booking_id
    #
    # print(booked_resources)
    #
    # resources = [{'uuid_id': str(x.uuid_id), 'name': x.name,
    #               'checked': 'checked' if x.name in booked_resources else ''}
    #              for x in resource_ids]
    #
    # print(resources)
    #
    # booking = {'uuid_display': str(x.uuid_id)[:6],
    #             'uuid_id': str(x.uuid_id),
    #             'title': x.title,
    #             'description': x.description,
    #             'user': x.user,
    #             'start_time': x.start_time,
    #             'end_time': x.end_time,
    #             'resources': resources # Resources are broken and need a new database-table anyway
    #             }
    #
    # return render_template("edit_booking.html",
    #     page_title="Modify booking", booking=booking)
    #
    # return "Booking not found<br><a href='/bookings'>List of bookings</a>", 404
    #
    #
