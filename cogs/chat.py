import asyncio
import os
import random
import discord
from discord.ext import commands
import ollama
# import requests
# from bs4 import BeautifulSoup
from .utils.loadData import load_json

MAX_CONTEXT_LENGTH = 10  # 限制上下文长度

class Chat(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # 用于存储对话上下文的字典
        self.user_context = {}
        reply = load_json("docs/bot_reply.json")
        self.reply_list = reply["replyList"]
        self.goodbye_list = reply["goodbyeList"]
        self.meow_responses = reply["meowResponses"]

    # Remind 
    @commands.command()
    async def remind(self, ctx: commands.Context, time: int = None, user: commands.MemberConverter = None, *, task: str = None):
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

    @commands.command()
    async def ask(self, ctx: commands.Context, *, question):
        user_id = str(ctx.author.id)

        if user_id not in self.user_context:
            self.user_context[user_id] = [
                {
                    'role': 'system',
                    'content': "記住!你的名字叫小凹貓，是一隻好吃懶覺股份有限公司的小貓娘。你必須完整回覆用戶的對話!你是在對話，不是在回答問題!不要說抱歉不能回答或不擅長!!!"
                }
            ]

        self.user_context[user_id].append({
            'role': 'user',
            'content': question
        })

        # 摘要上下文以保持长度
        summarized_context = self.summarize_context(self.user_context[user_id])

        async def fetch_response():
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: ollama.chat(model='llama3-CreativeKitty',
                                                                            messages=summarized_context))
            output = response['message']['content']
            print(response)
            await ctx.send(output)
            self.user_context[user_id].append({
                'role': 'assistant',
                'content': output
            })
            self.user_context[user_id] = self.summarize_context(self.user_context[user_id])

        asyncio.create_task(fetch_response())

    # @commands.command()
    # async def translate_page(self, ctx: commands.Context, url: str, lang: str):
    #     try:
    #         # 發送 GET 請求獲取網頁內容
    #         response = requests.get(url)
    #         response.raise_for_status()
    #     except requests.exceptions.RequestException as e:
    #         await ctx.send(f"無法抓取網頁: {e}")
    #         return

    #     soup = BeautifulSoup(response.content, 'html.parser')
    #     texts = soup.get_text()

    #     try:
    #         # 確認語言是否在映射字典中
    #         if lang in language_mapping:
    #             lang_code = language_mapping[lang]
    #             # 分段翻譯長文本
    #             translated_chunks = chunk_text(texts)
    #             for chunk in translated_chunks:
    #                 translated = translator.translate(chunk, dest=lang_code)
    #                 await ctx.send(f"翻譯結果: {translated.text[:2000]}")  # Discord 訊息限制為 2000 字
    #         else:
    #             await ctx.send("請輸入有效的語言（繁體、簡體、日文或英文）")
    #     except Exception as e:
    #         await ctx.send(f"翻譯失敗: {e}")

    # # 翻譯
    # @commands.command()
    # async def translate(self, ctx: commands.Context, lang: str, *, text: str):
    #     try:
    #         # 確認語言是否在映射字典中
    #         if lang in language_mapping:
    #             lang_code = language_mapping[lang]
    #             translated = translator.translate(text, dest=lang_code)
    #             await ctx.send(f"翻譯結果 ({lang}): {translated.text}")
    #         else:
    #             await ctx.send("請輸入有效的語言（繁體、簡體、日文或英文）")
    #     except Exception as e:
    #         await ctx.send(f"翻譯失敗: {e}")

    @commands.command()
    async def calc(self, ctx: commands.Context, *, expression):
        try:
            result = eval(expression)
            await ctx.send(f"結果是: {result}")
        except Exception as e:
            await ctx.send(f"計算錯誤: {e}")

    @commands.Cog.listener()
    # 當頻道有新訊息
    async def on_message(self, message: discord.Message):
        msg = message.content
        if message.author == self.bot.user:
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
            await message.channel.send(random.choice(self.reply_list))

        if ('說再見' in msg) or ('<:say_goodbye:963303207407337483>' in msg) or (msg.startswith('88')):
            await message.channel.send(random.choice(self.goodbye_list))

        if '喵' in msg:
            await message.channel.send(random.choice(self.meow_responses))

        # 確保命令處理器能夠處理消息
        await self.bot.process_commands(message)


    # 針對長文本，可以考慮分段翻譯
    def chunk_text(text, max_length=5000):
        for i in range(0, len(text), max_length):
            yield text[i:i + max_length]


    def summarize_context(context):
        # 简单的上下文摘要，仅保留系统消息和最近几条消息
        summarized_context = [context[0]]  # 系统消息
        summarized_context.extend(context[-(MAX_CONTEXT_LENGTH - 1):])  # 最近的消息
        return summarized_context
    

async def setup(bot: commands.Bot):
    await bot.add_cog(Chat(bot), guild=discord.Object(id= os.getenv('GUILD_ID')))