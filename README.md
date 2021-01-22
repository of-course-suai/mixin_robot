# mixin_robot

本文主要基于mixin实现-如何创建机器人，如何让机器人回复用户，如何让用户授权，如何让机器人按时发消息等等

参考来源：

 官方开发者文档：
 
 https://developers.mixin.one/document/bot/get-started/websocket
 
 GitHub开源项目：
 
 https://github.com/wenewzhang/mixin_labs-python-bot
 
 简书教程：
 
 https://www.jianshu.com/p/522e880a4233?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation
 
 
实现环境：

 python3.6
 
 sqlite3 数据库 用于存取userID 和会话ID   在使用之前记得先创建数据库
 
源码目录：

 mixin_config.py (配置机器人参数,在配置机器人之前你得先去mixin开发者后台申请机器人,详情可以参考我上边给的简书教程.)
 
      (注：机器人申请有一个域名白名单（这里解释一下，域名白名单用于防止伪造机器人链接，打开卡片跟按钮类型的消息时会校验链接的域名是否在白名单中，对于 APP_CARD 或者 APP_BUTTON_GROUP, 需要保证 action 在白名单中。）还有验证网址一定要写好,你可以写你的服务器的IP上去,因为这里在用户授权的时候需要用到!用于OAuth 授权回调)
                 
 mixin_api.py (写的是一些常规方法,具体可以看我的源码)
 
 mixin_ws_api.py (这里就是重头戏了,这个文件写的是机器人调用的方法,这里我完全按着GitHub开源老哥的来,但是我加了一些自己的东西)
 
 ws_test.py (运行项目~)
 
 
实现思路：

这里涉及太多东西，我就挑一些比较重要的来说。

 1，如何让机器人回复用户
 
  我这里主要的方式是让用户发信息，我们获取用户发过来的关键字，实现回复，但是关键字是定死的，比如：
  
  当用户发送你好这两个关键字的时候我们就会发送下列文字
  
  
    if '你好' == realData: 
     introductionContent = '欢迎使用卢本伟智能小助手~' 
     MIXIN_WS_API.sendUserText(ws, conversationId, userId, introductionContent)
     btns = [{"label":"订阅","action":"input:订阅","color":"#0084ff"},{"label":"取消订阅","action":"input:取消订阅","color":"#FF8000"}]  #按钮方法
     MIXIN_WS_API.sendAppButtonGroup(ws, conversationId, userId, btns)
    return
    
    
    
  这里还有一个按钮方法，具体可以查看我的mixin_ws_api.py源码   
  
 2,如何实现定时发送消息功能
 
  这里就变成了如何主动给用户发信息的问题了，首先我们要知道要给用户发消息需要些什么，根据官方的开发者文档，在我们给机器人发送消息的时候后台会返回 会话ID和用户ID，我们只需要把用户ID和会话ID存起来在定时发送消息的时候读取在发送就好了，比如：
  
  
    now_hour = time.strftime("%H", time.localtime()) #获取时间  比如：08：00  这步获取的是 08
    now_min = time.strftime("%M", time.localtime())  # 这步获取的是 00
    con = sqlite3.connect("subscribe.db")  #这里我用的是python自带的sqlite3数据库
    cur = con.cursor()
    if now_hour=='08' and now_min=='00':
      userids = cur.execute("select user_id,conversation_id from test where flag=0").fetchall()
      for u in userids:
          a = '斗地主时间到~'
          MIXIN_WS_API.sendUserText(ws, u[1], u[0], a)
      time.sleep(60)
    time.sleep(1)
  
