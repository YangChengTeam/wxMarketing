# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Boolean 



class InviteInfo(Base):

    __tablename__ = 'invite_info'

    id = Column(Integer, primary_key=True, autoincrement=True)

    group_name = Column(String(length=120), nullable=False)

    inviter_name = Column(String(length=120), nullable=False)

    invitee_name = Column(String(length=120))

    addtime = Column(Integer)

    group_puid = Column(String(length=60))

    is_used = Column(Boolean, unique=False, default=False)






