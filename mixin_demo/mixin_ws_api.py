# -*- coding: UTF-8 -*-


import sqlite3
import json
import uuid
import gzip
import time
from io import BytesIO
import base64
import websocket
import mixin_config
from mixin_api import MIXIN_API

try:
    import thread
except ImportError:
    import _thread as thread







class MIXIN_WS_API:

    def __init__(self, on_message, on_open=None, on_error=None, on_close=None, on_data=None):

        mixin_api = MIXIN_API(mixin_config)
        encoded = mixin_api.genGETJwtToken('/', "", str(uuid.uuid4()))

        if on_open is None:
            on_open = MIXIN_WS_API.__on_open

        if on_close is None:
            on_close = MIXIN_WS_API.__on_close

        if on_error is None:
            on_error = MIXIN_WS_API.__on_error

        if on_data is None:
            on_data = MIXIN_WS_API.__on_data
#   .decode()
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("wss://blaze.mixin.one/",
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close,
                                    header=["Authorization:Bearer " + encoded.decode()],
                                    subprotocols=["Mixin-Blaze-1"],
                                    on_data=on_data)

        self.ws.on_open = on_open

    """
    run websocket server forever
    """
    def run(self):
        self.ws.run_forever()

    """
    ========================
    WEBSOCKET DEFAULT METHOD
    ========================
    """

    """
    on_open default
    """
    @staticmethod
    def __on_open(ws):

        def run(*args):
            print("ws open")
            Message = {"id": str(uuid.uuid1()), "action": "LIST_PENDING_MESSAGES"}
            Message_instring = json.dumps(Message)

            fgz = BytesIO()
            gzip_obj = gzip.GzipFile(mode='wb', fileobj=fgz)
            gzip_obj.write(Message_instring.encode())
            gzip_obj.close()
            ws.send(fgz.getvalue(), opcode=websocket.ABNF.OPCODE_BINARY)
            while True:
                time.sleep(1)
        def jobday():
            while True:
                now_hour = time.strftime("%H", time.localtime())
                now_min = time.strftime("%M", time.localtime())
                con = sqlite3.connect("subscribe.db")
                cur = con.cursor()
                if now_hour=='08' and now_min=='00':
                    userids = cur.execute("select user_id,conversation_id from test where flag=0").fetchall()
                    for u in userids:
                        a = '签到时间到~ 签到完成后，记得点击已签到按钮哦，点击之后今天不再提醒~'
                        MIXIN_WS_API.sendUserText(ws, u[1], u[0], a)
                        MIXIN_WS_API.sendUserContactCard(ws, u[1], u[0], '71ae9403-9d20-4772-b47a-729e0cc3648b')
                        btns = [{"label": "一键直达签到", "action": "https://bonus.mixin.zone/tasks", "color": "#FF8000"},
                                {"label": "去答题", "action": "input:matter", "color": "#0084ff"},
                                {"label": "已签到", "action": "input:sign in", "color": "#0084ff"}]
                        MIXIN_WS_API.sendAppButtonGroup(ws, u[1], u[0], btns)
                        time.sleep(60)
                    time.sleep(1)

                if now_hour=='08' and now_min=='00':
                    userids = cur.execute("select user_id,conversation_id from test where task_wall=0").fetchall()
                    for u in userids:
                        MIXIN_WS_API.sendUserContactCard(ws, u[1],  u[0], "e08207df-55de-4ad9-8463-af692824f988")
                        btns = [{"label": "一键直达每日课堂", "action": "https://taskwall.mixin.zone/","color": "#FF8000"},
                                {"label": "已学习", "action": "input:learn", "color": "#0084ff"}]
                        MIXIN_WS_API.sendAppButtonGroup(ws, u[1], u[0], btns)
                        time.sleep(60)
                    time.sleep(1)

                if now_hour == '08' and now_min == '00':
                    userids = cur.execute("select user_id,conversation_id from test where shuilongtou=0").fetchall()
                    for u in userids:
                        MIXIN_WS_API.sendUserContactCard(ws, u[1], u[0], "1da1124a-9c97-4f2b-b332-f11f77c7604a")
                        btns = [{"label": "一键直达抽奖", "action": "https://app.exinearn.com/?isRobot=1#/discover", "color": "#FF8000"},
                                {"label": "已抽奖", "action": "input:luck draw", "color": "#0084ff"}]
                        MIXIN_WS_API.sendAppButtonGroup(ws, u[1], u[0], btns)
                    time.sleep(60)
                time.sleep(1)

        def updateflag():
            while True:
                now_hour = time.strftime("%H", time.localtime())
                now_min = time.strftime("%M", time.localtime())
                con = sqlite3.connect("subscribe.db")
                cur = con.cursor()
                if now_hour=='00' and now_min=='00':
                    cur.execute("update test set flag=0 where 1=1")
                    cur.execute("update test set task_wall=0 where 1=1")
                    cur.execute("update test set shuilongtou=0 where 1=1")
                    con.commit()
                    time.sleep(3600*23)
                time.sleep(1)


        def jobhour():
            while True:
                now_hour = time.strftime("%H", time.localtime())
                now_min = time.strftime("%M", time.localtime())
                con = sqlite3.connect("subscribe.db")
                cur = con.cursor()
                if int(now_hour)>8 and now_min=='00':
                    userids = cur.execute("select user_id,conversation_id from Test where flag=0").fetchall()
                    for u in userids:
                        a = '你今天还没有签到哦~ 赶紧点击下边的名片进行签到吧，签到完成记得点击已签到按钮,今日不在提醒哦~'
                        MIXIN_WS_API.sendUserText(ws, u[1], u[0], a)
                        MIXIN_WS_API.sendUserContactCard(ws, u[1], u[0], '71ae9403-9d20-4772-b47a-729e0cc3648b')
                        btns = [{"label": "一键直达签到", "action": "https://bonus.mixin.zone/tasks", "color": "#FF8000"},
                                {"label": "去答题", "action": "input:matter", "color": "#0084ff"},
                                {"label": "已签到", "action": "input:ok", "color": "#0084ff"}]
                        MIXIN_WS_API.sendAppButtonGroup(ws, u[1], u[0], btns)
                        time.sleep(3600)
                    time.sleep(1)

                if int(now_hour) > 8 and now_min == '00':
                    userids = cur.execute("select user_id,conversation_id from Test where task_wall=0").fetchall()
                    for u in userids:
                        a = '你今天还没有学习哦~ 赶紧点击下边的名片进行学习吧，签到完成记得点击已学习按钮,今日不在提醒哦~'
                        MIXIN_WS_API.sendUserText(ws, u[1], u[0], a)
                        MIXIN_WS_API.sendUserContactCard(ws, u[1], u[0],"e08207df-55de-4ad9-8463-af692824f988")
                        btns = [{"label": "一键直达每日课堂", "action": "https://app.exinearn.com/?isRobot=1#/discover","color": "#FF8000"},
                                {"label": "已学习", "action": "input:ok", "color": "#0084ff"}]
                        MIXIN_WS_API.sendAppButtonGroup(ws, u[1], u[0], btns)
                        time.sleep(3600)
                    time.sleep(1)

                if int(now_hour) > 8 and now_min == '00':
                    userids = cur.execute("select user_id,conversation_id from Test where shuilongtou=0").fetchall()
                    for u in userids:
                        a = '你今天还没有抽奖哦~ 赶紧点击下边的名片进行抽奖吧，签到完成记得点击已抽奖按钮,今日不在提醒哦~'
                        MIXIN_WS_API.sendUserText(ws, u[1], u[0], a)
                        MIXIN_WS_API.sendUserContactCard(ws, u[1], u[0],"1da1124a-9c97-4f2b-b332-f11f77c7604a")
                        btns = [{"label": "一键直达抽奖", "action": "https://taskwall.mixin.zone/", "color": "#FF8000"},
                                {"label": "已抽奖", "action": "input:ok", "color": "#0084ff"}]
                        MIXIN_WS_API.sendAppButtonGroup(ws, u[1], u[0], btns)
                    time.sleep(3600)
                time.sleep(1)

        thread.start_new_thread(run, ())
        thread.start_new_thread(jobday, ())
        thread.start_new_thread(jobhour, ())
        thread.start_new_thread(updateflag, ())
        now_hour = time.strftime("%H", time.localtime())
        print(int(now_hour))

    """
    on_data default
    """
    @staticmethod
    def __on_data(ws, readableString, dataType, continueFlag):
        return

    """
    on_close default
    """

    @staticmethod
    def __on_close(ws):
        print("on close")
        return

    """
    on_error default
    """

    @staticmethod
    def __on_error(ws, error):
        print(error)


    """
    =================
    REPLY USER METHOD
    =================
    """

    """
    generate a standard message base on Mixin Messenger format
    """

    @staticmethod
    def writeMessage(websocketInstance, action, params):

        message = {"id": str(uuid.uuid1()), "action": action, "params": params}
        message_instring = json.dumps(message)
        fgz = BytesIO()
        gzip_obj = gzip.GzipFile(mode='wb', fileobj=fgz)
        gzip_obj.write(message_instring.encode())
        gzip_obj.close()
        websocketInstance.send(fgz.getvalue(), opcode=websocket.ABNF.OPCODE_BINARY)

    """
    when receive a message, must reply to server
    ACKNOWLEDGE_MESSAGE_RECEIPT ack server received message
    """
    @staticmethod
    def replayMessage(websocketInstance, msgid):
        parameter4IncomingMsg = {"message_id": msgid, "status": "READ"}
        Message = {"id": str(uuid.uuid1()), "action": "ACKNOWLEDGE_MESSAGE_RECEIPT", "params": parameter4IncomingMsg}
        Message_instring = json.dumps(Message)
        fgz = BytesIO()
        gzip_obj = gzip.GzipFile(mode='wb', fileobj=fgz)
        gzip_obj.write(Message_instring.encode())
        gzip_obj.close()
        websocketInstance.send(fgz.getvalue(), opcode=websocket.ABNF.OPCODE_BINARY)
        return

    """
    reply a button to user     向用户回复按钮  网址
    """
    @staticmethod
    def sendUserAppButton(websocketInstance, in_conversation_id, to_user_id, realLink, text4Link, colorOfLink="#0084ff"):
        btn = '[{"label":"' + text4Link + '","action":"' + realLink + '","color":"' + colorOfLink + '"}]'
        print(btn)
        btn = base64.b64encode(btn.encode('utf-8')).decode(encoding='utf-8')
        params = {"conversation_id": in_conversation_id, "recipient_id": to_user_id, "message_id": str(uuid.uuid4()),
                  "category": "APP_BUTTON_GROUP", "data": btn}
        return MIXIN_WS_API.writeMessage(websocketInstance, "CREATE_MESSAGE", params)


    """
    reply a contact card to user      将联系人回复给用户
    
     {
    "id": "UUID",
    "action": "CREATE_MESSAGE",
    "params": {
        "conversation_id": "UUID",
        "category": "PLAIN_CONTACT",
        "status": "SENT",
        "message_id": "UUID",
        "data": "Base64 encoded data"
    }
 }
 
  {
    "user_id": "UUID"
 }
    """
    @staticmethod                                                               #共享用户ID
    def sendUserContactCard(websocketInstance, in_conversation_id, to_user_id, to_share_userid):
        btnJson = json.dumps({"user_id": to_share_userid})
        print(btnJson)
        btnJson = base64.b64encode(btnJson.encode('utf-8')).decode('utf-8')
        params = {"conversation_id": in_conversation_id, "recipient_id": to_user_id, "message_id": str(uuid.uuid4()),
                  "category": "PLAIN_CONTACT", "data": btnJson}
        print(params)
        return MIXIN_WS_API.writeMessage(websocketInstance, "CREATE_MESSAGE", params)

    """
    reply a text to user    发送文本              .encode('utf-8')
    """
    @staticmethod
    def sendUserText(websocketInstance, in_conversation_id, to_user_id, textContent):
        textContent = str(textContent)
        textContent = textContent.encode('utf-8')
        textContent = base64.b64encode(textContent).decode(encoding='utf-8')
        params = {"conversation_id": in_conversation_id, "recipient_id": to_user_id, "status": "SENT",
                  "message_id": str(uuid.uuid4()), "category": "PLAIN_TEXT",
                  "data": textContent}
        return MIXIN_WS_API.writeMessage(websocketInstance, "CREATE_MESSAGE", params)
    """
    发送图片
    """
    @staticmethod
    def sendUserImg(websocketInstance, in_conversation_id, to_user_id, Content):

        params = {"conversation_id": in_conversation_id, "recipient_id": to_user_id, "status": "SENT",
                  "message_id": str(uuid.uuid4()), "category": "PLAIN_IMAGE",
                  "data": Content}
        return MIXIN_WS_API.writeMessage(websocketInstance, "CREATE_MESSAGE", params)

    """
    send user a pay button   发送支付按钮
    """
    @staticmethod                                   # 会话ID
    def sendUserPayAppButton(webSocketInstance, in_conversation_id, to_user_id, inAssetName, inAssetID, inPayAmount, linkColor="#0CAAF5"):
        payLink = "https://mixin.one/pay?recipient=" + mixin_config.client_id + "&asset=" + inAssetID + "&amount=" + str(
            inPayAmount) + '&trace=' + str(uuid.uuid1()) + '&memo=PRS2CNB'
        btn = '[{"label":"' + inAssetName + '","action":"' + payLink + '","color":"' + linkColor + '"}]'
        btn = base64.b64encode(btn.encode('utf-8')).decode(encoding='utf-8')
        gameEntranceParams = {"conversation_id": in_conversation_id, "recipient_id": to_user_id,
                              "message_id": str(uuid.uuid4()), "category": "APP_BUTTON_GROUP", "data": btn}
        MIXIN_WS_API.writeMessage(webSocketInstance, "CREATE_MESSAGE", gameEntranceParams)

    @staticmethod
    def sendAppCard(websocketInstance, in_conversation_id, to_user_id, asset_id, amount, icon_url, title, description, color="#0080FF", memo=""):
        payLink = "https://mixin.one/pay?recipient=" + to_user_id + "&asset=" + asset_id + "&amount=" + \
                amount + "&trace=" + str(uuid.uuid4()) + "&memo="
        card =  '{"icon_url":"' + icon_url + '","title":"' + title + \
                '","description":"' + description + '","action":"'+ payLink + '"}'
        enCard = base64.b64encode(card.encode('utf-8')).decode(encoding='utf-8')
        params = {"conversation_id": in_conversation_id,  "message_id": str(uuid.uuid4()),
                  "category": "APP_CARD", "status": "SENT", "data": enCard}
        return MIXIN_WS_API.writeMessage(websocketInstance, "CREATE_MESSAGE", params)

    @staticmethod
    def sendAppButtonGroup(websocketInstance, in_conversation_id, to_user_id, buttons):
        buttonsStr = '[' + ','.join(str(btn) for btn in buttons) +']'
        buttonsStr = buttonsStr.replace("'",'"')
        print(buttonsStr)
        enButtons = base64.b64encode(buttonsStr.encode('utf-8')).decode(encoding='utf-8')
        params = {"conversation_id": in_conversation_id,  "recipient_id": to_user_id,
                "message_id": str(uuid.uuid4()),
                "category": "APP_BUTTON_GROUP", "status": "SENT", "data": enButtons}
        return MIXIN_WS_API.writeMessage(websocketInstance, "CREATE_MESSAGE", params)

    @staticmethod
    def packButton(to_user_id, asset_id, amount, label, color="#FF8000", memo=""):
        payLink = "https://mixin.one/pay?recipient=" + to_user_id + "&asset=" + asset_id + "&amount=" + \
                    amount + "&trace=" + str(uuid.uuid4()) + "&memo="
        print(payLink)
        button  = '{"label":"' + label + '","color":"' + color + '","action":"' + payLink + '"}'
        print(button)
        return button