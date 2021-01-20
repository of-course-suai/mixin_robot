
# -*- coding: UTF-8 -*-

import tornado.ioloop
import tornado.web
import requests
import json
from mixin_api import MIXIN_API
import mixin_config

# 这步具体参考官方开发者文档，我这里是用tornado写的，你也可以用其它方法来写，这里我就不详细阐述了
# 不会有人给了源码都不会用吧，不会吧不会吧~【doge】
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        code = self.get_query_argument("code")
        data = {'client_id':'？','code':code,'client_secret':'？'}
        res = requests.post('这是你机器人的验证地址',json=data).json()

        acc = res['data']['access_token']
        h = {"Authorization":"Bearer "+acc}
        res = requests.get('https://mixin-api.zeromesh.net/me',headers=h)
        self.write("授权成功，你可以再次点击订阅即可使用卢本伟每日提醒斗地主")
        res = res.json()
        print(res)


application = tornado.web.Application([
    (r"/auth", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
