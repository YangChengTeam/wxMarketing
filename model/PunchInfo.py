# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func

class PunchInfo(Base):

    __tablename__ = 'punch_info'

    id = Column(Integer, primary_key=True, autoincrement=True)

    group_name = Column(String(length=120), nullable=False)

    nick_name = Column(String(length=120), nullable=False)

    addtime = Column(TIMESTAMP, default = func.now())

    user_puid = Column(String(length=60))

    group_puid = Column(String(length=60))
