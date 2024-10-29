from dataclasses import dataclass

from sqlalchemy import text
from db import DataBase

from result import Result, Ok, Err  # pyright: ignore
from maybe import Maybe, Some, Nothing

from typing import cast


@dataclass
class Resource:
    name: str
    uuid_full: str

    uuid: str | None = ""
    booked: bool | None = False
    checked: str | None = ""

    def __post_init__(self):
        self.uuid_full = str(self.uuid_full)
        self.uuid = self.uuid_full[:6]

        # We need this for the html-template since checkboxes are annoying
        self.checked = "checked" if self.booked else ""

    @classmethod
    def from_dict(cls, d: dict[str, str | int | bool | None]):
        uuid_full: str = cast(str, d["uuid_id"])
        name: str = cast(str, d["name"])
        booked: bool = cast(bool, d["booked"])

        return Resource(name, uuid_full, booked=booked)


class Resources:
    def __init__(self, database: DataBase):
        self.database: DataBase = database

    def list(self) -> Maybe[list[Resource]]:
        """Fetch resources from database"""
        # match self.database.fetch(text("SELECT uuid_id, name FROM resources")):
        #     case Ok(data):
        #         print(data)
        #         return [Resource(x.name, str(x.uuid_id)) for x in data]
        #
        #     case Err(msg):
        #         print(f"Error: {msg}")
        #         return []
        #

        match self.database.fetch(text("SELECT uuid_id, name FROM resources")):
            case Ok(data):
                match data:
                    case Some(rows):
                        # TODO: Fix type warnings?
                        return Some([Resource(x.name, str(x.uuid_id)) for x in rows])

                    case Nothing():
                        return Nothing()

            case Err(e):
                print(f"Error: {e}")
                return Nothing()
