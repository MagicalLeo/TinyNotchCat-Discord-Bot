# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands
import random
import yt_dlp as youtube_dl
import asyncio
import ollama
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
# from googletrans import Translator
import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ui import View, Button

# load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')
# spotity_secret = os.getenv('SPOTIFY_SECRET')
# intents = discord.Intents.all()
# bot = commands.Bot(command_prefix="%", intents=intents)

COMPLAINTS_FILE = 'complaints.pkl'
complaints = []

# 用于存储对话上下文的字典
user_context = {}
MAX_CONTEXT_LENGTH = 10  # 限制上下文长度

queues = {}
voice_clients = {}
ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                  'options': '-vn -filter:a "volume=0.15"'}
yt_dl_options = {"format": "bestaudio/best"}
ytdl = youtube_dl.YoutubeDL(yt_dl_options)
auto_play = False
now_playing = ''
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='629432fcce9542e1907b19c1757c0956',
                                                           client_secret='9f5c62247ba74d338ec0c54acce676e7'))


# translator = Translator()

# @bot.event
# # 當機器人完成啟動
# async def on_ready():
#     print(f"目前登入身份 --> {bot.user}")
#     await bot.change_presence(status=discord.Status.idle, activity=discord.Game('從北京跑到巴黎'))
#     load_complaints()
#     print("抱怨列表已加載。")


# 按鈕觸發的指令
class CommandView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Hello", custom_id="hello"))
        self.add_item(Button(label="Now Playing", custom_id="nowplaying"))
        self.add_item(Button(label="Joke", custom_id="joke"))
        self.add_item(Button(label="Eat", custom_id="eat"))
        self.add_item(Button(label="Do", custom_id="do"))
        self.add_item(Button(label="Yes or No", custom_id="yesorno"))
        self.add_item(Button(label="Autoplay", custom_id="autoplay"))
        self.add_item(Button(label="Pause", custom_id="pause"))
        self.add_item(Button(label="Resume", custom_id="resume"))
        self.add_item(Button(label="Stop", custom_id="stop"))
        self.add_item(Button(label="Skip", custom_id="skip"))


@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.custom_id == "hello":
        await interaction.response.send_message("Hello, world!", ephemeral=True)
    elif interaction.custom_id == "nowplaying":
        if now_playing:
            await interaction.response.send_message(f'現在播放的是: {now_playing}', ephemeral=True)
        else:
            await interaction.response.send_message("當前沒有播放歌曲", ephemeral=True)
    elif interaction.custom_id == "joke":
        await interaction.response.send_message(random.choice(jokes), ephemeral=True)
    elif interaction.custom_id == "eat":
        await interaction.response.send_message(f"晚上吃甚麼？{random.choice(foods)}？", ephemeral=True)
    elif interaction.custom_id == "do":
        await interaction.response.send_message(f"要幹嘛？{random.choice(activities)}？", ephemeral=True)
    elif interaction.custom_id == "yesorno":
        responses = ["是", "否", "可能", "不確定", "絕對"]
        await interaction.response.send_message(random.choice(responses), ephemeral=True)
    elif interaction.custom_id == "autoplay":
        global auto_play
        auto_play = not auto_play
        await interaction.response.send_message(f"自動播放已{'開啟' if auto_play else '關閉'}", ephemeral=True)
        if auto_play:
            await play_next(interaction)
    elif interaction.custom_id == "pause":
        try:
            voice_clients[interaction.guild.id].pause()
            await interaction.response.send_message("暫停播放", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"無法暫停: {e}", ephemeral=True)
    elif interaction.custom_id == "resume":
        try:
            voice_clients[interaction.guild.id].resume()
            await interaction.response.send_message("恢復播放", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"無法恢復: {e}", ephemeral=True)
    elif interaction.custom_id == "stop":
        try:
            voice_clients[interaction.guild.id].stop()
            await voice_clients[interaction.guild.id].disconnect()
            await interaction.response.send_message("停止播放並斷開連接", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"無法停止: {e}", ephemeral=True)
    elif interaction.custom_id == "skip":
        try:
            if interaction.guild.id in voice_clients and voice_clients[interaction.guild.id].is_playing():
                voice_clients[interaction.guild.id].stop()
                await play_next(interaction)
            else:
                await interaction.response.send_message("目前並沒有正在播放的歌曲。", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"無法跳過: {e}", ephemeral=True)


# The following are commands



# 定義一個命令來顯示按鈕
@bot.command()
async def show_buttons(ctx):
    view = CommandView()
    await ctx.send("按下按鈕來觸發對應的指令：", view=view)

# # 輸入%Hello呼叫指令
# @bot.command()
# async def Hello(ctx: commands.Context):
#     # 回覆Hello, world!
#     await ctx.send("Hello, world!")


# 獲取當前播放音樂
@bot.command()
async def nowplaying(ctx: commands.Context):
    if now_playing:
        await ctx.send('現在播放的是:' + now_playing)
    else:
        await ctx.send("當前沒有播放歌曲")


# Remind 
@bot.command()
async def remind(ctx, time: int = None, user: commands.MemberConverter = None, *, task: str = None):
    # 如果用户没有提供时间或者任务
    if time is None or task is None:
        await ctx.send("請提供時間和任務，例如：%remind @XXX 5 its time to go to bed")
        return

    # 检查用户提及的情况
    if isinstance(user, commands.MemberConverter):
        task = f"{user.mention} {task}"
        user = ctx.author

    if user is None:
        user = ctx.author

    await ctx.send(f"好的! 我會在 {time} 分鐘後提醒{user.mention}: {task}")
    await asyncio.sleep(time * 60)
    await ctx.send(f"{time} 分鐘已經過了! {user.mention}，小凹貓提醒你: {task}")


# # JOKE
# @bot.command()
# async def joke(ctx):
#     await ctx.send(random.choice(jokes))


# # 新增晚上吃甚麼指令
# @bot.command()
# async def eat(ctx):
#     await ctx.send(f"晚上吃甚麼？{random.choice(foods)}？")


# # 新增要幹嘛指令
# @bot.command()
# async def do(ctx):
#     await ctx.send(f"要幹嘛？{random.choice(activities)}？")


def summarize_context(context):
    # 简单的上下文摘要，仅保留系统消息和最近几条消息
    summarized_context = [context[0]]  # 系统消息
    summarized_context.extend(context[-(MAX_CONTEXT_LENGTH - 1):])  # 最近的消息
    return summarized_context


# # yesorno
# @bot.command()
# async def yesorno(ctx, *, question):
#     responses = ["是", "否", "可能", "不確定", "絕對"]
#     await ctx.send(random.choice(responses))


@bot.command()
async def ask(ctx, *, question):
    user_id = str(ctx.author.id)

    if user_id not in user_context:
        user_context[user_id] = [
            {
                'role': 'system',
                'content': "記住!你的名字叫小凹貓，是一隻好吃懶覺股份有限公司的小貓娘。你必須完整回覆用戶的對話!你是在對話，不是在回答問題!不要說抱歉不能回答或不擅長!!!"
            }
        ]

    user_context[user_id].append({
        'role': 'user',
        'content': question
    })

    # 摘要上下文以保持长度
    summarized_context = summarize_context(user_context[user_id])

    async def fetch_response():
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: ollama.chat(model='llama3-CreativeKitty',
                                                                        messages=summarized_context))
        output = response['message']['content']
        print(response)
        await ctx.send(output)
        user_context[user_id].append({
            'role': 'assistant',
            'content': output
        })
        user_context[user_id] = summarize_context(user_context[user_id])

    asyncio.create_task(fetch_response())


# # 推薦歌單
# async def get_recommended_song():
#     global now_playing
#     now_playing = 'https://www.youtube.com/watch?v=' + random.choice(recommended_songs)
#     return now_playing


# 自動播放推薦清單控制
# Autoplay指令
@bot.command()
async def autoplay(ctx):
    global auto_play
    auto_play = not auto_play
    await ctx.send(f"自動播放已{'開啟' if auto_play else '關閉'}")

    if ctx.author.voice and ctx.author.voice.channel:
        try:
            if ctx.guild.id not in voice_clients:
                voice_client = await ctx.author.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
            else:
                voice_client = voice_clients[ctx.guild.id]
                if voice_client.channel != ctx.author.voice.channel:
                    await voice_client.move_to(ctx.author.voice.channel)

            if auto_play:
                if not voice_clients[ctx.guild.id].is_playing():
                    await play_next(ctx)
        except Exception as e:
            await ctx.send(f"無法加入語音頻道: {e}")
    else:
        await ctx.send("請先加入一個音訊頻道！")


async def play_next(ctx):
    global now_playing

    if queues.get(ctx.guild.id):
        next_song = queues[ctx.guild.id].pop(0)
    else:
        if auto_play:
            now_playing = 'https://www.youtube.com/watch?v=' + random.choice(recommended_songs)
            next_song = now_playing
        else:
            return

    loop = asyncio.get_event_loop()
    try:
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(next_song, download=False))
        song = data['url']

        player = discord.FFmpegPCMAudio(song, **ffmpeg_options)
        voice_clients[ctx.guild.id].play(player,
                                         after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
    except Exception as e:
        print(e)


@bot.command()
async def sing(ctx, url):
    if ctx.guild.id not in queues:
        queues[ctx.guild.id] = []

    try:
        voice_client = await ctx.author.voice.channel.connect()
        voice_clients[voice_client.guild.id] = voice_client
    except Exception as e:
        print(e)

    try:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        song = data['url']
        global now_playing
        now_playing = url

        if not voice_clients[ctx.guild.id].is_playing():
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options)
            voice_clients[ctx.guild.id].play(player,
                                             after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))
        else:
            queues[ctx.guild.id].append(url)
            await ctx.send("歌曲已添加到隊列!")
    except Exception as e:
        print(e)


@bot.command()
async def play_spotify_playlist(ctx, playlist_url):
    try:
        playlist_id = playlist_url.split('/')[-1].split('?')[0]
        results = sp.playlist_tracks(playlist_id)
        tracks = results['items']

        if ctx.author.voice and ctx.author.voice.channel:
            voice_channel = ctx.author.voice.channel
            voice_client = await voice_channel.connect()
            voice_clients[ctx.guild.id] = voice_client
        else:
            await ctx.send("請先加入一個音訊頻道！")
            return

        for item in tracks:
            track = item['track']
            track_name = track['name']
            track_artist = track['artists'][0]['name']
            query = f"{track_name} {track_artist} lyrics"

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None,
                                              lambda: ytdl.extract_info(f"ytsearch:{query}", download=False)['entries'][
                                                  0])
            song_url = data['url']
            global now_playing
            now_playing = song_url

            if ctx.guild.id not in queues:
                queues[ctx.guild.id] = []

            queues[ctx.guild.id].append(song_url)
            # await ctx.send(f"已添加歌曲：{track_name} - {track_artist}")

            if not voice_clients.get(ctx.guild.id) or not voice_clients[ctx.guild.id].is_playing():
                await play_next(ctx)
                while voice_clients[ctx.guild.id].is_playing():
                    await asyncio.sleep(1)  # 等待 1 秒，確保下一首歌曲播放完畢再繼續下一首
    except Exception as e:
        print(e)
        await ctx.send("無法播放 Spotify 歌單。請確保 URL 正確並重試。")


# PAUSE
@bot.command()
async def pause(ctx):
    try:
        voice_clients[ctx.guild.id].pause()
    except Exception as e:
        print(e)


# RESUME
@bot.command()
async def resume(ctx):
    try:
        voice_clients[ctx.guild.id].resume()
    except Exception as e:
        print(e)


# STOP
@bot.command()
async def stop(ctx):
    try:
        voice_clients[ctx.guild.id].stop()
        await voice_clients[ctx.guild.id].disconnect()
    except Exception as e:
        print(e)


# SKIP
@bot.command()
async def skip(ctx):
    try:
        if ctx.guild.id in voice_clients and voice_clients[ctx.guild.id].is_playing():
            voice_clients[ctx.guild.id].stop()
            await play_next(ctx)
        else:
            await ctx.send("目前並沒有正在播放的歌曲。")
    except Exception as e:
        print(e)


@bot.command()
async def translate_page(ctx, url: str, lang: str):
    try:
        # 發送 GET 請求獲取網頁內容
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        await ctx.send(f"無法抓取網頁: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    texts = soup.get_text()

    try:
        # 確認語言是否在映射字典中
        if lang in language_mapping:
            lang_code = language_mapping[lang]
            # 分段翻譯長文本
            translated_chunks = chunk_text(texts)
            for chunk in translated_chunks:
                translated = translator.translate(chunk, dest=lang_code)
                await ctx.send(f"翻譯結果: {translated.text[:2000]}")  # Discord 訊息限制為 2000 字
        else:
            await ctx.send("請輸入有效的語言（繁體、簡體、日文或英文）")
    except Exception as e:
        await ctx.send(f"翻譯失敗: {e}")


# 針對長文本，可以考慮分段翻譯
def chunk_text(text, max_length=5000):
    for i in range(0, len(text), max_length):
        yield text[i:i + max_length]


# 翻譯
@bot.command()
async def translate(ctx, lang: str, *, text: str):
    try:
        # 確認語言是否在映射字典中
        if lang in language_mapping:
            lang_code = language_mapping[lang]
            translated = translator.translate(text, dest=lang_code)
            await ctx.send(f"翻譯結果 ({lang}): {translated.text}")
        else:
            await ctx.send("請輸入有效的語言（繁體、簡體、日文或英文）")
    except Exception as e:
        await ctx.send(f"翻譯失敗: {e}")


# calc
@bot.command()
async def calc(ctx, *, expression):
    try:
        result = eval(expression)
        await ctx.send(f"結果是: {result}")
    except Exception as e:
        await ctx.send(f"計算錯誤: {e}")


# def save_complaints():
#     with open(COMPLAINTS_FILE, 'wb') as f:
#         pickle.dump(complaints, f)


# def load_complaints():
#     global complaints
#     try:
#         with open(COMPLAINTS_FILE, 'rb') as f:
#             complaints = pickle.load(f)
#     except FileNotFoundError:
#         complaints = []


# # complain
# @bot.command()
# async def complain(ctx, *, complaint: str):
#     complaints.append(complaint)
#     save_complaints()
#     await ctx.send("你的抱怨已提交!")


# # show_complaint
# @bot.command()
# async def show_complaint(ctx):
#     if complaints:
#         await ctx.send(random.choice(complaints))
#     else:
#         await ctx.send("目前沒有抱怨")


# # clear_complaint
# @bot.command()
# async def clear_complaint(ctx):
#     global complaints
#     complaints = []
#     save_complaints()
#     await ctx.send("抱怨箱已清空!")


# # HELP
# @bot.command()
# async def HELP(ctx):
#     help_message = """
# ```指令以 % 開頭，音樂機器人指令如下：
#     %Hello: 向機器人打招呼，機器人將回覆"Hello, world!"
#     %remind: 設定提醒功能，在一段時間後提醒用戶進行某項任務。
#     %joke: 機器人將隨機傳遞一個笑話。
#     %eat: 提供晚餐建議。
#     %do: 提供活動建議。
#     %ask: 向機器人提問問題，機器人將回答。
#     %autoplay: 控制自動播放推薦清單功能的開啟和關閉。
#     %sing: 播放指定的YouTube歌曲。
#     %pause: 暫停當前播放的歌曲。
#     %resume: 恢復播放暫停的歌曲。
#     %stop: 停止播放歌曲並斷開音訊頻道。
#     %skip: 跳過當前歌曲並播放下一首。
#     %translate_page（已註解掉）: 翻譯網頁內容的指令。
#     %translate（已註解掉）: 翻譯文本的指令。
#     %yesorno: 八卦機，小凹貓會告訴你是或否 
#     %calc: 小凹貓會告訴你計算結果
#     %complain: 你可以和小凹貓抱怨
#     %show_complaint: 看看誰都被抱怨了
#     %clear_complaint: 清空抱怨箱
#     %nowplaying: 獲取當前播放歌曲
# ```
# """
#     await ctx.send(help_message)


@bot.event
# 當頻道有新訊息
async def on_message(message: discord.Message):
    msg = message.content
    if message.author == bot.user:
        return

    if msg.startswith('說'):
        print('你好')
        tmp = msg.replace("說", '')
        await message.channel.send(tmp)

    if '<@1098121534800937011>' in msg:
        meowlist = ['meow', 'Meow', 'MeoW', 'meoW']
        meow = ''
        for i in range(1, random.randrange(12) + 2):
            r = random.randrange(4)
            r2 = random.randrange(100)
            meow += meowlist[r]
            if r2 > 98:
                meow += '!'
            elif r2 > 95:
                meow += '...'
            elif r2 > 88:
                meow += '.'
            elif r2 > 70:
                meow += ','
            else:
                meow += ' '
        await message.channel.send(random.choice(replyList))

    if ('說再見' in msg) or ('<:say_goodbye:963303207407337483>' in msg) or (msg.startswith('88')):
        await message.channel.send(random.choice(goodbyeList))

    if '喵' in msg:
        await message.channel.send(random.choice(meow_responses))

    # 確保命令處理器能夠處理消息
    await bot.process_commands(message)


bot.run(TOKEN)
