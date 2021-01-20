# -*- coding: UTF-8 -*-

from threading import Timer
from mixin_ws_api import MIXIN_WS_API
from mixin_api import MIXIN_API
import mixin_config


import json
import time
from io import BytesIO
import base64
import gzip
import sqlite3

try:
    import thread
except ImportError:
    import _thread as thread

def on_message(ws, message):
    con = sqlite3.connect("subscribe.db")
    cur = con.cursor()


    inbuffer = BytesIO(message)
    f = gzip.GzipFile(mode="rb", fileobj=inbuffer)
    rdata_injson = f.read()
    # print(rdata_injson)
    rdata_obj = json.loads(rdata_injson)
    print(rdata_obj)
    action = rdata_obj["action"]


    if action not in ["ACKNOWLEDGE_MESSAGE_RECEIPT", "CREATE_MESSAGE", "LIST_PENDING_MESSAGES"]:
        print("unknow action")
        return

    if action == "ACKNOWLEDGE_MESSAGE_RECEIPT":
        return

    if action == "CREATE_MESSAGE":
        data = rdata_obj["data"]
        msgid = data["message_id"] #1
        typeindata = data["type"] #1
        categoryindata = data["category"] #1

        userId = data["user_id"]
        print("userID",userId)

        conversationId = data["conversation_id"]
        dataindata = data["data"]
        created_at = data["created_at"]
        updated_at = data["updated_at"]

        realData = base64.b64decode(dataindata)
        MIXIN_WS_API.replayMessage(ws, msgid)



        # now_hour = time.strftime("%H", time.localtime())
        # now_min = time.strftime("%M", time.localtime())
        # a = int(now_hour)
        # print(a)


        # print('id', userId) #创建人id
        # print("创建时间",created_at)
        # print("更新时间",updated_at)


        if 'error' in rdata_obj:
            return

        if categoryindata not in ["SYSTEM_ACCOUNT_SNAPSHOT", "PLAIN_TEXT", "SYSTEM_CONVERSATION", "PLAIN_STICKER", "PLAIN_IMAGE", "PLAIN_CONTACT"]:
            print("unknow category")
            return

        if categoryindata == "PLAIN_TEXT" and typeindata == "message":
            realData = realData.lower().decode('utf-8')


            if '你好' == realData:
                introductionContent = '欢迎使用水龙头微习惯智能小助手~'
                a = '现在你可以点击订阅，订阅之后小助手会每天早上八点提醒你签到哦~'
                MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent)
                MIXIN_WS_API.sendUserText(ws, conversationId, userId, a)
                btns = [{"label":"订阅","action":"input:订阅","color":"#0084ff"},{"label":"取消订阅","action":"input:取消订阅","color":"#FF8000"}]
                MIXIN_WS_API.sendAppButtonGroup(ws, conversationId, userId, btns)
                MIXIN_WS_API.sendUserImg(ws,conversationId,userId,img)
                return

            if '签到' == realData:
                print('sign in')
                introductionContent = '点击下方的名片进行签到~,签到完成后请点击已签到~'
                MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent)
                MIXIN_WS_API.sendUserContactCard(ws, conversationId, userId, "71ae9403-9d20-4772-b47a-729e0cc3648b")
                MIXIN_WS_API.sendUserAppButton(ws, conversationId, userId, "input:Ok", "已签到")
                return

            if 'sign in' ==realData:
                print('签到成功')
                introductionContent = '明天再见~'
                MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent)
                cur.execute("update test set flag=1 where user_id=?",(userId,))
                con.commit()
                return


            if 'learn' ==realData:
                print('学习成功')
                introductionContent = '明天再见~'
                MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent)
                cur.execute("update test set task_wall=1 where user_id=?", (userId,))
                con.commit()
                return


            if 'luck draw' ==realData:
                print('水龙头啊~ 水龙头~')
                introductionContent = '明天再见~'
                MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent)
                cur.execute("update test set shuilongtou=1 where user_id=?", (userId,))
                con.commit()
                return

            if 'matter'  == realData:
                print('Go and answer the questions')
                introductionContent = '请点击下方的名片进行答题~'
                MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent)
                MIXIN_WS_API.sendUserContactCard(ws, conversationId, userId, "0fa27e96-e421-4f16-8629-121bf047ade8")
                return



            if '订阅' == realData:
                print('调用方法')
                demo = (str(userId))
                squrl = cur.execute('select * from shouquan where user_id=?',(demo,)).fetchall()
                if len(squrl)==0:
                    introductionContent = '在使用订阅前得先授权嗷，请点击下方按钮进行授权'
                    MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent)
                    MIXIN_WS_API.sendUserAppButton(ws, conversationId, userId, "https://mixin-www.zeromesh.net/oauth/authorize?client_id=959f944f-603f-437c-a566-9acc1c0e070e&scope=PROFILE:READ+PHONE:READ+CONTACTS:READ+ASSETS:READ+SNAPSHOTS:READ&response_type=code&return_to=http://122.9.51.227:8888/auth", "点击授权")
                else:

                    # luck btc
                    introductionContent = '订阅成功,现在你可以点击下方名片进行签到了,签到完成不要忘记点击已签到按钮哦~'
                    MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent)
                    MIXIN_WS_API.sendUserContactCard(ws, conversationId, userId, "71ae9403-9d20-4772-b47a-729e0cc3648b")
                    btns = [{"label": "一键直达签到", "action": "https://bonus.mixin.zone/tasks", "color": "#FF8000"},
                            {"label": "去答题", "action": "input:matter", "color": "#0084ff"},
                            {"label": "已签到", "action": "input:sign in", "color": "#0084ff"}]
                    MIXIN_WS_API.sendAppButtonGroup(ws, conversationId, userId, btns)

                    # task wall
                    MIXIN_WS_API.sendUserContactCard(ws, conversationId, userId, "e08207df-55de-4ad9-8463-af692824f988")
                    btns = [{"label": "一键直达每日课堂", "action": "https://taskwall.mixin.zone/", "color": "#FF8000"},
                            {"label": "已学习", "action": "input:learn", "color": "#0084ff"}]
                    MIXIN_WS_API.sendAppButtonGroup(ws, conversationId, userId, btns)

                    # 水龙头APP
                    MIXIN_WS_API.sendUserContactCard(ws, conversationId, userId, "1da1124a-9c97-4f2b-b332-f11f77c7604a")
                    btns = [{"label": "一键直达抽奖", "action": "https://app.exinearn.com/?isRobot=1#/discover", "color": "#FF8000"},
                            {"label": "已抽奖", "action": "input:luck draw", "color": "#0084ff"}]
                    MIXIN_WS_API.sendAppButtonGroup(ws, conversationId, userId, btns)

                    data = (str(userId),str(conversationId))
                    res = cur.execute('select * from test where user_id=? and conversation_id=?',(data)).fetchall()
                    if len(res)==0:
                        cur.execute('INSERT INTO test(user_id,conversation_id) VALUES (?,?)' ,data)
                        con.commit()
                        return


            if '取消订阅' == realData:
                introductionContent = '取消订阅成功,没有小助手的提醒你也要按时签到哦~'
                MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent)
                cur.execute('DELETE FROM test where user_id=?',(userId,))
                con.commit()
                return


        elif categoryindata == "PLAIN_TEXT":
            print("PLAIN_TEXT but unkonw:")





if __name__ == "__main__":

    mixin_api = MIXIN_API(mixin_config)
    mixin_ws = MIXIN_WS_API(on_message=on_message)
    def checkrun(*args):
        while True:
            mixin_ws = MIXIN_WS_API(on_message=on_message)
            if not mixin_ws.ws.sock:
                mixin_ws = MIXIN_WS_API(on_message=on_message)
                mixin_ws.run()
            time.sleep(10)
    thread.start_new_thread(checkrun, ())
    while True:
        time.sleep(3600)










