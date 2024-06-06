""" db.py - Provide access to the database """

from flask_sqlalchemy import SQLAlchemy
from result import Result, Ok, Err

class DataBase:
    """Provide access to the database"""

    def __init__(self, app):
        self.app = app
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///calare"
        self.db = SQLAlchemy(app)

    def fetch(self, query: str, params: dict = None, single: bool = False) -> Result[list, str]:
        """Executes a query and returns the results"""

        params = params if params is not None else {}

        try:
            result = self.db.session.execute(query, params)

            if single:
                return Ok(result.fetchone())

            return Ok(result.fetchall())

        except Exception as e: # to-do: differentiate between exceptions
            print(e)
            return Err("Error fetching data from database")
        
