"""db.py - Provide access to the database"""

from collections.abc import Sequence
from typing import Any
from result import Result, Ok, Err
from maybe import Maybe, Some, Nothing

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Row
import flask


class DataBase:
    """Provide access to the database"""

    def __init__(self, app: flask.Flask):
        self.app: flask.Flask = app
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///calare"
        self.db: SQLAlchemy = SQLAlchemy(app)

    def fetch(
        self,
        query: sqlalchemy.sql.expression.Executable,
        params: dict[str, str] | None = None,
        single: bool = False,
    ) -> Result[Maybe[list[Row[Any]] | Row[Any]], Exception]:
        """Executes a query and returns the results"""

        params = params if params is not None else {}

        try:
            result = self.db.session.execute(statement=query, params=params)

            res: Sequence[Row[Any]] | Row[Any] | None = None
            if single:
                res = result.fetchone()
                if res is not None:
                    return Ok(Some(res))
                else:
                    return Ok(Nothing())

            res = result.fetchall()
            if len(res) > 0:
                return Ok(Some(list(res)))
            else:
                return Ok(Nothing())

        # TODO: Differentiante between exception types
        except Exception as e:
            print(e)  # TODO: Add logging
            return Err(e)
