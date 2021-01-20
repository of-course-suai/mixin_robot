
# -*- coding: UTF-8 -*-

import tornado.ioloop
import tornado.web
import requests
import json
from mixin_api import MIXIN_API
import mixin_config
import sqlite3

con = sqlite3.connect("subscribe.db")
cur = con.cursor()


# sql = "CREATE TABLE IF NOT EXISTS shouquan(id INTEGER PRIMARY KEY,full_name TEXT,user_id TEXT)"
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        code = self.get_query_argument("code")
        data = {'client_id':'959f944f-603f-437c-a566-9acc1c0e070e','code':code,'client_secret':'77528561c84bb956df5a50a5e498bb5092e1c496fdc892e8e8dd12869e7a845f'}
        # d = json.dumps(data)
        res = requests.post('https://mixin-api.zeromesh.net/oauth/token',json=data).json()
        print(res)

        acc = res['data']['access_token']
        h = {"Authorization":"Bearer "+acc}
        res = requests.get('https://mixin-api.zeromesh.net/me',headers=h)
        self.write("授权成功，您可以再次点击订阅即可使用小助手每日提醒签到~")
        res = res.json()
        print(res)
        # res = json.dumps(res.json())


        demo = (str(res['data']['full_name']), str(res['data']['user_id']), str(res['data']['phone']), str(res['data']['avatar_url']), str(res['data']['code_url']), str(res['data']['created_at']), str(res['data']['fiat_currency']))
        data = (str(res['data']['full_name']), str(res['data']['user_id']))
        res = cur.execute('select * from shouquan where full_name=? and user_id=?', (data)).fetchall()
        if len(res) == 0:
            cur.execute('INSERT INTO shouquan(full_name,user_id,phone,avatar_url,code_url,created_at,fiat_currency) VALUES (?,?,?,?,?,?,?)', demo)
            con.commit()

        # print(res['data']['full_name'])
        # print(res['data']['user_id'])
        # print(res['data']['phone'])
        # print(res['data']['avatar_url'])
        # print(res['data']['code_url'])
        # print(res['data']['created_at'])
        # print(res['data']['fiat_currency'])



application = tornado.web.Application([
    (r"/auth", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()