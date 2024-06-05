from dataclasses import dataclass
from sqlalchemy import text

from result import Result, Ok, Err

@dataclass
class Resource:
    name: str
    uuid_full: str

    def __post_init__(self):
        self.uuid = self.uuid_full[:6]
    
    
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

    
