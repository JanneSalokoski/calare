""" db.py - Provide access to the database """

from flask_sqlalchemy import SQLAlchemy
from result import Result, Ok, Err

class DataBase:
    """Provide access to the database"""

    def __init__(self, app):
        self.app = app
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///calare"
        self.db = SQLAlchemy(app)

    def fetch(self, query: str) -> Result[list, str]:
        """Executes a query and returns the results"""
        try:
            result = self.db.session.execute(query)
            return Ok(result.fetchall())

        except Exception: # to-do: differentiate between exceptions
            return Err("Error fetching data from database")
        
