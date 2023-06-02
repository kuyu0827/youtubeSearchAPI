# Youtubeから引っ張るもの

# coding:utf-8

# ==========================
# インポートモジュール
# ==========================
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys

# ==========================
# グローバル変数
# ==========================
args = sys.argv  # CLI引数格納
API_KEY = ''
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
)

# ==========================
# 関数
# ==========================

# [チャンネル名]を検索 → [チャンネル名とチャンネルID]を配列で返す
def searchChannels(_keyword, max=25):
    search_response = youtube.search().list(
        q=_keyword, part='id,snippet', maxResults=max).execute()
    channels = []
    length = 0
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#channel":
            length += 1
            channels.append([search_result["snippet"]["title"],
                            search_result["id"]["channelId"], [str(length)+"番目"]])
    return channels

# チャンネルIDから紐づくビデオIDを取得する[detail=TrueでIDのすべての情報を返す]
def getVideoInfo(_channelid, max=50, detail=False):
    searches = []
    search_response = youtube.search().list(
      part="snippet",
      channelId=_channelid,
      maxResults=max,
      order="date",
    ).execute()

    for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        if detail:
          searches.append(search_result)
        else:
          searches.append(search_result["id"]["videoId"])
    return searches
