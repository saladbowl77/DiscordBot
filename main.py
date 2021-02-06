# インストールした discord.py を読み込む
import discord  # pip install discord.py

from os.path import join, dirname  # 標準ライブラリ
from os import getenv  # 標準ライブラリ
from dotenv import load_dotenv  # pip install python-dotenv

import feedparser  # pip install feedparser
import requests  # pip install request

from dateutil.parser import parse  # pip install python-dateutil

# 環境変数読み込み
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

TOKEN = getenv("DISCORD_TOKEN")

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    print("ログインしました")


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == "/tomato":
        sendTexts = (
            "とまとちゃんぼっとヘルプ\n"
            "コマンド一覧\n"
            "```/rssQiitaTags Qiitaのタグの記事最新の5件を取得します。``````例:/rssQiitaTags python```\n"
            "```/rssQiitaUser Qiitaのユーザーの記事最新の5件を取得します。``````例/rssQiitaUser saladbowl77```\n"
            "\nそのうちまた実用的な機能も実装します\n"
        )

        embed = discord.Embed(
            title="", description=sendTexts, color=0xD5303E
        )  # 16進数カラーコード
        embed.set_author(name="とまとちゃんぼっと", url="https://saladbowl.work", icon_url="")
        await message.channel.send(embed=embed)
    if message.content[:13] == "/rssQiitaTags":
        checkUrl = f"http://qiita.com/tags/{message.content[14:]}/feed.atom"

        feed = feedparser.parse(
            checkUrl, response_headers={"content-type": "text/xml; charset=utf-8"}
        )
        if not feed:
            embed = discord.Embed(
                title="404", description="タグが見当たらないかエラーが発生しました", color=0x55C500
            )  # 16進数カラーコード
            embed.set_author(
                name="QiitaRSS_Tag",
                url="https://qiita.com",
                icon_url="https://cdn.qiita.com/assets/favicons/public/apple-touch-icon-ec5ba42a24ae923f16825592efdc356f.png",
            )
            await message.channel.send(embed=embed)
        else:
            sendTexts = ""
            for rss in feed.entries[:5]:
                publishedTime = parse(str(rss.published))
                publishedTime = publishedTime.strftime("%Y-%m-%d %H:%M")
                sendTexts = f"{sendTexts}[{rss.title}]({rss.link})\nPublished:{publishedTime}\nUser:[{rss.author}](https://qiita.com/{rss.author})\n\n"

            embed = discord.Embed(
                title="", description=sendTexts, color=0x55C500
            )  # 16進数カラーコード
            embed.set_author(
                name="QiitaRSS_Tag",
                url="https://qiita.com",
                icon_url="https://cdn.qiita.com/assets/favicons/public/apple-touch-icon-ec5ba42a24ae923f16825592efdc356f.png",
            )
            await message.channel.send(embed=embed)

    if message.content[:13] == "/rssQiitaUser":
        checkUrl = f"http://qiita.com/{message.content[14:]}/feed.atom"

        feed = feedparser.parse(
            checkUrl, response_headers={"content-type": "text/xml; charset=utf-8"}
        )
        if not feed:
            embed = discord.Embed(
                title="404", description="ユーザーが見当たらないかエラーが発生しました", color=0x55C500
            )  # 16進数カラーコード
            embed.set_author(
                name="QiitaRSS_Tag",
                url="https://qiita.com",
                icon_url="https://cdn.qiita.com/assets/favicons/public/apple-touch-icon-ec5ba42a24ae923f16825592efdc356f.png",
            )
            await message.channel.send(embed=embed)
        else:
            sendTexts = ""
            for rss in feed.entries[:5]:
                publishedTime = parse(str(rss.published))
                publishedTime = publishedTime.strftime("%Y-%m-%d %H:%M")
                sendTexts = f"{sendTexts}[{rss.title}]({rss.link})\nPublished:{publishedTime}\nUser:[{rss.author}](https://qiita.com/{rss.author})\n\n"
            embed = discord.Embed(
                title="", description=sendTexts, color=0x55C500
            )  # 16進数カラーコード
            embed.set_author(
                name="QiitaRSS_User",
                url="https://qiita.com",
                icon_url="https://cdn.qiita.com/assets/favicons/public/apple-touch-icon-ec5ba42a24ae923f16825592efdc356f.png",
            )
            await message.channel.send(embed=embed)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)