  # -*- coding: UTF-8 -*-

from threading import Timer
from mixin_ws_api import MIXIN_WS_API
from mixin_api import MIXIN_API
import mixin_config

import schedule
import json
import time
from io import BytesIO
import base64
import gzip
import sqlite3


# 可以指定创建数据库的路径，比如可以写成sqlite3.connect(r"E:\DEMO.db")
con = sqlite3.connect("1.db")
cur = con.cursor()
sql = "CREATE TABLE IF NOT EXISTS shouquan(id INTEGER PRIMARY KEY,full_name TEXT,user_id TEXT)"
cur.execute(sql)








# print(cur.fetchall())
# try:
#     import thread
# except ImportError:
#     import _thread as thread
#
# def subscribe(ws,message):
#     inbuffer = BytesIO(message)
#
#     f = gzip.GzipFile(mode="rb", fileobj=inbuffer)
#     rdata_injson = f.read()
#     rdata_obj = json.loads(rdata_injson)
#     action = rdata_obj["action"]
#
#     if action not in ["ACKNOWLEDGE_MESSAGE_RECEIPT", "CREATE_MESSAGE", "LIST_PENDING_MESSAGES"]:
#         print("unknow action")
#         return
#
#     if action == "ACKNOWLEDGE_MESSAGE_RECEIPT":
#         return
#
#     if action == "CREATE_MESSAGE":
#         data = rdata_obj["data"]
#         msgid = data["message_id"]  # 1
#         typeindata = data["type"]  # 1
#         categoryindata = data["category"]  # 1
#         userId = data["user_id"]
#         conversationId = data["conversation_id"]
#         dataindata = data["data"]
#         created_at = data["created_at"]
#         updated_at = data["updated_at"]
#
#         realData = base64.b64decode(dataindata)
#         MIXIN_WS_API.replayMessage(ws, msgid)
#
#         if 'error' in rdata_obj:
#             return
#
#         if categoryindata not in ["SYSTEM_ACCOUNT_SNAPSHOT", "PLAIN_TEXT", "SYSTEM_CONVERSATION", "PLAIN_STICKER",
#                                   "PLAIN_IMAGE", "PLAIN_CONTACT"]:
#             print("unknow category")
#             return
#
#         if categoryindata == "PLAIN_TEXT" and typeindata == "message":
#             realData = realData.lower().decode('utf-8')
#
#         introductionContent = '订阅成功,小助手将会在每天早上八点提醒你签到~,现在你可以点击下方名片进行签到~'
#         MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent)
#         MIXIN_WS_API.sendUserContactCard(ws, conversationId, userId, "71ae9403-9d20-4772-b47a-729e0cc3648b")
#
# ### 定时任务
# schedule.every().day.at("08:00").do(subscribe)
# while True:
#     schedule.run_pending()
#     time.sleep(1)







