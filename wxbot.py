# -*- coding: utf-8 -*-

from wxpy import *
import re

from service import Service

bot = Bot(cache_path=True, console_qr=True, logout_callback=True)
if __name__ == '__main__':
    bot.enable_puid()
    myself = bot.self
    xiaoi = XiaoI('open_dGb1rXs7IF71', 'VespFeqKuc3B7hQQRjhV')
    xiaoi.url = "http://robot.open.xiaoi.com/ask.do"

# filter
def is_owner(msg):
    if u'武汉抢购' in msg.chat.name:
        return True
    return False

# 加入了群聊
@bot.register(Group, NOTE)
def note_group(msg):
    print msg
    if not is_owner(msg):
        print u'不是武汉抢购群'
        return

    if u'加入了群聊' in msg.text and u'邀请' in msg.text:
        add_group(msg)
    if u'加入群聊' in msg.text and u'通过扫描' in msg.text:
        add_group2(msg)
    if u'修改群名为' in msg.text:
        update_group(msg)

def update_group(msg):
    matches = re.match(u'(.+)?修改群名为(.+)', msg.text)
    current_group_name = msg.chat.name
    group_name = matches.group(2)
    
    if group_name[0] == '“' and group_name[-1] == '”':
        group_name = group_name[1:-1]
 
    Service.updateInviteInfo(current_group_name, group_name)
    msg.chat.update_group()

def add_group(msg):
    matches = re.match(u'(.+)?邀请(.+)?加入了群聊', msg.text)

    inviteer = matches.group(1)
    invitees = matches.group(2)

    if inviteer[0] == '"' and inviteer[-1] == '"':
        inviteer = inviteer[1:-1]
   
    if invitees[0] == '"' and invitees[-1] == '"':
        invitees = invitees[1:-1]

    for invitee in invitees.split(u'、'):
        if inviteer == u'你':
            inviteer = msg.member.name
        Service.addInviteInfo_Service(msg.chat.puid, msg.chat.name, inviteer, invitee)


def add_group2(msg):
    matches = re.match(u'(.+)?通过扫描(.+)?分享的二维码加入群聊', msg.text)
    invitee = matches.group(1)
    inviteer = matches.group(2)
    
    if inviteer[0] == '"' and inviteer[-1] == '"':
        inviteer = inviteer[1:-1]

    if invitee[0] == '"' and invitee[-1] == '"':
        invitee = invitee[1:-1]

    if inviteer == u'你':
        inviteer = msg.member.name
    
    Service.addInviteInfo_Service(msg.chat.puid, msg.chat.name, inviteer, invitee)


# 自动回复
@bot.register(Group, TEXT, except_self=False)
def auto_replay(msg):
    print msg
    if not is_owner(msg):
        print u'不是武汉抢购群'
        return
    
    name = msg.member.name
    group_name = msg.chat.name
    if u'我的邀请' == msg.text:
        msg.chat.update_group()

        rankInfo = Service.getRankInfo_Service(msg.chat.puid, group_name, name)
        rank = rankInfo[0]
        inviteInfos = rankInfo[1]

        invite_total_count = len(inviteInfos)
        invite_effect_count = invite_total_count

        print inviteInfos

        if invite_total_count == 0 and invite_effect_count == 0:
            rank = u'暂无排名'
        else:
            rank = 'NO.' + str(rank)

        for inviteInfo in inviteInfos:
            exist = False
            for member in msg.chat:
                if re.sub(r'<.*?>', '', inviteInfo.invitee_name).replace('?', '') in member.name:
                    exist = True
            if not exist:
                invite_effect_count = invite_effect_count - 1
        
        return my_invite_info(name, rank, invite_total_count, invite_effect_count)
    elif u'打卡' == msg.text:
        return Service.addPunchInfo_Service(msg.chat.puid, group_name, name, msg.member.puid)
    elif u'打卡记录' == msg.text:
        return Service.punchInfoRecord_Service(msg.chat.puid, group_name, name, msg.member.puid)
    elif '0-' == unicode(msg.text)[0:2] and msg.chat.owner == msg.member: # 更新邀请记录
        name = msg.text.split('-')[1]
        count = Service.updateInviteInfo(msg.chat.puid, group_name, name)
        return u'操作结果: {0}'.format(u'成功' if count > 0 else u'失败')
    else:
        if msg.is_at:
            xiaoi.do_reply(msg)

def my_invite_info(name, rank, invite_total_count, invite_effect_count):
    return u"""@{name}
你在当前群的邀请统计如下:
排名：{rank}
邀请总数: {invite_total_count}
有效邀请: {invite_effect_count}
""".format(name=name, rank=rank, invite_total_count=invite_total_count, invite_effect_count = invite_effect_count)


embed()
