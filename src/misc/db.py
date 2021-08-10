from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from fastapi_sqlalchemy import db

from datetime import datetime, timedelta, timezone

from misc.config import Config

Base = declarative_base()


class Code(Base):
    __tablename__ = "codes"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    created_at = Column(DateTime(), default=datetime.now(timezone(Config.TIME_ZONE)))
    end_at = Column(
        DateTime(),
        default=datetime.now(timezone(Config.TIME_ZONE)) + timedelta(minutes=10),
    )

    def __init__(self, **kwargs):
        self.client_id = kwargs["client_id"]
        self.email = kwargs["email"]
        self.code = kwargs["code"]


## TODO db connect 데코레이터 있으면 좋겠네
class CodeController:
    def __init__(self):
        pass

    @staticmethod
    def generate(**kwargs):
        con = db.session
        code = Code(kwargs)

        con.add(code)
        con.commit()
        con.refresh(code)

    @staticmethod
    def delete(**kwargs):
        con = db.session

        code = (
            con.query(Code)
            .filter(
                Code.client_id == kwargs["client_id"] and Code.email == kwargs["email"]
            )
            .first()
        )
        con.delete(code)
        con.commit()

    @staticmethod
    def get(code: str):
        con = db.session

        return con.query(Code).filter(Code.code == code).first()
