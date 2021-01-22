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
    # 后台返回参数----
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


        if 'error' in rdata_obj:
            return

        if categoryindata not in ["SYSTEM_ACCOUNT_SNAPSHOT", "PLAIN_TEXT", "SYSTEM_CONVERSATION", "PLAIN_STICKER", "PLAIN_IMAGE", "PLAIN_CONTACT"]:
            print("unknow category")
            return

        if categoryindata == "PLAIN_TEXT" and typeindata == "message":
            realData = realData.lower().decode('utf-8')
            
            # 第一次关注机器人的时候系统默认 用户发送关键字为你好，会主动发送这条消息。。
            if '你好' == realData:
                introductionContent = '欢迎使用卢本伟智能小助手'
                a = '现在你可以点击订阅，订阅之后每天早上八点提醒你斗地主'
                MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent)
                MIXIN_WS_API.sendUserText(ws, conversationId, userId, a)
                btns = [{"label":"订阅","action":"input:订阅","color":"#0084ff"},{"label":"取消订阅","action":"input:取消订阅","color":"#FF8000"}]
                MIXIN_WS_API.sendAppButtonGroup(ws, conversationId, userId, btns)
                return

            if '订阅' == realData:
                print('调用方法')
                demo = (str(userId))
                squrl = cur.execute('select * from shouquan where user_id=?',(demo,)).fetchall()  # 这里是查询授权表
                if len(squrl)==0:
                    introductionContent = '在使用订阅前得先授权嗷，请点击下方按钮进行授权'
                    MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent)
                    MIXIN_WS_API.sendUserAppButton(ws, conversationId, userId, "https://mixin-www.zeromesh.net/oauth/authorize?client_id=''''?''''&scope=PROFILE:READ+PHONE:READ+CONTACTS:READ+ASSETS:READ+SNAPSHOTS:READ&response_type=code&return_to='机器人验证地址'", "点击授权")
                else:

                    introductionContent = '订阅成功,现在你可以斗地主了'
                    MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent)
                    btns = [{"label": "一键直达", "action": "https://qqgame.qq.com/game/105.shtml", "color": "#FF8000"}]
                    MIXIN_WS_API.sendAppButtonGroup(ws, conversationId, userId, btns)
                    
                    # 获取用户ID 和 会话ID
                    data = (str(userId),str(conversationId))
                    res = cur.execute('select * from test where user_id=? and conversation_id=?',(data)).fetchall()
                    if len(res)==0:
                        cur.execute('INSERT INTO test(user_id,conversation_id) VALUES (?,?)' ,data)
                        con.commit()
                        return


            if '取消订阅' == realData:
                introductionContent = '取消订阅成功,没有卢本伟的提醒你也要按时斗地主'
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










