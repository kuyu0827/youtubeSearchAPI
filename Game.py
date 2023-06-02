# coding:utf-8

#==========================
# インポートモジュール
#==========================
import urllib.request

#==========================
# 処理
#==========================


def gameTitle(videoId):
    url = 'https://www.youtube.com/watch?v=' + videoId
    content = urllib.request.urlopen(url).read().decode('utf-8')

    prefix = '}]},"title":{"simpleText":"'
    if prefix in content:
        gameName = content.split(prefix)[1].split('"')[0]
    else:
        gameName = "不明"
    return gameName

