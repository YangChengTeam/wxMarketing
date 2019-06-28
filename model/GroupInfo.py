# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String



class GroupInfo(Base):

    __tablename__ = 'group_info'

    id = Column(Integer, primary_key=True, autoincrement=True)

    group_name = Column(String(length=120), nullable=False)

    group_puid = Column(String(length=60))




