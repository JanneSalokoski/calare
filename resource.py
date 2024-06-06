from dataclasses import dataclass
from typing import Optional

from sqlalchemy import text

from result import Result, Ok, Err


@dataclass
class Resource:
    name: str
    uuid_full: str
    booked: Optional[bool] = False

    def __post_init__(self):
        self.uuid_full = str(self.uuid_full)
        self.uuid = self.uuid_full[:6]

        # We need this for the html-template since checkboxes are annoying
        self.checked = "checked" if self.booked else ""

    @classmethod
    def from_dict(cls, d: dict):
        uuid_full = d.uuid_id
        name = d.name
        booked = d.booked

        return Resource(name, uuid_full, booked)
    
    
class Resources:
    def __init__(self, database):
        self.database = database

    def list(self) -> list[Resource]:
        """Fetch resources from database"""
        match self.database.fetch(text("SELECT uuid_id, name FROM resources")):
            case Ok(data):
                print(data)
                return [Resource(x.name, str(x.uuid_id)) for x in data]

            case Err(msg):
                print(f"Error: {msg}")
                return []

    

    
