# -*- coding: utf-8 -*-
from model.InviteInfo import InviteInfo
from model.GroupInfo import GroupInfo
from model.MemberInfo import MemberInfo
from model.PunchInfo import PunchInfo

from sqlalchemy.sql import func
from sqlalchemy import desc

import time
import datetime
import calendar

import re

from sqlalchemy import extract
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_

engine = create_engine(
    "mysql+mysqlconnector://root:123456@localhost/wxinfo?charset=utf8mb4")
session = sessionmaker(engine)



# dao
def addInviteInfo(group_puid, group_name, inviter_name, invitee_name):
    mySession = session()
    inviteInfo = InviteInfo(group_puid=group_puid,
                            group_name=group_name,
                            inviter_name=inviter_name,
                            invitee_name=invitee_name,
                            addtime=int(time.time()))
    mySession.add(inviteInfo)
    mySession.commit()
    mySession.close()


def addGroupInfo(group_puid, group_name):
    mySession = session()
    groupInfo = GroupInfo(group_puid=group_puid, group_name=group_name)
    mySession.add(groupInfo)
    mySession.commit()
    mySession.close()


def addMemberInfo(group_puid, group_name, nick_name, user_puid, age, city,
                  sex):
    mySession = session()
    memberInfo = MemberInfo(group_puid=group_puid,
                            group_name=group_name,
                            nick_name=nick_name,
                            user_puid=user_puid,
                            age=age,
                            city=city,
                            sex=sex)
    mySession.add(memberInfo)
    mySession.commit()
    mySession.close()


def addPunchInfo(group_puid, group_name, nick_name, user_puid):
    mySession = session()
    punchInfo = PunchInfo(group_puid=group_puid,
                          group_name=group_name,
                          nick_name=nick_name,
                          user_puid=user_puid)
    mySession.add(punchInfo)
    mySession.commit()
    mySession.close()


def getPunchInfo(group_puid, group_name, nick_name, user_puid):
    mySession = session()
    punchInfos = mySession.query(PunchInfo, PunchInfo.addtime).filter(
        or_(PunchInfo.group_name == group_name,
            PunchInfo.group_puid == group_puid),
        or_(PunchInfo.nick_name == nick_name,
            PunchInfo.user_puid == user_puid)).order_by(desc(
                PunchInfo.addtime)).all()
    mySession.close()

    return punchInfos


def getPunchInfoByMonth(group_puid, group_name, nick_name, user_puid):
    mySession = session()
    punchInfos = mySession.query(PunchInfo, PunchInfo.addtime).filter(
        or_(PunchInfo.group_name == group_name,
            PunchInfo.group_puid == group_puid),
        or_(PunchInfo.nick_name == nick_name,
            PunchInfo.user_puid == user_puid),
        func.date_format(
            PunchInfo.addtime,
            "%Y-%m") == datetime.datetime.now().strftime('%Y-%m')).order_by(
                desc(PunchInfo.addtime)).all()
    mySession.close()

    return punchInfos


def getInviteInfo(group_puid, group_name, inviter_name):
    mySession = session()
    inviteInfos = mySession.query(
        InviteInfo, InviteInfo.id, InviteInfo.group_name,
        InviteInfo.inviter_name, InviteInfo.invitee_name).filter(
            InviteInfo.is_used == False,
            or_(InviteInfo.group_name == group_name,
                InviteInfo.group_puid == group_puid),
            InviteInfo.inviter_name == inviter_name).all()
    mySession.close()

    return inviteInfos


def getInviteInfo2(group_puid, group_name, invitee_name):
    mySession = session()
    inviteInfos = mySession.query(
        InviteInfo, InviteInfo.id, InviteInfo.group_name,
        InviteInfo.inviter_name, InviteInfo.invitee_name).filter(
            or_(InviteInfo.group_name == group_name,
                InviteInfo.group_puid == group_puid),
            InviteInfo.invitee_name == invitee_name).all()
    mySession.close()

    return inviteInfos


def getInviteInfo3(group_puid, group_name, inviter_name):
    mySession = session()
    inviteInfos1 = mySession.query(
        InviteInfo, InviteInfo.id, InviteInfo.group_name,
        InviteInfo.inviter_name, InviteInfo.invitee_name).filter(
            InviteInfo.is_used == False,
            or_(InviteInfo.group_name == group_name,
                InviteInfo.group_puid == group_puid),
            InviteInfo.inviter_name == inviter_name).all()
    inviteInfos2 = mySession.query(
        InviteInfo, InviteInfo.inviter_name, func.count(InviteInfo.id)).filter(
            InviteInfo.is_used == False,
            or_(InviteInfo.group_name == group_name,
                InviteInfo.group_puid == group_puid)).group_by(
                    InviteInfo.inviter_name).order_by(
                        desc(func.count(InviteInfo.id))).all()
    mySession.close()

    return [inviteInfos1, inviteInfos2]


def updateInviteInfo(group_puid, group_name, inviter_name):
    mySession = session()
    count = mySession.query(InviteInfo).filter(
        InviteInfo.is_used == False,
        or_(InviteInfo.group_name == group_name,
            InviteInfo.group_puid == group_puid),
        InviteInfo.inviter_name == inviter_name).update(
            {InviteInfo.is_used: True})
    mySession.commit()
    mySession.close()
    
    return count


# service
def addInviteInfo_Service(group_puid, group_name, inviter_name, invitee_name):
    if len(getInviteInfo2(group_puid, group_name, invitee_name)) == 0:
        inviter_name = re.sub(r'<.*?>', '', inviter_name).replace('?', '')
        invitee_name = re.sub(r'<.*?>', '', invitee_name).replace('?', '')
        addInviteInfo(group_puid, group_name, inviter_name, invitee_name)


def addPunchInfo_Service(group_puid, group_name, nick_name, user_puid):
    date2 = datetime.datetime.now()
    if date2.hour >= 8 and date2.hour < 10:
        punchInfos = getPunchInfo(group_puid, group_name, nick_name, user_puid)
        if len(punchInfos) > 0:
            punchInfo = punchInfos[0]
            date1 = punchInfo.addtime.strftime('%Y-%m-%d')
            date2 = datetime.datetime.now()
            if date1 == date2.strftime('%Y-%m-%d'):
                return u'已经打过卡了~'
        addPunchInfo(group_puid, group_name, nick_name, user_puid)
        return u'打卡成功'

    else:
        return u'不在打卡范围内，打卡时间为早上8点—10点~'


def punchInfoRecord_Service(group_puid, group_name, nick_name, user_puid):
    punchInfos = getPunchInfoByMonth(group_puid, group_name, nick_name,
                                     user_puid)

    date2 = datetime.datetime.now()
    mdays = calendar.monthrange(date2.year, date2.month)[1]
    m = len(punchInfos)
    n = 0

    for punchInfo in punchInfos:
        date1Str = punchInfo.addtime.strftime('%Y-%m-%d')
        data2Str = str(date2.year) + "-" + (str(date2.month) if (
            date2.month > 9) else str('0') + str(date2.month)) + "-" + (
                str(date2.day - n) if
                (date2.day - n > 9) else str('0') + str(date2.day - n))
        if date1Str == data2Str:
            n += 1
        else:
            break
    return u"""@{nick_name}
本月一共{mdays}天，已打卡{m}天，已连续签到{n}天。""".format(nick_name=nick_name,
                                          mdays=mdays,
                                          m=m,
                                          n=n)


def getRankInfo_Service(group_puid, group_name, inviter_name):
    inviteInfos = getInviteInfo3(group_puid, group_name, inviter_name)
    rank = 0
    for row in inviteInfos[1]:
        rank = rank + 1
        if row.inviter_name == inviter_name:
            break
    return [rank, inviteInfos[0]]


# get group and member infos
def addGroupMemberInfos_Service(bot):
    for group in bot.groups():
        Service.addGroupInfo(group.puid, group.name)
        for member in group.members:
            Service.addMemberInfo(group.puid, group.name, member.name,
                                  member.puid, 0, '', '')



