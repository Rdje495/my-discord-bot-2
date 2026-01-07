import discord
from discord.ext import commands
from discord import app_commands
import json
import random
from easy_pil import *
import requests
import math
import zipfile
import os
import asyncio
from discord.ext import tasks
from discord import Webhook
import asyncio
import aiohttp
from flask import Flask
from threading import Thread
import os
from dotenv import load_dotenv

class MyBot(commands.Bot):
    async def setup_hook(self):
	    await self.tree.sync()

intents = discord.Intents.all()
intents.message_content = True
client = MyBot(intents=intents,command_prefix="$")
presence = discord.Game("Discord")
CLIENT_ID = 1288137746732417105
API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOiIxMzE1MjM2OTg1NjIyODkwMDU4IiwiaWF0IjoxNzMzNjQ3MzMzfQ.KM3Aqk8E_H2A9FMJdeVsCqMgGRnOQXVDf2rrKXIx2lQ"
"https://discord.com/oauth2/authorize?client_id=1288137746732417105&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%2Fcallback&scope=identify+connections+guilds.join"
"Vb3DMrMJXHzuWF22YEMhjoGkwZvSZ5"
channel = None
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
#以下Flask系
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Renderは環境変数 PORT を指定してくるため、それに合わせる
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Flaskを別スレッドで動かす関数
def keep_alive():
    t = Thread(target=run)
    t.start()

@client.event
async def on_ready():
    print("Startup Completed!")
    await client.tree.sync()
    allowed_mentions = discord.AllowedMentions(replied_user=False)
    client.allowed_mentions = allowed_mentions
    file = zipfile.ZipFile(f'backup_server_data/1216303889599565875.zip', 'w', zipfile.ZIP_DEFLATED)
    file.write(f"backup_server_data/1216303889599565875.json")
    file.close()
    maple = await client.fetch_user(1140293401489707148)
    await maple.send(file=discord.File(f"backup_server_data/1216303889599565875.zip"))
    os.remove(f"backup_server_data/1216303889599565875.zip")
    backupa.start()

@tasks.loop(hours=24)
async def backupa():
    await backup_(1216303889599565875)
    channel = await client.fetch_channel(1417861889677070376)
    file = zipfile.ZipFile(f'backup_server_data/1216303889599565875.zip', 'w', zipfile.ZIP_DEFLATED)
    file.write(f"backup_server_data/1216303889599565875.json")
    file.close()
    file2 = zipfile.ZipFile(f'backup_server_data/1441743289798758513.zip', 'w', zipfile.ZIP_DEFLATED)
    file2.write(f"backup_server_data/1441743289798758513.json")
    file2.close()
    await channel.send(file=discord.File(f"backup_server_data/1216303889599565875.zip"))
    await channel.send(file=discord.File(f"backup_server_data/1441743289798758513.zip"))

async def get_role_deta(guild_id):
    with open(f"server_datas/{str(guild_id)}.json","r") as f:
        role = json.load(f)
    role = role["verify_role"]
    return role

async def get_channels_data():
    try:
        with open("chdata.json", mode='x') as f:
            f.write("{}")
    except FileExistsError:
        pass
    with open("chdata.json",mode = "r") as f:
        users = json.load(f)
    return users



"""
class ButtonVerify(discord.ui.View):
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="認証",style=discord.ButtonStyle.green,custom_id="verifybutton")
    async def verify(self, interaction:discord.Interaction, button:discord.ui.Button) -> None:
        roles = await get_role_deta(interaction.guild.id)
        role = interaction.guild.get_role(int(roles[str(interaction.guild_id)]))
        if role in interaction.author.roles:
            await interaction.reply("すでに認証されています",ephemeral=True)
        await interaction.author.add_roles(role)
        await interaction.reply(f"認証しました\nサーバールールを守り、{interaction.guild.name}をお楽しみください",ephemeral=True)

class Math(discord.ui.Modal,title="計算認証"):
    def __init__(self, timeout=None) -> None:
        one=random.randint(1, 30)
        two=random.randint(1, 30)
        ans=one+two
        global answer
        answer=ans
        super().__init__(timeout=timeout)
        self.answer = discord.ui.TextInput(label="計算問題", placeholder=f'{one} + {two} = ??', style=discord.TextStyle.short,required=True)
        self.add_item(self.answer)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if int(self.answer.value)==answer: #計算結果が正しい
            roles = await get_role_deta()
            role = interaction.guild.get_role(int(roles[str(interaction.guild_id)]))
            await interaction.author.add_roles(role)
            await interaction.reply(f"認証しました\nサーバールールを守り、{interaction.guild.name}をお楽しみください", ephemeral=True)
        else: #計算結果が正しくない
           await interaction.reply('計算が間違っています',ephemeral=True)


class Verify_math(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='認証', style=discord.ButtonStyle.green, custom_id='verify_math')
    async def math_verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        roles = await get_role_deta()
        role = interaction.guild.get_role(int(roles[str(interaction.guild_id)]))
        if role in interaction.author.roles:
            await interaction.reply("すでに認証されています",ephemeral=True)
        modal=Math()
        await interaction.response.send_modal(modal)
"""

async def open_whitelist():
    with open("bot_whitelist.json","r") as f:
        return json.load(f)

async def permission_check(author,level):
    with open("bot_whitelist.json","r") as f:
        whlist = json.load(f)
    try:
        return whlist[str(author)] >= level
    except:
        return False


async def create_user_data(user,guild_id):
    try:
        with open(f"server_datas/{str(guild_id)}.json", mode='x') as f:
            f.write("{}")
    except FileExistsError:
        pass

    with open(f"server_datas/{str(guild_id)}.json",mode = "r") as f:
        ##f.write("{}")
        users = json.load(f)
    
    if "level_role_name_template" not in users:
        users["level_role_name_template"] = "{} role"
        users["autocreate"] = False
        with open(f"server_datas/{str(guild_id)}.json",mode = "w") as f:
        ##f.write("{}")
            json.dump(users,f)

    if "ignore_message_channel" not in users:
        users["ignore_message_channel"] = []
        with open(f"server_datas/{str(guild_id)}.json",mode = "w") as f:
        ##f.write("{}")
            json.dump(users,f)

    if "ignore_channel" not in users:
        users["ignore_channel"] = []
        with open(f"server_datas/{str(guild_id)}.json",mode = "w") as f:
        ##f.write("{}")
            json.dump(users,f)

    if "getexp_chance" not in users:
        users["getexp_chance"] = 5
        with open(f"server_datas/{str(guild_id)}.json",mode = "w") as f:
        ##f.write("{}")
            json.dump(users,f)

    if "getexp_frommessage" not in users:
        users["getexp_frommessage"] = 100
        with open(f"server_datas/{str(guild_id)}.json",mode = "w") as f:
        ##f.write("{}")
            json.dump(users,f)
    
    if "getexp_distance" not in users:
        users["getexp_distance"] = 5
        with open(f"server_datas/{str(guild_id)}.json",mode = "w") as f:
        ##f.write("{}")
            json.dump(users,f)
    
    if str(user) not in users:
        users[str(user)] = {}
        users[str(user)]["exp"] = 0
        users[str(user)]["level"] = 0
        users[str(user)]["nextlevel"] = 1
        with open(f"server_datas/{str(guild_id)}.json",mode = "w") as f:
        ##f.write("{}")
            json.dump(users,f)

    if "getexp_distance" not in users[str(user)]:
        users[str(user)]["getexp_distance"] = 5
        with open(f"server_datas/{str(guild_id)}.json",mode = "w") as f:
        ##f.write("{}")
            json.dump(users,f)
    
    with open(f"server_datas/{str(guild_id)}.json",mode = "r") as f:
        ##f.write("{}")
        users = json.load(f)
    return users

async def get_server_data(guild_id):
    with open(f"server_datas/{str(guild_id)}.json",mode = "r") as f:
        ##f.write("{}")
        users = json.load(f)

    if "level_role_name_template" not in users:
        users["level_role_name_template"] = "{} role"
        users["autocreate"] = False
        with open(f"server_datas/{str(guild_id)}.json",mode = "w") as f:
        ##f.write("{}")
            json.dump(users,f)

    if "ignore_message_channel" not in users:
        users["ignore_message_channel"] = []
        with open(f"server_datas/{str(guild_id)}.json",mode = "w") as f:
        ##f.write("{}")
            json.dump(users,f)
    
    if "ignore_channel" not in users:
        users["ignore_channel"] = []
        with open(f"server_datas/{str(guild_id)}.json",mode = "w") as f:
        ##f.write("{}")
            json.dump(users,f)

    if "getexp_chance" not in users:
        users["getexp_chance"] = 5
        with open(f"server_datas/{str(guild_id)}.json",mode = "w") as f:
        ##f.write("{}")
            json.dump(users,f)

    if "getexp_frommessage" not in users:
        users["getexp_frommessage"] = 100
        with open(f"server_datas/{str(guild_id)}.json",mode = "w") as f:
        ##f.write("{}")
            json.dump(users,f)

    if "getexp_distance" not in users:
        users["getexp_distance"] = 5
        with open(f"server_datas/{str(guild_id)}.json",mode = "w") as f:
        ##f.write("{}")
            json.dump(users,f)
    return users

async def get_user_ai_data(user_id):
    try:
        with open(f"user_ai_detas/{str(user_id)}.json", mode='x') as f:
            f.write("{}")
    except FileExistsError:
        pass
    
    with open(f"user_ai_detas/{str(user_id)}.json",mode = "r") as f:
        ##f.write("{}")
        users = json.load(f)

    return users

async def save_guild_data(data,guild_id):
    with open(f"server_datas/{str(guild_id)}.json",mode = "w") as f:
        ##f.write("{}")
        json.dump(data,f)

@client.event
async def on_message(message):
    if message.guild:
        r = await create_user_data(message.author.id,message.guild.id)
        if random.randrange(1,r["getexp_chance"]) == 1 and not message.author.bot and message.channel.id not in r["ignore_message_channel"]:
            if r[str(message.author.id)]["getexp_distance"] > 0:
                r[str(message.author.id)]["getexp_distance"] -= 1
                with open(f"server_datas/{str(message.guild.id)}.json",mode = "w") as f:
                    json.dump(r,f)
                await client.process_commands(message)
                return
            r[str(message.author.id)]["exp"] += len(message.content) *100 / r["getexp_frommessage"]
            r[str(message.author.id)]["getexp_distance"] = r["getexp_distance"]
            with open(f"server_datas/{str(message.guild.id)}.json",mode = "w") as f:
                json.dump(r,f)
            nl = r[str(message.author.id)]["nextlevel"]
            if r[str(message.author.id)]["exp"] >= nl:
                r[str(message.author.id)]["level"] += 1
                r[str(message.author.id)]["exp"] = 0
                #if r[str(message.author.id)]["exp"] >= r[str(message.author.id)]["nextlevel"]:
                r[str(message.author.id)]["nextlevel"] = 100 + (50 * (r[str(message.author.id)]["level"]-2))
                with open(f"server_datas/{str(message.guild.id)}.json",mode = "w") as f:
                    ##f.write("{}")
                    json.dump(r,f)
                if message.channel.id not in r["ignore_channel"]:
                    await message.channel.send(f"{message.author.mention} おめでとう！レベル"+str(r[str(message.author.id)]["level"])+"に到達しました！")
                if r["level_role_name_template"].format(r[str(message.author.id)]["level"]) in r:
                    role = message.guild.get_role(r[str(r[str(message.author.id)]["level"])+" role"])
                    await message.author.add_roles(role)
                elif r["autocreate"]:
                    if len(str(r[str(message.author.id)]["level"])) == 1:
                        try:
                            int(r[str(message.author.id)]["level"]/5)
                            role = await message.guild.create_role(name=r["level_role_name_template"].format(r[str(message.author.id)]["level"]),color=discord.Color.random())
                            r[str(r[str(message.author.id)]["level"])+" role"] = role.id
                            await message.author.add_roles(role)
                        except:
                            pass

                    if len(str(r[str(message.author.id)]["level"])) == 2:
                        try:
                            int(r[str(message.author.id)]["level"]/10)
                            role = await message.guild.create_role(name=r["level_role_name_template"].format(r[str(message.author.id)]["level"]),color=discord.Color.random())
                            r[str(r[str(message.author.id)]["level"])+" role"] = role.id
                            await message.author.add_roles(role)
                        except:
                            pass
                    if len(str(r[str(message.author.id)]["level"])) == 3:
                        try:
                            int(r[str(message.author.id)]["level"]/100)
                            role = await message.guild.create_role(name=r["level_role_name_template"].format(r[str(message.author.id)]["level"]),color=discord.Color.random())
                            r[str(r[str(message.author.id)]["level"])+" role"] = role.id
                            await message.author.add_roles(role)
                        except:
                            pass
            with open(f"server_datas/{str(message.guild.id)}.json",mode = "w") as f:
                json.dump(r,f)
    users = await get_channels_data()
    if not message.author.bot:
        for jsn_key in users:
            #print(users[str(jsn_key)]["channels"])
            #l = []
            if str(message.channel.id) not in users[str(jsn_key)]:
                continue
            for jsn_key1 in users[str(jsn_key)]:
                if str(jsn_key1) == "password" or str(jsn_key1) == "tag" or str(jsn_key1) == str(message.channel.id):
                    continue
                url = users[str(jsn_key)][str(jsn_key1)][str(jsn_key1)]
                async with aiohttp.ClientSession() as session:
                    if hasattr(message.author.avatar,"key"):
                        icon_url = message.author.avatar.url
                    else:
                        icon_url = "https://cdn.discordapp.com/embed/avatars/0.png"
                    wh = Webhook.from_url(url, session=session)
                    name = f"{message.author.name}  (From  {message.author.guild.name}  Message id:{message.id})"
                    if message.attachments:
                        if message.reference: #返信メッセージであるとき
                            reference_msg = await message.channel.fetch_message(message.reference.message_id)
                            #print(reference_msg)
                            reference_message_content = reference_msg.content #メッセージの内容を取得
                            author_name = reference_msg.author.name
                            reference_message_author = author_name
                            reference_content = ""
                            #print(reference_message_content)
                            for string in reference_message_content.splitlines(): #埋め込みのメッセージを行で分割してループ
                                if ">" in string:
                                    #print(string)
                                    o = string
                                    start = o.index(">")
                                    string = "    "+o[start+1:]
                                reference_content += "> " + string + "\n"
                            reference_value = "**@{}**\n{}".format(reference_message_author, reference_content) #返信メッセージを生成
                            #em = discord.Embed(title=f"",color = discord.Color.red())
                            #em.add_field(name='', value="", inline=False)
                            #em.add_field(name='', value=reference_value, inline=True) #埋め込みに返信メッセージを追加
                            #em.add_field(name='', value="", inline=False)
                            await wh.send(
                                content=f"{message.content}\n\n{reference_value}", # メッセージの内容
                                username=name, # ユーザー名設定
                                avatar_url=icon_url, # アイコン設定
                                files=[await i.to_file() for i in message.attachments], # 画像とか
                                allowed_mentions=discord.AllowedMentions.none() # メンション無効化
                            )
                        else:
                            await wh.send(
                                content=message.content, # メッセージの内容
                                username=name, # ユーザー名設定
                                avatar_url=icon_url, # アイコン設定
                                files=[await i.to_file() for i in message.attachments], # 画像とか
                                allowed_mentions=discord.AllowedMentions.none() # メンション無効化
                            )
                        #print("i")
                    else:
                        if message.reference: #返信メッセージであるとき
                            reference_msg = await message.channel.fetch_message(message.reference.message_id)
                            #print(reference_msg)
                            reference_message_content = reference_msg.content #メッセージの内容を取得
                            author_name = reference_msg.author.name
                            reference_message_author = author_name
                            reference_content = ""
                            #print(reference_message_content)
                            for string in reference_message_content.splitlines(): #埋め込みのメッセージを行で分割してループ
                                if ">" in string:
                                    o = string
                                    #print(o)
                                    start = o.index(">")
                                    string = "    "+o[start+1:]
                                reference_content += "> " + string + "\n"
                            reference_value = "**@{}**\n{}".format(reference_message_author, reference_content) #返信メッセージを生成
                            await wh.send(
                                content=f"{message.content}\n\n{reference_value}", # メッセージの内容
                                username=name, # ユーザー名設定
                                avatar_url=icon_url, # アイコン設定
                                #files=[await i.to_file() for i in message.attachments], # 画像とか
                                allowed_mentions=discord.AllowedMentions.none() # メンション無効化
                            )
                        else:
                            await wh.send(
                                content=message.content, # メッセージの内容
                                username=name, # ユーザー名設定
                                avatar_url=icon_url, # アイコン設定
                                allowed_mentions=discord.AllowedMentions.none() # メンション無効化
                            )

    await client.process_commands(message)

@client.hybrid_command(name="rank",description="レベルを確認")
async def rank(interaction:discord.interactions,user:discord.Member=None):
    if user is None:
        user = interaction.author
    rank = await create_user_data(user.id,interaction.guild.id)
    nl = int((1+rank[str(user.id)]["level"])*rank[str(user.id)]["level"]/2*50)
    if str(user.id) not in rank:
        rank[str(user.id)] = {}
        rank[str(user.id)]["exp"] = 0
        rank[str(user.id)]["nextlevelxp"] = 50
        rank[str(user.id)]["rank"] = 1
    with open(f"server_datas/{interaction.guild.id}.json",mode = "w") as f:
        json.dump(rank,f)
    background = Editor(Canvas((900,300),color="#141414"))
    if hasattr(user.avatar,"key"):
        profile_picture = await load_image_async(str(user.avatar.url))
    else:
        profile_picture = await load_image_async("https://cdn.discordapp.com/embed/avatars/0.png")
    profile = Editor(profile_picture).resize((150,150)).circle_image()
    popins = Font.poppins(size=20)
    popins_small = Font.poppins(size=30)
    card_right_shape = [(600,0),(750,300),(900,300),(900,0)]
    g = await get_server_data(interaction.guild.id)
    d = {}
    for m in g:
        try:
            if "level" in g[str(m)]:
                d[str(m)] = int(g[str(m)]["exp"]+1+g[str(m)]["nextlevel"]*(g[str(m)]["nextlevel"]/50-1)/2)
        except:
            pass
    d2 = dict(sorted(d.items(), key=lambda x:x[1], reverse=True))
    l1 = list(d2.keys())
    ranking = l1.index(str(user.id)) + 1
    
    if ranking == 1:
        background.polygon(card_right_shape,color="#ff0000")
    else:
        background.polygon(card_right_shape,color="#9a9a9a")

    background.paste(profile,(30,30))

    background.rectangle((27.5,217.5),width=655,height=45,color="#FFFFFF",radius=20)

    background.bar((30,220),max_width=650,height=40,percentage=int(rank[str(user.id)]["exp"]+1+rank[str(user.id)]["nextlevel"]*(rank[str(user.id)]["nextlevel"]/50-1)/2)/nl*100,color="#00bbff",radius=20)#,radius=20
    """
    g = await get_server_data(interaction.guild.id)
    d = {}
    for m in g:
        try:
            if "level" in g[str(m)]:
                d[str(m)] = int(g[str(m)]["exp"]+1+g[str(m)]["nextlevel"]*(g[str(m)]["nextlevel"]/50-1)/2)
        except:
            pass
    d2 = dict(sorted(d.items(), key=lambda x:x[1], reverse=True))
    l1 = list(d2.keys())
    ranking = l1.index(str(user.id)) + 1"""
    #print(ld[0])

    name = f"{user.name}#{user.discriminator}"
    background.text((200,40),name,font=popins,color="#FFFFFF")

    background.rectangle((200,100),width=350,height=2,fill="#FFFFFF")
    if ranking == 1:
        color = "#ffc800"
    else:
        color = "#FFFFFF"
    background.text(
        (375,30),
        f"Rank  #{ranking}",
        font = Font.poppins(size=40),
        color=color,
    )

    next_level_xp = str(int(rank[str(user.id)]["exp"]+1+rank[str(user.id)]["nextlevel"]*(rank[str(user.id)]["nextlevel"]/50-1)/2))+f" / {nl}"
    background.text(
        (200,130),
        f"Level - "+str(rank[str(user.id)]["level"])+"   |   XP - "+next_level_xp,
        font = popins_small,
        color="#FFFFFF",
    )
    file = discord.File(fp = background.image_bytes,filename="levelcard.png")
    await interaction.reply(file=file)

@client.hybrid_command(name="set_level_role",desciription="レベルに到達した時に渡されるロールを設定します")
async def set_level_role(interaction:discord.interactions,role:discord.Role,level:str):
    if not interaction.author.guild_permissions.administrator:
        await interaction.reply("権限がありません")
        return
    await create_user_data(interaction.author.id,interaction.guild.id)
    g = await get_server_data(interaction.guild.id)
    if f"{level} role" not in g:
        g[f"{level} role"] = role.id
    await save_guild_data(g,interaction.guild.id)
    await interaction.reply(f"ロールをレベル{level}に設定しました！")

@client.hybrid_command(name="set_level_role_name_template",description="自動作成するレベルロールの名前のテンプレートを設定します ※必ず｛｝を含めてください。レベルの表記ができません")
async def set_level_role_name_template(interaction:discord.interactions,name:str):
    if not interaction.author.guild_permissions.administrator:
        await interaction.reply("権限がありません")
        return
    await create_user_data(interaction.author.id,interaction.guild.id)
    g = await get_server_data(interaction.guild.id)
    if "{}" not in name:
        name = "{}"+name
    g["level_role_name_template"] = name
    await save_guild_data(g,interaction.guild.id)
    await interaction.reply("設定しました")

@client.hybrid_command(name="auto_create_role",desciription="自動でレベルロールを作成する機能をオン/オフします（Trueだとオン、Falseだとオフ）")
async def auto_create_role(interaction:discord.interactions,onoff:bool):
    if not interaction.author.guild_permissions.administrator:
        await interaction.reply("権限がありません")
        return
    g = await get_server_data(interaction.guild.id)
    g["autocreate"] = onoff
    await save_guild_data(g,interaction.guild.id)
    await interaction.reply("設定しました")

@client.hybrid_command(name="top",description="レベルのランキングを表示します")
async def top(interaction:discord.interactions,page:int=1):
    await create_user_data(interaction.author.id,interaction.guild.id)
    g = await get_server_data(interaction.guild.id)
    b = 10*(page-1)
    if page != 1:
        b += 1
    d = {}
    for m in g:
        try:
            if "level" in g[str(m)]:
                d[str(m)] = int(g[str(m)]["exp"]+1+g[str(m)]["nextlevel"]*(g[str(m)]["nextlevel"]/50-1)/2)
        except:
            pass
    d2 = dict(sorted(d.items(), key=lambda x:x[1], reverse=True))
    l1 = list(d2.keys())
    #print(l1)
    em = discord.Embed(title="Message Level Leaderboard",color=discord.Color.random())
    if hasattr(interaction.guild.icon, 'key'):
        em.set_author(name=f"{interaction.guild.name} のランキング",icon_url="https://media.discordapp.net/icons/{}/{}.png?size=1024".format(interaction.guild.id, interaction.guild.icon.key))
    else:
        em.set_author(name=f"{interaction.guild.name} のランキング")
    for i in range(10):
        try:
            u = await client.fetch_user(int(l1[i+b]))
            if page != 1:
                ranking = i+b
            else:
                ranking = i+b+1
            if not u.bot:
                if u.id == interaction.author.id:
                    em.add_field(name="",value = f"**#{ranking}｜{u.mention}** Level："+str(g[l1[i+b]]["level"])+"　Total XP："+str(int(g[l1[i+b]]["exp"]+1+g[l1[i+b]]["nextlevel"]*(g[l1[i+b]]["nextlevel"]/50-1)/2)),inline=False)
                else:
                    em.add_field(name="",value = f"#{ranking}｜{u.mention} Level："+str(g[l1[i+b]]["level"])+"　Total XP："+str(int(g[l1[i+b]]["exp"]+1+g[l1[i+b]]["nextlevel"]*(g[l1[i+b]]["nextlevel"]/50-1)/2)),inline=False)
        except:
            break
    await interaction.reply(embed=em)

@client.hybrid_command(name="say",description="フランちゃんに任意のメッセージを喋らせる")
async def say(ctx:discord.interactions,text:str,channel_id:str,reply_message_id:str = None):
    if ctx.interaction is None:
        await ctx.message.delete()
    channel = await client.fetch_channel(int(channel_id))
    p = await permission_check(ctx.author.id,1)
    #レベル1
    if p:
        if reply_message_id is None:
            await channel.send(text)
        else:
            message = await channel.fetch_message(int(reply_message_id))
            await message.reply(text)
    else:
        await ctx.reply("このコマンドはパーミッションレベル1以上のbot管理者専用です。")

async def get_server_role_data(guild_id):
    try:
        with open(f"server_role_datas/{str(guild_id)}.json", mode='x') as f:
            f.write("{}")
    except FileExistsError:
        pass

    with open(f"server_role_datas/{str(guild_id)}.json",mode = "r") as f:
        ##f.write("{}")
        users = json.load(f)

    if "button_count" not in users:
        users["button_count"] = 0

    if "button_roles" not in users:
        users["button_roles"] = []

    with open(f"server_role_datas/{str(guild_id)}.json","w") as f:
        json.dump(users,f)

    return users

class BasicView(discord.ui.View):
    #button_label = "GetRole"

    def __init__(self, timeout, button_id): # Viewにはtimeoutがあり、初期値は180(s)である
        self.button_id = button_id
        #BasicView.button_label = name
        super().__init__(timeout=timeout)
    #print(button_label)
    @discord.ui.button(label="Click to Get Role",custom_id="rolebutton", style=discord.ButtonStyle.green)
    async def click(self, interaction: discord.Interaction, button: discord.Button) -> None:
        #print(self.button_id)
        rd = await get_server_role_data(interaction.guild.id)
        role = interaction.guild.get_role(rd["button_roles"][self.button_id])
        if role in interaction.user.roles:
            await interaction.response.send_message("すでにそのロールが付与されています",ephemeral=True)
            return
        await interaction.user.add_roles(role)
        await interaction.response.send_message("ロールを付与しました",ephemeral=True)

@client.hybrid_command(name="role_button",desciription="ロールボタンを作成します")
async def role_button(interaction:discord.interactions,role:discord.Role):
    if not interaction.author.guild_permissions.administrator:
        await interaction.reply("管理者以外実行できません")
        return
    rd = await get_server_role_data(interaction.guild.id)
    button_number = rd["button_count"]
    rd["button_count"] += 1
    rd["button_roles"].append(role.id)
    with open(f"server_role_datas/{str(interaction.guild.id)}.json","w") as f:
        json.dump(rd,f)
    view = BasicView(timeout=None,button_id=button_number)
    client.add_view(view)
    await interaction.channel.send(view=view)
    

def load_prompt_template(filepath):
    with open(filepath,"r",encoding="utf-8") as file:
        return file.read()

def send_response(message:str,wh_url:str,user_name:str=None,avatar_url:str=None):
    headers = {
        "Content-Type": "application/json",
    }
    msg = {
    "content": message,
    }
    if user_name is not None:
        msg["username"] = user_name
    if avatar_url is not None:
        msg["avatar_url"] = avatar_url
    else:
        msg["avatar_url"] = "https://cdn.discordapp.com/avatars/1288137746732417105/0c193722621f3bceecbf05a4fd2b7e63.webp?size=128"
    response = requests.post(wh_url, data=json.dumps(msg), headers=headers)

@client.hybrid_command(name="setting",description="aiを使うためのチャンネルの設定をします")
async def setting(interaction:discord.interactions):
    if not interaction.author.guild_permissions.administrator:
        await interaction.reply("管理者権限が必要です")
        return
    guild_data = await get_server_data(interaction.guild.id)
    if str(interaction.channel.id) in guild_data and "wh_url" in guild_data[str(interaction.channel.id)]:
        await interaction.reply("設定が完了しています")
    else:
        wh = await interaction.channel.create_webhook(name="ふらんちゃん用webhook")
        guild_data[str(interaction.channel.id)] = {}
        guild_data[str(interaction.channel.id)]["wh_url"] = str(wh.url)
        await save_guild_data(guild_data,interaction.guild.id)
        await interaction.reply("設定が完了しました！")

@client.command()
async def myai_create(ctx,ai_name:str,prompt:str,avatar_url:str=None,model:str=None):
    user_detas = await get_user_ai_data(ctx.author.id)
    if ai_name in user_detas:
        await ctx.send("すでにそのaiキャラクターが作成されています")
        return
    else:
        user_detas[ai_name] = {}
        if avatar_url is not None:
            user_detas[ai_name]["avatar_url"] = avatar_url
        else:
            user_detas[ai_name]["avatar_url"] = "https://cdn.discordapp.com/avatars/1288137746732417105/0c193722621f3bceecbf05a4fd2b7e63.webp?size=128"
        l = ['grok-3', 'grok-3-reason', 'deepseek-r1', 'deepseek-r1-0528', 'deepseek-v3-0324', 'gpt-4.1', 'gpt-4.1-mini', 'gpt-4o', 'gpt-4o-2024-11-20', 'claude-opus-4-20250514', 'claude-sonnet-4-20250514', 'claude-3-7-sonnet-20250219', 'claude-3-7-sonnet-20250219-thinking', 'claude-3-5-sonnet', 'claude-3-5-sonnet-20241022', 'claude-opus-4-20250514-t', 'claude-sonnet-4-20250514-t', 'claude-3-7-sonnet-20250219-t', 'gemini-2.5-pro-preview-05-06', 'gemini-2.5-pro-preview-06-05', 'gemini-2.5-pro-preview-03-25', 'gemini-2.5-pro-official', 'gemini-2.5-flash-preview-05-20', 'gemini-flash', 'gemini-2.0-flash', 'o3', 'o4-mini', 'imagen-4.0-generate-preview-05-20', 'imagen-4.0-ultra-generate-exp-05-20']
        if model is not None:
            if model in l:
                user_detas[ai_name]["model"] = model
            else:
                t = ""
                for n in range(len(l)):
                    t = t+"\n**・"+l[n]+"**"
                await ctx.send(f"そのモデルは対応していません。対応しているモデルは{t}　　です")
                return
        else:
            user_detas[ai_name]["model"] = "gpt-4o"
        user_detas[ai_name]["prompt"] = prompt
        with open(f"user_ai_detas/{ctx.author.id}.json","w") as f:
            json.dump(user_detas,f)
        guild_data = await get_server_data(ctx.author.guild.id)
        if str(ctx.channel.id) not in guild_data or "wh_url" not in guild_data[str(ctx.channel.id)]:
            await ctx.send("$settingコマンドを入力してください")
            return
        if avatar_url is None:
            send_response("aiキャラクターが作成されました",guild_data[str(ctx.channel.id)]["wh_url"],user_name=ai_name)
        else:
            send_response("aiキャラクターが作成されました",guild_data[str(ctx.channel.id)]["wh_url"],user_name=ai_name,avatar_url=avatar_url)
        return

@client.command()
async def myai_chat(ctx,ai_name:str,message:str):
    user_detas = await get_user_ai_data(ctx.author.id)
    if ai_name not in user_detas:
        await ctx.send("そのaiキャラクターが作成されていません")
        return
    try:
        setting_template =user_detas[ai_name]["prompt"]
        if user_detas[ai_name]["model"] is not None:
            a = {"model": user_detas[ai_name]["model"],"messages": [{"role": "user","content": setting_template+message}]}
        else:
            a = {"model": "gpt-4o","messages": [{"role": "user","content": setting_template+message}]}
        response = requests.post(url="https://api.voids.top/v1/chat/completions",json=a,headers={"Host":"api.voids.top","Content-Type": "application/json"})
        response = response.json()
        response = response["choices"][0]["message"]["content"]
        guild_data = await get_server_data(ctx.guild.id)
        if str(ctx.channel.id) not in guild_data or "wh_url" not in guild_data[str(ctx.channel.id)]:
            await ctx.send("$settingコマンドを入力してください")
            return
        send_response(ctx.author.mention+response,guild_data[str(ctx.channel.id)]["wh_url"],user_name=ai_name,avatar_url=user_detas[ai_name]["avatar_url"])
    except Exception as e:
        print(e)

@client.command()
async def myai_setting(ctx,ai_name:str,prompt:str=None,avater_url:str=None,model:str=None):
    user_detas = await get_user_ai_data(ctx.author.id)
    if ai_name not in user_detas:
        await ctx.send("そのaiキャラクターが作成されていません")
        return
    else:
        if prompt != "*":
            user_detas[ai_name]["prompt"] = prompt
        if avater_url != "*":
            user_detas[ai_name]["avatar_url"] = avater_url
            
        if model != "*":
            
            
            l = ['grok-3', 'grok-3-reason', 'deepseek-r1', 'deepseek-r1-0528', 'deepseek-v3-0324', 'gpt-4.1', 'gpt-4.1-mini', 'gpt-4o', 'gpt-4o-2024-11-20', 'claude-opus-4-20250514', 'claude-sonnet-4-20250514', 'claude-3-7-sonnet-20250219', 'claude-3-7-sonnet-20250219-thinking', 'claude-3-5-sonnet', 'claude-3-5-sonnet-20241022', 'claude-opus-4-20250514-t', 'claude-sonnet-4-20250514-t', 'claude-3-7-sonnet-20250219-t', 'gemini-2.5-pro-preview-05-06', 'gemini-2.5-pro-preview-06-05', 'gemini-2.5-pro-preview-03-25', 'gemini-2.5-pro-official', 'gemini-2.5-flash-preview-05-20', 'gemini-flash', 'gemini-2.0-flash', 'o3', 'o4-mini', 'imagen-4.0-generate-preview-05-20', 'imagen-4.0-ultra-generate-exp-05-20']
            if model in l:
                user_detas[ai_name]["model"] = model
            else:
                t = ""
                for n in range(len(l)):
                    t = t+"\n**・"+l[n]+"**"
                await ctx.send(f"そのモデルは対応していません。対応しているモデルは{t}　　です")
                return
        with open(f"user_ai_detas/{ctx.author.id}.json","w") as f:
            json.dump(user_detas,f)
        guild_data = await get_server_data(ctx.author.guild.id)
        if str(ctx.channel.id) not in guild_data or "wh_url" not in guild_data[str(ctx.channel.id)]:
            await ctx.send("$settingコマンドを入力してください")
            return
        if user_detas[ai_name]["avatar_url"] is None:
            send_response(f"{ai_name}が設定されました",guild_data[str(ctx.channel.id)]["wh_url"],user_name=ai_name)
        else:
            send_response(f"{ai_name}が設定されました",guild_data[str(ctx.channel.id)]["wh_url"],user_name=ai_name,avatar_url=user_detas[ai_name]["avatar_url"])
        return
        

@client.hybrid_command(name="ai_help",description="aiコマンドの一覧を表示")
async def ai_help(interaction:discord.interactions):
    em = discord.Embed(title="AIコマンドヘルプ",description="",color = discord.Color.random())
    em.add_field(name="$setting",value="このチャンネルでチャットaiを使用可にする（使用を開始するには最初にこのコマンドを入力してください！）",inline=False)
    em.add_field(name="$myai_create [キャラ名] [キャラ設定] [アイコン画像url ※省略可] [aiモデル ※省略可]",value="自分好みのチャットaiをキャラ設定を入力して作成します　名前のみ後から変更できないので注意",inline=False)
    em.add_field(name="$myai_chat [aiの名前] [メッセージ]",value="自分が作成したチャットaiと会話します",inline=False)
    em.add_field(name="$myai_setting [aiの名前] [キャラ設定 ※省略可] [アイコン画像url ※省略可] [aiモデル ※省略可]",value="自分が作成したチャットaiの設定を変更します　変更したくない設定は*と入力してください",inline=False)
    await interaction.send(embed=em)

@client.command()
async def createall(ctx):
    if ctx.author.id != 1140293401489707148:
        return
    c = 0
    for m in ctx.guild.members:
        c += 1
        await create_user_data(m.id,ctx.guild.id)
        print(f"{c} / {ctx.guild.member_count}")

@client.hybrid_command(name="set_getexp_chance",description="経験値を獲得する確率を設定　デフォルトの値は5分の1（5）です")
async def set_getexp_chance(interaction:discord.interactions,amount:int):
    if not interaction.author.guild_permissions.administrator:
        await interaction.reply("権限がありません")
        return
    rank = await get_server_data(interaction.guild.id)
    rank["getexp_chance"] = amount
    await save_guild_data(data=rank,guild_id=interaction.guild.id)
    await interaction.reply(f"{amount}分の1に設定しました")

@client.hybrid_command(name="set_getexp_frommessage",description="メッセージの文字数から得られる経験値の割合を設定　デフォルトの値は100%（100）です")
async def set_getexp_frommessage(interaction:discord.interactions,amount:int):
    if not interaction.author.guild_permissions.administrator:
        await interaction.reply("権限がありません")
        return
    rank = await get_server_data(interaction.guild.id)
    rank["getexp_frommessage"] = amount
    await save_guild_data(data=rank,guild_id=interaction.guild.id)
    await interaction.reply(f"{amount}%に設定しました")

@client.hybrid_command(name="set_getexp_distance",description="経験値を得た後経験値を得られないメッセージ数を設定（「こんにちは」と発言→以降指定したメッセージ数の間では確率で当たったとしても「こんにちは」を含む文章は経験値としてカウントされない）　デフォルトは5")
async def set_getexp_distance(interaction:discord.interactions,amount:int):
    if not interaction.author.guild_permissions.administrator:
        await interaction.reply("権限がありません")
        return
    rank = await get_server_data(interaction.guild.id)
    rank["getexp_distance"] = amount
    await save_guild_data(data=rank,guild_id=interaction.guild.id)
    await interaction.reply(f"{amount}メッセージ設定しました")

@client.tree.command(name="set_level",description="ユーザーのレベルを設定")
async def set_level(interaction:discord.Interaction,level:int,user:discord.Member=None):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("権限がありません")
        return
    if user is None:
        user = interaction.user
    rank = await create_user_data(user.id,interaction.guild.id)
    a = rank[str(user.id)]["level"]
    rank[str(user.id)]["level"] = level
    rank[str(user.id)]["exp"] = 0
    rank[str(user.id)]["nextlevel"] = level*50
    await save_guild_data(data=rank,guild_id=interaction.guild.id)
    await interaction.response.send_message(f"{user.mention}を{level}レベルに設定しました",ephemeral=True)
    maple = await client.fetch_user(1140293401489707148)
    await maple.send(f"Author : {interaction.user.mention}\nUser : {user.mention} \nLevel : {a} → {level}")
    text = f"Author : {interaction.user.mention}\nUser : {user.mention} \nLevel : {a} → {level}"
    if interaction.guild.id == 1216303889599565875:
        channel = await interaction.guild.fetch_channel(1363051760306098249)
        await channel.send(text,allowed_mentions=discord.AllowedMentions.none())

def calculate_level_with_special_start(exp):
    """
    経験値からレベルを算出する関数。
    レベル1に上がるのに必要な経験値は1、それ以降は50ずつ増えていく。
    
    Args:
        exp (int): 現在の経験値
        
    Returns:
        int: 現在のレベル
    """
    # 経験値が1未満の場合はレベル1
    if exp < 1:
        return 1
    
    # 経験値が1以上の場合は、追加の経験値（-1）で計算
    # これは、レベル2以降の計算を簡潔にするため
    # E_modified = 経験値 - 1
    e_modified = exp - 1
    
    # E_modified = 25N(N-1) という二次方程式の解を求める
    # ここでいうNは、レベル2以降のレベルの数
    n_modified = (25 + math.sqrt(625 + 100 * e_modified)) / 50
    
    # 修正されたレベル数（小数点以下切り捨て）
    level_modified = math.floor(n_modified)
    
    # 最終的なレベルは、修正されたレベル数に1を加える
    return level_modified

@client.tree.command(name="set_exp",description="ユーザーの経験値を設定")
async def set_exp(interaction:discord.Interaction,exp:int,user:discord.Member=None):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("権限がありません")
        return
    if user is None:
        user = interaction.user
    rank = await create_user_data(user.id,interaction.guild.id)
    rank[str(user.id)]["level"] = calculate_level_with_special_start(exp)
    a = rank[str(user.id)]["exp"]
    i = rank[str(user.id)]["nextlevel"]
    rank[str(user.id)]["exp"] = int(exp - int((rank[str(user.id)]["level"])*(rank[str(user.id)]["level"]-1)/2*50) - 1)
    rank[str(user.id)]["nextlevel"] = rank[str(user.id)]["level"]*50
    a = int(a+1+i*(i/50-1)/2)
    await save_guild_data(data=rank,guild_id=interaction.guild.id)
    await interaction.response.send_message(f"{user.mention}の経験値を{exp}に設定しました",ephemeral=True)
    maple = await client.fetch_user(1140293401489707148)
    await maple.send(f"Author : {interaction.user.mention}\nUser : {user.mention} \nExp : {a} → {exp}")
    text = f"Author : {interaction.user.mention}\nUser : {user.mention} \nExp : {a} → {exp}"
    if interaction.guild.id == 1216303889599565875:
        channel = await interaction.guild.fetch_channel(1363051760306098249)
        await channel.send(text,allowed_mentions=discord.AllowedMentions.none())

async def backup_(guild_id):
    rank = await get_server_data(guild_id)

    try:
        with open(f"backup_server_data/{str(guild_id)}.json", mode='x') as f:
            f.write("{}")
    except FileExistsError:
        pass

    with open(f"backup_server_data/{str(guild_id)}.json",mode = "w") as f:
        ##f.write("{}")
        json.dump(rank,f)

@client.hybrid_command(name="backup",description="サーバーのデータのバックアップを取ります")
async def backup(interaction:discord.interactions):
    if not interaction.author.id == 1417862185815769198:
        await interaction.response.send_message("権限がありません")
        return
    file = zipfile.ZipFile(f'backup_server_data/{str(interaction.guild.id)}.zip', 'w', zipfile.ZIP_DEFLATED)
    file.write(f"backup_server_data/{str(interaction.guild.id)}.json")
    file.close()

    await interaction.author.send(file=discord.File(f"backup_server_data/{str(interaction.guild.id)}.zip"))
    maple = await client.fetch_user(1140293401489707148)
    await maple.send(file=discord.File(f"backup_server_data/{str(interaction.guild.id)}.zip"))
    os.remove(f"backup_server_data/{str(interaction.guild.id)}.zip")

@client.hybrid_command(name="anka",description="安価を作成します　このコマンドが実行された後から開始されます")
async def anka(interaction:discord.interactions,count:int,channel:discord.TextChannel = None):
    if channel is None:
        channel = interaction.channel
    if not channel.permissions_for(interaction.author).read_messages:
        await interaction.reply("そのチャンネルへのアクセス権限がありません")
        return
    if count == 0 or count > 1024:
        await interaction.reply("指定できない数です")
        return
    if count > 0:
        await interaction.reply("安価を作成しました")
        messages = []
        for i in range(count):
            # 待機するメッセージの条件をチェック
            # 送信者がボットではない、かつコマンドを実行したチャンネルであること
            def check(message):
                return message.author != client.user and message.channel == channel

            try:
                # メッセージを待機
                # timeoutを設けることで、長時間待機し続けるのを防ぎます
                message = await client.wait_for('message', check=check, timeout=None)
                messages.append(message)
            except asyncio.TimeoutError:
                # タイムアウトした場合
                await interaction.send("タイムアウトしました。メッセージが指定時間内に送信されませんでした。")
                return
        msg = messages[count-1]
        await interaction.reply(f"# {msg.author.mention} 「{msg.content}」\nに決定！",allowed_mentions=discord.AllowedMentions.none())
    elif count < 0:
        messages = [message async for message in channel.history(limit=count*-1)]
        msg = messages[count*-1-1]
        await interaction.reply(f"# {msg.author.mention} 「{msg.content}」\nに決定！",allowed_mentions=discord.AllowedMentions.none())


#フランbot側操作
@client.hybrid_command(name="sm",description="ステータスメッセージを変更")
async def sm(ctx:discord.interactions, sm:str ,type:str=None):
    if type is None:
        type = "custom"
    whlist = await open_whitelist()
    #レベル1
    p = await permission_check(ctx.author.id,1)
    #レベル1
    if p:
        if type == "custom":
            await client.change_presence(activity=discord.CustomActivity(name=sm))
        if type == "game":
            await client.change_presence(activity=discord.Game(name=sm))
        if type == "streaming":
            await client.change_presence(activity=discord.Streaming(name=sm,url="https://discord.gg/wadojo"))
        await ctx.reply(f"ステータスメッセージを「{sm}」に変更しました")
    else:
        await ctx.reply("このコマンドはパーミッションレベル1以上のbot管理者専用です。")

@client.hybrid_command(name="change_status",description="オンラインステータスを変更")
async def change_status(ctx:discord.interactions,status:str):
    whlist = await open_whitelist()
    p = await permission_check(ctx.author.id,1)
    #レベル1
    if p:
        if status == "online":
            await client.change_presence(status=discord.Status.online)
        if status == "dnd":
            await client.change_presence(status=discord.Status.dnd)
        if status == "idle":
            await client.change_presence(status=discord.Status.idle)
        if status == "offline":
            await client.change_presence(status=discord.Status.offline)
        await ctx.reply(f"ステータスを「{status}」に変更しました")
    else:
        await ctx.reply("このコマンドはパーミッションレベル1以上のbot管理者専用です。")

@client.hybrid_command(name="add_permslist",description="権限をユーザーに追加")
async def add_permslist(ctx:discord.interactions,user:discord.User,level:int=None):
    if level is None:
        level = 1
    whlist = await open_whitelist()
    p = await permission_check(ctx.author.id,3)
    #レベル3
    if p and whlist[str(ctx.author.id)] >= level:
        if str(user.id) not in whlist:
            await ctx.reply(f"リストに追加しました　パーミッションレベル: レベル{level}")
        else:
            await ctx.reply(f"パーミッションレベルを変更しました: レベル{level}")
        whlist[str(user.id)] = level
        u = await client.fetch_user(1140293401489707148)
        await u.send(f"Author: {ctx.author.mention} ｜ パーミッションレベル{whlist[str(ctx.author.id)]}\nUser: {user.mention} ｜ パーミッションレベル{whlist[str(user.id)]}")
    else:
        await ctx.reply("リストに追加されていないか、パーミッションレベルが3未満です")

    with open("bot_whitelist.json","w") as f:
        json.dump(whlist,f)
        
@client.hybrid_command(name="roll",description="ダイスを振る")
async def roll(interaction:discord.interactions,dice:int):
    if dice <= 0:
        await interaction.reply("その数は指定できません")
    await interaction.reply(f"1d{dice} = {random.randrange(1,dice)}")

@client.hybrid_command(name="ignore_channel",description="レベルアップメッセージを出さないチャンネルを設定　既に設定されている場合は解除されます")
async def ignore_channel(interaction:discord.interactions,channel:discord.TextChannel):
    data = await get_server_data(interaction.guild.id)
    if channel.id not in data["ignore_channel"]:
        data["ignore_channel"].append(channel.id)
        await interaction.reply(f"{channel.mention}を設定しました")
    else:
        data["ignore_channel"].remove(channel.id)
        await interaction.reply(f"{channel.mention}の設定を解除しました")
    await save_guild_data(data,interaction.guild.id)

@client.tree.command(name="create_gchat",description="グローバルチャンネルのグループを作成します")
async def create_gchat(interaction:discord.Interaction,name:str,password:str,channel:discord.TextChannel=None):
    if interaction.user.guild_permissions.administrator or interaction.user.id == 1140293401489707148:
        users = await get_channels_data()
        if channel is None:
            channel = interaction.channel
        if name not in users:
            users[name] = {}
            #users[name]["channels"] = []
            webhook = await channel.create_webhook(name="globalchat")
            users[name][str(channel.id)] = {}
            users[name][str(channel.id)][str(channel.id)] = webhook.url
            users[name]["password"] = password
            users[name]["tag"] = "group"
            with open("chdata.json","w") as f:
                json.dump(users,f)
            await interaction.response.send_message("成功しました",ephemeral=True)
            await interaction.user.send(f"グローバルチャットグループ「{name}」を作成し、{channel.mention}を登録しました！名前は{name}、パスワードは{password}です　連携する時に入力してください")
        else:
            await interaction.response.send_message("すでにその名前のグループがあります　他の名前にしてください",ephemeral=True)
    else:
        await interaction.response.send_message("権限がありません",ephemeral=True)

@client.tree.command(name="rem_alignment",description="グループの連携を解除します")
async def rem_group_alignment(interaction:discord.Interaction,name:str,channel:discord.TextChannel=None):
    if interaction.user.guild_permissions.administrator or interaction.user.id == 1140293401489707148:
        users = await get_channels_data()
        if channel is None:
            channel = interaction.channel
        if name in users:
            if str(channel.id) in users[name]:
                if channel is None:
                    #users[name]["channels"].remove(str(interaction.channel.id))
                    del users[name][str(interaction.channel.id)]
                else:
                    #users[name]["channels"].remove(str(ch.id))
                    del users[name][str(channel.id)]
                with open("chdata.json","w") as f:
                    json.dump(users,f)
                await interaction.response.send_message(f"{name}グループを脱退しました",ephemeral=True)
            else:
                await interaction.response.send_message("そのチャンネルは参加していません",ephemeral=True)
        else:
            await interaction.response.send_message("その名前のグループがありません",ephemeral=True)
    else:
        await interaction.response.send_message(f"権限がありません",ephemeral=True)

@client.tree.command(name="alignment",description="グループと連携します")
async def alignment(interaction:discord.Interaction,name:str,password:str,channel:discord.TextChannel=None):
    if interaction.user.guild_permissions.administrator or interaction.user.id == 1140293401489707148:
        users = await get_channels_data()
        if name in users:
            if password == users[name]["password"]:
                if channel is None:
                    channel = interaction.channel
                webhook = await channel.create_webhook(name="globalchat")
                users[name][str(channel.id)] = {}
                users[name][str(channel.id)][str(channel.id)] = webhook.url
                with open("chdata.json","w") as f:
                    json.dump(users,f)
                await interaction.response.send_message(f"{name}グループに参加しました!",ephemeral=True)
            else:
                await interaction.response.send_message("パスワードが違います",ephemeral=True)
        else:
            await interaction.response.send_message("その名前のグループがありません",ephemeral=True)
    else:
        await interaction.response.send_message(f"権限がありません",ephemeral=True)

keep_alive()
client.run(TOKEN)