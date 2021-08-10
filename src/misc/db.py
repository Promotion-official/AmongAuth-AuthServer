
from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base 

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
  end_at = Column(DateTime(), default=datetime.now(timezone(Config.TIME_ZONE)) + timedelta(minutes=10))

  def __init__(self, **kwargs):
    self.client_id = kwargs["client_id"]
    self.email = kwargs["email"]
    self.code = kwargs["code"]
    