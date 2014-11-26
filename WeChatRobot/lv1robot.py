#coding:utf-8
from werobot import WeRoBot
from werobot.reply import TextReply,MusicReply,Article,ArticlesReply
from werobot.client import *
from werobot.messages import WeChatMessage
robot = WeRoBot(token='kefengwei')


@robot.subscribe
def subscribe_me(message):
    reply = ArticlesReply(message=message)
    article = Article(
    title="WeRoBot",
    description="WeRoBot是一个微信机器人框架",
    img="https://github.com/apple-touch-icon-144.png",
    url="https://github.com/whtsky/WeRoBot"
    )
    reply.add_article(article)
    return reply

@robot.unsubscribe
def unsubscribe_me(message):
    print 'One User leave us!'

@robot.text
def hello_world(message):
    content =  message.content
    print message.source
    print message.target
    if content == 'm':
        reply = TextReply(message=message,content="hello!!!")
    else:
        reply = "wrong text"
    return reply

@robot.voice
def hello_voice(message):
    return "You send a voice to me!"

@robot.image
def hello_image(message):
    picurl = message.img
    print picurl
    reply = ArticlesReply(message=message)
    article = Article(
    title="WeRoBot",
    description="WeRoBot是一个微信机器人框架",
    img="https://github.com/apple-touch-icon-144.png",
    url="https://github.com/whtsky/WeRoBot"
    )
    reply.add_article(article)
    return reply

@robot.click
def click_my(message):
    print message.key
    return  "This is a click %s" % message.key

client = Client('wx1c61843daa556523','0798b663ac452fdc9ec8c76d99751a17')
token = client.grant_token()
print token
client.create_menu({
                "button":[
                    {
                        "type":"click",
                        "name":"今日歌曲",
                        "key":"V1001_TODAY_MUSIC"
                    },
                    {
                        "type":"click",
                        "name":"歌手简介",
                        "key":"V1001_TODAY_SINGER"
                    },
                    {
                        "name":"菜单",
                        "sub_button":[
                            {
                                "type":"view",
                                "name":"搜索",
                                "url":"http://testrobot.nat123.net/hello"
                            },
                        ]
                    }
                ]})
print client.get_menu()

robot.run(host='0.0.0.0',port=80)