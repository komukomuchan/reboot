import accessClashRoyaleAPI as cr
import requests
import datetime
import asyncio
from PIL import Image
from io import BytesIO
import os
import json
from discord.ext import commands,tasks
import changeValueName
import numpy as np
import japanize_matplotlib
import trophyRateGraph
import createFolderPath
import datetime
import normalized as nl
import pandas as pd
import discord


#トワストのタグ#P8RG0YGL
#レコブラのタグ#9QL8QC09

def get_channel():
    return "2"

def get_file_name():
    id = get_channel()
    clan_list = load_clanlist_json()
    for clan in clan_list["clan_list"].items():
        if id == clan[0]:
            json_name = clan[1][0]
    return json_name

def get_clantag():
    channel = get_channel()
    clan_list = load_clanlist_json()
    for clan in clan_list["clan_list"].items():
        if channel == clan[0]:
            clan_tag = clan[1][1]
    return clan_tag


def get_clanname():
  return cr.access_api("clans", get_clantag())["name"]


def get_current_rate(player_tag):
  rate = cr.access_api(
      'players', player_tag)["currentPathOfLegendSeasonResult"]["trophies"]
  if rate == 0:
    rate = cr.access_api(
        'players',
        player_tag)["currentPathOfLegendSeasonResult"]["leagueNumber"] * 100
  return rate

def load_clanlist_json():
    file_name = "clan_list.json"

    # 指定されたファイルが存在するか確認
    if os.path.exists(file_name):
        # ファイルが存在する場合は読み込む
        with open(file_name, 'r') as file:
            data = json.load(file)
    else:
        # ファイルが存在しない場合は新しく作成する
        data = {
            "clan_list":{
                "1":["twilight.json","#P8RG0YGL"],
                "2":["reko.json","#9QL8QC09"]
            }
        }

        with open(file_name, 'w') as file:
            json.dump(data, file, indent=2)
    
    return data


def load_json():
    file_name = get_file_name()

    # 指定されたファイルが存在するか確認
    if os.path.exists(file_name):
        # ファイルが存在する場合は読み込む
        with open(file_name, 'r') as file:
            data = json.load(file)
    else:
        # ファイルが存在しない場合は新しく作成する
        data = {
            "river_race_check":False,
            "member_list": {
                "members": [],
                "len": 0
            },
            "in_out": {
                "out_list": [],
                "len": 0
            },
            "exp_list": []
        }

        with open(file_name, 'w') as file:
            json.dump(data, file, indent=2)
    
    return data

def write_json(data):
    # JSONファイルの書き込み
    with open(get_file_name(), 'w') as file:
        json.dump(data, file, indent=2,ensure_ascii=False)



class CustomBotException(Exception):
    def __init__(self, message="カスタムボット例外が発生しました"):
        self.message = message
        super().__init__(self.message)



TOKEN = 'MTEyMjkxMjU5MjkyNzY2MjI2Mg.GCr9jT._hFc6WLykSK4fvGLYjzSFnpVL8ydwOJpx6TVGo'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents,case_insensitive=True)

@bot.command()
async def change_name_tag(ctx,player_name):
    player_tag = player_name
    if not player_name.startswith('#'):
        data = load_json()
        player_name = player_name.lower()
        player_name_tag_list = [[player["player_name"],player["player_tag"]] for player in data["member_list"]["members"]]

        #player_name_tag[0]が名前で[1]がタグ
        try:
            for player_name_tag in player_name_tag_list:
                if player_name in player_name_tag[0].lower():
                    player_tag = player_name_tag[1]
                    break
            else:
                raise CustomBotException("該当者が見つかりませんでした")
        except CustomBotException as e:
            # カスタム例外をキャッチして処理
            await ctx.channel.send("該当者が見つかりませんでした")
    
    return player_tag


async def send_message_at_specific_time():
    target_time = datetime.time(14, 24)  # 13:30を指定
    while True:
        data = load_json()
        river_race_check = data["river_race_check"]
        now = datetime.datetime.now()
        if now.time().hour == target_time.hour and now.time().minute == target_time.minute and now.weekday() in [4, 5, 6, 0] and river_race_check:
            channel = bot.get_channel(1122913404051538144)  # メッセージを送信したいチャンネルのIDを指定
            await channel.send(await riverCheck("yes"))
        await asyncio.sleep(60)  # 1分ごとに確認

@bot.event
async def on_ready():
    print('Startup Success!!!')
    bot.loop.create_task(send_message_at_specific_time())
    test_command.start()



@tasks.loop(hours=1)
async def test_command():
    # ここに1時間ごとに実行したいコマンドを実装
    clan_members = cr.access_api('clans',get_clantag())["memberList"]
    data = load_json()
    current_clan_list,out_data = [],[]

    #在籍リストと、現在クラン内にいる人のタグをリストにする
    clan_list = [tag["player_tag"] for tag in data["member_list"]["members"]]

    current_clan_list = [tag["tag"] for tag in clan_members]

    #在籍リストにいるがクラロワ内にいない人
    go_out = [item for item in clan_list if item not in current_clan_list]

    out_data = [tag["player_tag"] for tag in data["in_out"]["out_list"]]


    new_out = [value for value in go_out if value not in out_data]
    come_back = [value for value in out_data if value not in go_out]


    #データベースに登録されていない外出者new_outを外出リスト(out_listテーブル)に登録、また、帰ってきた人を外出リストから外す。
    # 現在の日付を取得
    today = datetime.date.today()

    #MM-DD 形式の文字列にフォーマット
    formatted_date = today.strftime("%m/%d")

    for member in new_out:
        data["in_out"]["out_list"].append({

                                            "player_tag":member,
                                            "date":formatted_date,
                                            "memo":""
                                            })
        
    data["in_out"]["out_list"] = [out for out in data["in_out"]["out_list"] if out["player_tag"] not in come_back]
    data["in_out"]["len"] = len(data["in_out"]["out_list"])

    write_json(data)


@bot.command()
async def out(ctx):
    await test_command()
    data = load_json()
    clan_members = cr.access_api('clans',get_clantag())["memberList"]
    member_list,clan_members_tag_list = [],[]
    await ctx.channel.send("現在の外出者の一覧です")

    clan_members_tag_list = [member["tag"] for member in clan_members]
    out_list = [member for member in data["in_out"]["out_list"]]

    await ctx.channel.send("外出")
    for member in out_list:
        await ctx.channel.send(cr.access_api('players',member["player_tag"])["name"]+"  "+member["date"]+"  "+member["memo"])


    member_list = [member["player_tag"] for member in data["member_list"]["members"]]

    enjoy_list = [item for item in clan_members_tag_list if item not in member_list]

    await ctx.channel.send("遊び")
    for member in enjoy_list:
        await ctx.channel.send(cr.access_api('players', member)["name"])

    out_len = len(out_list)
    clan_members_len = len(clan_members_tag_list)
    await ctx.channel.send("外出人数:" + str(out_len) + "人")
    await ctx.channel.send("現在クラン内にいる人数:" + str(clan_members_len) + "人")
    await ctx.channel.send("計" + str(out_len + clan_members_len) + "人")

@bot.command()
async def outMemo(ctx,player_name,memo=""):
    player_tag = await change_name_tag(ctx,player_name)
    data = load_json()

    for out_data in data["in_out"]["out_list"]:
        if out_data["player_tag"] == player_tag:
            out_data["memo"] = memo
            break
    else:
        await ctx.channel.send("該当者が見つかりませんでした")

    write_json(data)

    await out(ctx)


@bot.command()
async def changeDate(ctx,player_name,date):
    player_tag = await change_name_tag(ctx,player_name)
    data = load_json()

    for out_data in data["in_out"]["out_list"]:
        if out_data["player_tag"] == player_tag:
            out_data["date"] = date

    write_json(data)

    await ctx.channel.send("日付を変更しました")
    await out(ctx)


@bot.command()
async def tag(ctx,*player_name):
    player_tag_list = [await change_name_tag(ctx,name) for name in player_name]
    data = load_json()
    for member in data["member_list"]["members"]:
        if member["player_tag"] in player_tag_list:
            await ctx.channel.send(member["player_name"]+"のプレイヤータグ")
            await ctx.channel.send(member["player_tag"])



@bot.command()
async def addMem(ctx,*args):

    # 文字列が "#" で始まる要素だけを新しいリストに抽出
    add_member =  set(item for item in list(args) if item.startswith("#"))
    add_id = [item for item in list(args) if not item.startswith("#")]

    #該当しないプレイヤーを弾く
    for member in add_member:
       if isinstance(cr.access_api('players', member), requests.exceptions.HTTPError):
            await ctx.channel.send("存在しないプレイヤーIDです")
            await ctx.channel.send("該当プレイヤー:"+member)
            return
    data = load_json()


    #既にデータに入っている場合は弾く
    member_tag = set(tag["player_tag"] for tag in data["member_list"]["members"])
    check_add_member = add_member - member_tag
    bound_data = add_member - check_add_member
    check = True
    if bound_data:
        await ctx.channel.send("下記のデータは既に存在しています")
        for data in bound_data:
            await ctx.channel.send(data)


    # データ挿入
    for member,number in zip(check_add_member,add_id):
        data["member_list"]["members"].append({
                                    "player_name":cr.access_api('players',member)['name'],
                                    "player_tag":member,
                                    "discord_id":number,
                                    "role":"メンバー"
                                    })
        check = False
    if check:
        await ctx.channel.send("データが追加されませんでした。")
        return
    data["member_list"]["len"] = len(data["member_list"]["members"])

    write_json(data)
    await ctx.channel.send("追加されました")


@bot.command()
async def show(ctx):
    await ctx.channel.send(get_clanname()+"のメンバー")
    data = load_json()
    for member in data["member_list"]["members"]:
        await ctx.channel.send(member["player_name"]+"  "+member["role"])
        await ctx.channel.send((member["player_tag"]))

@bot.command()
async def showMem(ctx,player_name):
    player_tag = await change_name_tag(ctx,player_name)
    data = load_json()

    for member in data["member_list"]["members"]:
        if member["player_tag"] == player_tag:
            await ctx.channel.send(member["player_name"]+"  "+member["role"])
            await ctx.channel.send((member["player_tag"]))
            break
    else:
        await ctx.channel.send("プレイヤー名"+player_name+"はクランリストに存在しません")



@bot.command()
async def delMem(ctx,*args):
    data = load_json()
    #削除したい対象のタグの集合を作成
    delete_tags = set(args)

    for member in data["member_list"]["members"]:
        #在籍リストにいる人が削除対象に入っていた場合
        if member["player_tag"] in delete_tags:
            await ctx.channel.send(member["player_name"]+"→削除")

    #削除後のデータ
    new_data = [member for member in data["member_list"]["members"] if member["player_tag"] not in delete_tags]
        
    # 既存のデータと新しいデータの差分を表示

    data["member_list"]["members"] = new_data

    data["member_list"]["len"] = len(data["member_list"]["members"])

    # 更新後のデータを保存する
    write_json(data)



@bot.command()
async def updMem(ctx,*args):
    if len(args) != 2:
        await ctx.channel.send("プレイヤータグと役職の2つが必要です")
        return
    data = load_json()
    player_tag,role = args

    for member in data["member_list"]["members"]:
        await ctx.channel.send(member["player_tag"])
        if member["player_tag"] == player_tag:
            member["role"] = role
            break
    else:
        await ctx.channel.send("該当のプレイヤーが存在しなかったため、役職を更新できませんでした")

    write_json(data)


@bot.command()
async def role(ctx):
    await ctx.channel.send("現在役職が違うクランメンバーです")
    #現在クランにいるクラメンのリスト
    clan_member = cr.access_api("clans",get_clantag())["memberList"]

    data = load_json()
    tag_role_list = [[member["player_tag"],member["role"]] for member in data["member_list"]["members"]]

    #役割を変換するための辞書
    role_list = {
        "メンバー":"member",
        "長老": "elder",
        "サブリーダー": "coLeader",
        "リーダー": "leader",
        "member": "メンバー",
        "elder": "長老",
        "coLeader": "サブリーダー",
        "leader": "リーダー"
    }

    # 役割を変換した新しいリストを生成
    updated_roles = [(player_tag, role_list.get(role, role)) for player_tag, role in tag_role_list]

    for member in clan_member:
        #プレイヤー1人につき、在籍リストを一つ一つ参照しプレイヤータグが一致する場合は役職を確認
        for row in updated_roles:
           if member["tag"] == row[0] and member["role"] != row[1]:
               await ctx.channel.send(member["name"]+" "+"誤:"+role_list[member["role"]]+" "+"正:"+role_list[row[1]])


@bot.command()
async def river(ctx,mension="no"):
    await ctx.channel.send(riverCheck(mension))


@bot.command()
async def riverCheck(mension="no"):
    mension = mension.lower() == "yes"
    message = ""
    #クラン戦免除リストのタグを取得
    data = load_json()
    exp_list = data["exp_list"]

    #在籍リストからプレイヤータグとそれに紐ずくDiscordIDを取得
    mension_list = [[member["player_tag"],member["discord_id"]] for member in data["member_list"]["members"]]

    
    #クラン対戦未消化者が在籍リストに入っているか確認するために在籍リストからプレイヤータグを取得
    list_tag = [item[0] for item in mension_list]


    data = cr.access_current_riverrace(get_clantag())
    clan_member_tag_list = [i["tag"] for i in cr.access_api("clans",get_clantag())["memberList"]]
    war_miss_in,war_miss_out = [],[]


    for member in data["clan"]["participants"]:
        if member["decksUsedToday"] < 4 and member["tag"] not in exp_list and member["tag"] in list_tag:
            if member["tag"] in clan_member_tag_list:
                war_miss_in.append(member)
            else:
                war_miss_out.append(member)
    
    if war_miss_in != []:
        message += "-----クラン内にいて4戦消化していない人-----\n"
        for member in war_miss_in:
            for tag in mension_list:
                if tag[0] == member["tag"]:
                    mension_id = tag[1]
                    break
            message += f"<@{mension_id}>:残り{str(4-member['decksUsedToday'])}デッキ\n" if mension else f"{member['name']}さん:残り{str(4-member['decksUsedToday'])}デッキ\n"

    if war_miss_out != []:
        message += "-----外出中で4戦消化していない人-----\n"
        for member in war_miss_out:
            for tag in mension_list:
                if tag[0] == member["tag"]:
                    mension_id = tag[1]
                    break
            if mension:
                message += f"<@{mension_id}>:残り{str(4-member['decksUsedToday'])}デッキ\n"
            else:
                message += f"{member['name']}さん:残り{str(4-member['decksUsedToday'])}デッキ\n"


    if message == "":
        message += "現在4戦消化していないメンバーはいません"
    else:
        message = "現在4戦消化していない人のメンバ一覧です\n"+message
    return message



@bot.command()
async def showExp(ctx):
    data = load_json()
    await ctx.channel.send("クラン戦免除一覧")
    for member in data["exp_list"]:
        await ctx.channel.send(cr.access_api("players",member)["name"])

@bot.command()
async def addExp(ctx,*player_name):
    data = load_json()
    for name in player_name:
        tag = await change_name_tag(ctx,name)
        if tag not in data["exp_list"]:
            data["exp_list"].append(tag)
    write_json(data)
    await ctx.channel.send("追加されました")

    await showExp(ctx)


@bot.command()
async def delExp(ctx,*player_name):
    data = load_json()
    for name in player_name:
        tag = await change_name_tag(ctx,name)
        data["exp_list"].remove(tag)
    write_json(data)
    await ctx.channel.send("削除しました")
    await showExp(ctx)

@bot.command()
async def showID(ctx, player_name):
    data = load_json()
    player_tag = await change_name_tag(ctx,player_name)
    for player in data["member_list"]["members"]:
        if player["player_tag"] == player_tag:
            await ctx.channel.send(player["player_name"] + "のDiscordIDは" +str(player["discord_id"]))
            break
    else:
        await ctx.channel.send("該当プレイヤーが見つかりません")






@bot.command()
async def clan_csv(ctx):

    # 現在の日付を取得
    current_date = datetime.date.today()

    # 先月を計算
    first_day_of_current_month = current_date.replace(day=1)
    last_day_of_last_month = first_day_of_current_month - datetime.timedelta(days=1)
    first_day_of_last_month = last_day_of_last_month.replace(day=1)

    # 先月の日付を"YYYY-MM"形式にフォーマット
    formatted_date = first_day_of_last_month.strftime("%Y-%m")


    #クラメンの人数
    clan_name = get_clanname()
    clan_member,member_name,role,trophies,legacy_trophies,last_rate,last_ranking,best_rate,best_ranking = [],[],[],[],[],[],[],[],[]

    #在籍リストからタグを取得
    data = load_json()
    clan_member = [tag["player_tag"] for tag in data["member_list"]["members"]]
    

    for i in clan_member:
        player_data = cr.access_api("players",i)

        #値の挿入
        member_name.append(player_data["name"])
        if "role" in player_data:
            role.append(player_data["role"])
        else:
            role.append("member")

        trophies.append(player_data["trophies"])

        #伝説の道が開放されているという条件
        if player_data["bestPathOfLegendSeasonResult"] != None:
            best_rate.append(player_data["bestPathOfLegendSeasonResult"]["trophies"])

            #天界に到達していない場合はリーグを取得
            if player_data["lastPathOfLegendSeasonResult"]["trophies"] == 0:
                last_rate.append(player_data["lastPathOfLegendSeasonResult"]["leagueNumber"])
            else:
                last_rate.append(player_data["lastPathOfLegendSeasonResult"]["trophies"])


        #値が空欄の箇所に0を代入
        legacy_trophies.append(nl.change_none_to_zero(player_data["legacyTrophyRoadHighScore"]))
        last_ranking.append(nl.change_none_to_zero(player_data["lastPathOfLegendSeasonResult"]["rank"]))
        best_ranking.append(nl.change_none_to_zero(player_data["bestPathOfLegendSeasonResult"]["rank"]))



        

    trophy_csv_data = {

        "クラロワ名" : member_name,
        "役職": role,
        "トロフィー" : trophies,
        "往年の輝き" : legacy_trophies

    }

    rate_csv_data = {

        "クラロワ名" : member_name,
        "レート" : last_rate,
        "順位" : last_ranking,
        "ベストレート" : best_rate,
        "ベスト順位" : best_ranking

    }

    #pandasを用いてcsvに
    df1 = pd.DataFrame(trophy_csv_data)
    df2 = pd.DataFrame(rate_csv_data)

    #間の空欄
    df1[""] = ""

    #トロフィー順とレート順のcsvを合成
    merged_df1 = pd.concat([df1, df2], axis=1)
    #不要な列の削除
    merged_df1 = merged_df1.drop("",axis=1)
    #重複する列の削除
    merged_df1 = merged_df1.loc[:, ~merged_df1.columns.duplicated()]

    # 降順で並び替え
    df1_sorted = df1.sort_values(by='トロフィー', ascending=False)
    df2_sorted = df2.sort_values(by='レート', ascending=False)
    merged_df1 = merged_df1.sort_values(by='レート', ascending=False)

    # インデックスを振り直す
    df1_sorted = df1_sorted.reset_index(drop=True)
    df2_sorted = df2_sorted.reset_index(drop=True)
    merged_df1 = merged_df1.reset_index(drop=True)
    #1列目をスタートに
    merged_df1.index = merged_df1.index + 1

    #役職名を日本語に
    role_name = {"member":"メンバー","elder":"長老","coLeader":"サブリーダー","leader":"リーダー"}
    changeValueName.translate_value(df1_sorted,'役職',role_name)
    changeValueName.translate_value(merged_df1,'役職',role_name)

    #天界未到達の人のレートを日本語に変換
    rate_name = {1:"銅剣",2:"銀剣",3:"金剣",4:"的",5:"ハンマー",6:"青瓶",7:"プリ冠",8:"赤冠",9:"青冠"}
    changeValueName.translate_value(df2_sorted,'レート',rate_name)
    changeValueName.translate_value(merged_df1,'レート',rate_name)

    #出力先を格納するフォルダの作成
    folder_path = "../"+clan_name+"シーズン結果/"+formatted_date
    createFolderPath.create_folder(folder_path)

    #csvとして出力
    df2_sorted.to_csv(folder_path+"/"+clan_name+"レートリスト.csv")


@bot.command()
async def setting(ctx):
    data = load_json()
    data["river_race_check"] = not data["river_race_check"]
    write_json(data)
    if data["river_race_check"]:
        await ctx.channel.send("クラン戦管理をONにしました")
    else:
        await ctx.channel.send("クラン戦管理をOFFにしました")



bot.run(TOKEN)
