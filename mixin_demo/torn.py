
# -*- coding: UTF-8 -*-

import tornado.ioloop
import tornado.web
import requests
import json
from mixin_api import MIXIN_API
import mixin_config

# 这步具体参考官方开发者文档，我这里是用tornado get方法写的，你也可以用其它方法来写，这里我就不详细阐述了，因为已经写的很清楚了
# 不会有人给了源码都不会用吧，不会吧不会吧~【doge】   相关参数可以去看开发者文档，对照我的tornado源码就很容易看懂，就是常规的请求返回参数操作
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        code = self.get_query_argument("code")
        data = {'client_id':'这个东西你的机器人json有','code':code,'client_secret':'这个也是'}
        res = requests.post('https://mixin-api.zeromesh.net/oauth/token',json=data).json()

        acc = res['data']['access_token']   # access_token  
        h = {"Authorization":"Bearer "+acc}
        res = requests.get('https://mixin-api.zeromesh.net/me',headers=h)
        self.write("授权成功，你可以再次点击订阅即可使用卢本伟每日提醒斗地主")
        res = res.json()
        print(res)
# 授权之后别忘记了把授权的信息存起来
'''创建一个shouquan表'''

application = tornado.web.Application([
    (r"/auth", MainHandler),
])

if __name__ == "__main__":
    application.listen(6666)
    tornado.ioloop.IOLoop.instance().start()
