
# coding:utf-8

# ==========================
# インポートモジュール
# ==========================
import pandas
import pprint
import collections
from re import split
from Game import gameTitle
from wikipedia_search import wikipedia_search
from ytdata import searchChannels, getVideoInfo
from typing import List

#==========================
# 関数
#==========================

# チャンネル名検索
def input_channel():
    channel_name = input("検索するチャンネル名を入力してください : ")
    ytlist = searchChannels(channel_name, 50)  # リストで検索されたものを表示
    
    # チャンネルが見つからないときの処理
    if(len(ytlist) == 0):
        print("チャンネルが見つかりませんでした。")
        return input_channel()
    # 候補チャンネルが2つ以上の場合は選択させる
    elif(len(ytlist) > 1):
        flag = True
        while flag:
            pprint.pprint(ytlist)
            print("\n該当チャンネルが" + str(len(ytlist)) + "件見つかりました")
            channel_getIDindex = input("何件目を取得しますか? : ")
            if(0 < int(channel_getIDindex) and int(channel_getIDindex) <= len(ytlist)):
              ytlist = ytlist[int(channel_getIDindex) - 1]
              flag = False
            else:
                print("1~" + str(len(ytlist)) + "の間の件数を入力してください")
    return ytlist

#1つのリストから複数のリスト
def onelistToList(listVer):
    stringVer= ', '.join(map(str, listVer))
    stringVer = stringVer.replace("[","")       #[削除
    stringVer = stringVer.replace("]","")       #]削除
    stringVer = stringVer.replace(" ","")       #空白削除
    stringVer = stringVer.replace("'","")       #アポストロフィ削除
    listVer = stringVer.split(',')
    return listVer

#ゲームリスト整理
def gameListtoList(gameList):
    #ゲームリストの整理
    gameList = collections.Counter(gameList)
    gameList = gameList.most_common()
    return gameList

#ゲームの選択
def gameListtogameSelect(gameList):
    print()
    if(len(gameList) == 1):
        print("ゲームタイトルが" + gameList[0][0] + "の1件のみ取得されたので、自動的に選択されました")
        return 0
    flag = True
    while flag:
        gameSelectNum = input("ゲームタイトルを[1~" + str(len(gameList)) +"]の中から選択してください : ")
        if(int(gameSelectNum) > len(gameList) or int(gameSelectNum) < 1):
            print("正しい値が入力されませんでした。もう一度選択してください")
            print("入力された値 : [" + gameSelectNum + "]")
        else:
            print(gameList[int(gameSelectNum) - 1][0] +"が選択されました")
            flag = False
    
    return (int(gameSelectNum)-1)


#==========================
# 処理
#==========================

#1つのチャンネルの取得
serachChannel = input_channel()

#チャンネルのデータの分割
channelList = onelistToList(serachChannel)

#動画データの取得(25件)
videoList = getVideoInfo(channelList[1],25,False)

#デバッグ用
#pandas.to_pickle(videoList, "videoList.pkl")
#videoList = pandas.read_pickle("videoList.pkl")

gameList = []
#動画データからゲームリストの作成
for i in range(len(videoList)):
    gameName = gameTitle(videoList[i])
    #print(gameName)
    if(gameName != "不明"):
        gameList.append(gameName)

#ゲームリストの整理
gameList = gameListtoList(gameList)

#ゲームリストの出力
print()
if(len(gameList) == 0):
    print("ゲームタイトルが見つかりませんでした")
    exit()
print(str(len(gameList)) + "個のゲームタイトルを発見しました")
for i in range(len(gameList)):
    print( "[" + str((i) + 1) +"] " + "ゲームタイトル : " + gameList[i][0] + ", " + str(gameList[i][1]) + "件の動画" )


#ゲームリストを検索
selectGameNum =  gameListtogameSelect(gameList)

#ゲームをwikipediaで検索
wikipedia_search(gameList[selectGameNum][0])

exit()
