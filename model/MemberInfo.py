# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String



class MemberInfo(Base):

    __tablename__ = 'member_info'

    id = Column(Integer, primary_key=True, autoincrement=True)

    group_name = Column(String(length=120), nullable=False)

    age= Column(Integer)

    nick_name = Column(String(length=120), nullable=False)

    sex = Column(String(length=2), nullable=False)

    city = Column(String(length=10), nullable=False)

    user_puid = Column(String(length=60))

    group_puid = Column(String(length=60))
