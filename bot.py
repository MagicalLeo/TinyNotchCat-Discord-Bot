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

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
spotity_secret = os.getenv('SPOTIFY_SECRET')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="%", intents=intents)

# 定義回覆消息列表
replyList = [
    '叫屁叫阿 媽的我是貓不是狗ㄟ喵',
    'PoP Cat --> https://popcat.click/  阿喵',
    '喵喵魔咒攻擊(∩^o^)⊃━☆ﾟ.*･｡喵',
    '給你喵幣(・∀・)つ⑩',
    '喵喵破壞傢具功!!喵',
    '欉三小拉喵',
    '喵喵喵!!!!!',
    'Meowwwwwwwwww!!!',
    '貓貓火箭拳的啦!喵',
    '喵喵~desu',
    '喵喵生氣😾',
    ' (=^･ω･^=)喵',
    '哈喵',
    '嘿嘿( Φ ω Φ )',
    '不要吵我啦，喵(=｀ω´=)', '你這人類，喵!', '喵! 我是貓，不是鬧鐘', '再叫我，我就爬你頭上了，喵', '你以為我是狗嗎? 喵',
    '這裡是我的地盤，喵', '看見我尾巴動了嗎? 喵', '人類，注意你的態度，喵', '又想吃罐罐了嗎? 喵', '你知道貓王嗎? 喵',
    '來個貓抓板，喵',
    '喵咪高踢腿', '喵喵跳躍!', '給我貓薄荷，喵', '你想變老鼠嗎? 喵', '貓貓生氣了，喵', '這是貓咪專屬，喵', '喵! 給我安靜',
    '主人，別鬧，喵',
    '貓咪的世界你不懂，喵', '別再叫我了，喵', '你是不是欠抓，喵', '小心我咬你，喵', '人類，你好煩，喵', '給我魚乾，喵',
    '我是高貴的貓，喵', '別打擾我睡覺，喵',
    '你會後悔的，喵', '喵~ 看看我多可愛', '主人，你醒了嗎? 喵', '再叫，我就跑了，喵', '貓咪懶得理你，喵',
    '給我肉罐罐，喵', '貓咪超能量，喵', '喵喵小碎步', '喵，吃飯時間到了', '別看我，喵', '喵! 這裡不是你的', '給我新玩具，喵',
    '人類，我要你注意我，喵'
]

goodbyeList = ['嘿喵', '快去睡拉臭甲喵', 'Zzz...', '徹底喵狂!!!!!', '<:DoUKnowWhatUJustSaid:984290809719439380>',
               '<:say_goodbye:963303207407337483>', '<:gotoBed:1089210502397309009>', '<:bedge:1085608434520576141>',
               'Good night! meow~', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
               'https://www.youtube.com/watch?v=ifm00JEjSeo',
               'https://www.youtube.com/watch?v=vFxjK0WTdTQ', 'https://www.youtube.com/watch?v=Vpda8MPu0mc',
               'https://www.youtube.com/watch?v=TGyLsf7PRpU', 'https://youtu.be/ba7mB8oueCY',
               'https://youtu.be/zpLIbqBVtTg',
               'https://www.youtube.com/watch?v=pKEOgP5ARXU', '晚ㄤ喵', '說再見喵', '喵再見', '掰喵',
               'https://www.youtube.com/watch?v=KKsioz-zaZY',
               'https://www.youtube.com/watch?v=Lhel0tzHE08', '睡你媽逼起來喵喵拳', '舒壓( ˘ω˘)<Zzz',
               '(懶洋洋)喵~明天見啦', '88888喵', '不要和我說再見，一句再見，結局只能喵喵', '881',
               '再會咯地球~', '夢進喵鄉', 'Zz(´-ω-`*)', '喵(´-εヾ )', '看我喵喵拳─=≡Σ((( つ•̀ω•́)つ',
               'ξ( ✿＞◡❛)▄︻▇▇〓▄︻┻┳═一', '祝你好喵', '睡甚麼喵',
               '晚安，喵~', '時間不早了，該休息了喵。', '早點休息，明天會更好喵。', '好夢，喵喵。', '祝你做個美夢喵~',
               '願你的夢境充滿甜蜜，喵。', '夜深了，記得早點睡覺喵。', '貓咪也要休息了，喵。', '明天再見，喵~',
               '夢中與你相遇，喵喵。', '祝你有個安靜的夜晚，喵。', '夢裡會有驚喜，喵！', '嗯吶，晚安，喵。', '有夢就有歸處，喵。',
               '願每一個晚安都是甜蜜的，喵。', '累了一天，該好好休息了，喵。',
               '星星在天空閃耀，夢在心裡發光，晚安，喵。', '貓咪會在夢中保護你，喵。', '夜深了，貓咪也要去夢鄉了，喵。',
               '呼嚕呼嚕，夢裡的貓咪也會和你一起呼嚕呼嚕，喵~'
               ]

jokes = [
    "為什麼小凹貓喜歡電腦？因為它們喜歡踩在鍵盤上！",
    "小凹貓的最愛歌曲是什麼？《貓的搖籃曲》！",
    "你知道小凹貓最討厭什麼嗎？狗！",
    "為什麼小凹貓不喜歡說謊？因為它們不喜歡 '狗' 謊！",
    "你知道小凹貓最喜歡的數字是什麼嗎？貓（毛）數！",
    "小凹貓的最愛運動是什麼？撲撲跳！",
    "為什麼小凹貓喜歡晚上出門？因為它們有夜視眼！",
    "小凹貓在沙灘上最喜歡做什麼？抓沙！",
    "你知道小凹貓最喜歡喝什麼嗎？貓薄荷茶！",
    "為什麼小凹貓喜歡看電影？因為它們喜歡 '咪' 奇妙的世界！",
    "小凹貓的最愛遊戲是什麼？躲貓貓！",
    "為什麼小凹貓常常打盹？因為它們有貓瞌睡！",
    "你知道小凹貓的最愛食物是什麼嗎？罐罐和魚乾！",
    "小凹貓最怕什麼？洗澡！",
    "為什麼小凹貓總是看起來那麼高傲？因為它們覺得自己是貓王！",
    "小凹貓的最愛節日是什麼？國際貓咪日！",
    "你知道小凹貓最討厭什麼聲音嗎？吸塵器！",
    "小凹貓為什麼喜歡紙箱？因為它們覺得紙箱是它們的小城堡！",
    "你知道小凹貓的最愛顏色是什麼嗎？橘色，因為那是金黃色的貓咪！",
    "為什麼小凹貓喜歡高處？因為它們覺得自己是國王！",
    "你知道小凹貓怎麼向朋友問好嗎？它們用鼻子碰碰！",
    "小凹貓為什麼喜歡用爪子？因為它們要保持爪子的鋒利！",
    "小凹貓最喜歡做的事是什麼？打盹和吃罐罐！",
    "你知道小凹貓為什麼喜歡躺在陽光下嗎？因為它們喜歡曬太陽！",
    "為什麼小凹貓會捉老鼠？因為它們覺得這是個遊戲！",
    "凹凹偷偷在公司廁所裡放置攝像頭，暗中監控員工的上廁所行為，引起了一場隱私保護風波。",
    "阿哲頭在公司年度聖誕派對上偷偷在飲料中添加了臭酸味的成分，讓所有人的聖誕快樂氣氛瞬間破滅。",
    "阿酸頭將公司的辦公室空調調至極低溫，讓同事們冷得瑟瑟發抖，而他卻裹著厚厚的羽絨服舒適地坐在辦公桌前。",
    "滴發發偷偷在公司午餐室的咖啡機中添加了催眠藥，企圖在同事們午休時窃取他們的機密文件。",
    "阿豬頭在公司餐廳的自助餐中偷偷放入了大量的辣椒粉，導致同事們紛紛被辣得喘不過氣來。",
    "凹凹趁著辦公室聚會的機會，把一隻迷路的貓帶進了辦公室，讓整個辦公室陷入一片混亂。",
    "阿哲頭在公司的會議上突然開始大聲哭泣，聲稱他的金魚死了，結果讓所有同事們都感到尷尬不已。",
    "阿酸頭偷偷在公司的植物中放置了一隻假蛇，嚇得同事們一陣尖叫，他卻得意地笑了起來。",
    "滴發發趁著同事們上廁所的時候，將所有的電腦滑鼠換成了一個超級敏感的設置，讓他們回來後一頭霧水。",
    "阿豬頭趁著同事們午休的時候，偷偷在辦公室放了一個假的恐龍模型，結果讓同事們回來後吓得魂飛魄散。",
    "凹凹在公司辦公室的水龍頭中放了顏料，導致同事們打開水龍頭時被噴灑得全身都是顏料，成了彩虹人。",
    "阿哲頭偷偷在公司的電梯裡放了一群蜜蜂，結果引發了一場驚慌失措的電梯事件。",
    "阿酸頭在公司的停車場裡放了一個氣球地雷，當同事們開車進入時，地雷爆炸了，汽車輪胎全都被刺破。",
    "滴發發把公司辦公室的香水噴霧換成了螢光塑料彩帶，導致同事們噴了香水後身上全是五顏六色的塑料帶子。",
    "阿豬頭在公司的電子郵件系統中寄發了一封假的遺囑，聲稱公司老闆將全部財產捐給了他，引起了一場極大的混亂和不滿。",
    '你知道嗎，凹凹利用公司資源進行非法監控',
    '你知道嗎，阿豬頭私自篡改員工績效評定',
    '你知道嗎，小凹貓與機器人勞工串通，偷偷拍攝公司機密',
    '你知道嗎，阿哲頭在研發過程中隱瞞了一個致命缺陷',
    '你知道嗎，阿酸頭利用公司資金進行個人投資，涉嫌內部交易',
    '你知道嗎，滴發發通過不正當手段獲得了大量股份',
    '你知道嗎，凹凹對公司董事會隱瞞了一筆龐大的財務風險',
    '你知道嗎，阿豬頭收受員工回扣，影響了招聘和晉升決策',
    '你知道嗎，小凹貓利用公司社交平台散佈假消息，損害公司聲譽',
    '你知道嗎，阿哲頭竊取了競爭對手的技術，違反了知識產權法',
    '你知道嗎，阿酸頭在財務報告中隱藏了公司虧損情況',
    '你知道嗎，滴發發透過行賄手段獲得了政府合同',
    '你知道嗎，凹凹通過偽造文件來掩蓋公司的法律風險',
    '你知道嗎，阿豬頭操控了公司股價，從中獲利',
    '你知道嗎，小凹貓與外部竊賊合作，偷竊公司機密文件',
    '你知道嗎，阿哲頭在新產品上故意添加了有毒成分',
    '你知道嗎，阿酸頭在公司收入分配上作了不公正的安排',
    '你知道嗎，滴發發利用公司資源開展了一項違法企業',
    '你知道嗎，凹凹通過操縱股東大會來控制公司決策',
    '你知道嗎，阿豬頭利用內部消息交易股票，違反證券法'
    # '你知道嗎，<@611388157010771989>利用公司資源進行非法監控',
    # '你知道嗎，<@632444792026169364>私自篡改員工績效評定',
    # '你知道嗎，小凹貓與機器人勞工串通，偷偷拍攝公司機密',
    # '你知道嗎，<@614357104735682560>在研發過程中隱瞞了一個致命缺陷',
    # '你知道嗎，<@632446444648792064>利用公司資金進行個人投資，涉嫌內部交易',
    # '你知道嗎，<@516602109391798274>通過不正當手段獲得了大量股份',
    # '你知道嗎，<@611388157010771989>對公司董事會隱瞞了一筆龐大的財務風險',
    # '你知道嗎，<@632444792026169364>收受員工回扣，影響了招聘和晉升決策',
    # '你知道嗎，小凹貓利用公司社交平台散佈假消息，損害公司聲譽',
    # '你知道嗎，<@614357104735682560>竊取了競爭對手的技術，違反了知識產權法',
    # '你知道嗎，<@632446444648792064>在財務報告中隱藏了公司虧損情況',
    # '你知道嗎，<@516602109391798274>透過行賄手段獲得了政府合同',
    # '你知道嗎，<@611388157010771989>通過偽造文件來掩蓋公司的法律風險',
    # '你知道嗎，<@632444792026169364>操控了公司股價，從中獲利',
    # '你知道嗎，小凹貓與外部竊賊合作，偷竊公司機密文件',
    # '你知道嗎，<@614357104735682560>在新產品上故意添加了有毒成分',
    # '你知道嗎，<@632446444648792064>在公司收入分配上作了不公正的安排',
    # '你知道嗎，<@516602109391798274>利用公司資源開展了一項違法企業',
    # '你知道嗎，<@611388157010771989>通過操縱股東大會來控制公司決策',
    # '你知道嗎，<@632444792026169364>利用內部消息交易股票，違反證券法',
    # "<@611388157010771989>偷偷在公司廁所裡放置攝像頭，暗中監控員工的上廁所行為，引起了一場隱私保護風波。",
    # "<@614357104735682560>在公司年度聖誕派對上偷偷在飲料中添加了臭酸味的成分，讓所有人的聖誕快樂氣氛瞬間破滅。",
    # "<@632446444648792064>將公司的辦公室空調調至極低溫，讓同事們冷得瑟瑟發抖，而他卻裹著厚厚的羽絨服舒適地坐在辦公桌前。",
    # "<@516602109391798274>偷偷在公司午餐室的咖啡機中添加了催眠藥，企圖在同事們午休時窃取他們的機密文件。",
    # "<@632444792026169364>在公司餐廳的自助餐中偷偷放入了大量的辣椒粉，導致同事們紛紛被辣得喘不過氣來。",
    # "<@611388157010771989>趁著辦公室聚會的機會，把一隻迷路的貓帶進了辦公室，讓整個辦公室陷入一片混亂。",
    # "<@614357104735682560>在公司的會議上突然開始大聲哭泣，聲稱他的金魚死了，結果讓所有同事們都感到尷尬不已。",
    # "<@632446444648792064>偷偷在公司的植物中放置了一隻假蛇，嚇得同事們一陣尖叫，他卻得意地笑了起來。",
    # "<@516602109391798274>趁著同事們上廁所的時候，將所有的電腦滑鼠換成了一個超級敏感的設置，讓他們回來後一頭霧水。",
    # "<@632444792026169364>趁著同事們午休的時候，偷偷在辦公室放了一個假的恐龍模型，結果讓同事們回來後吓得魂飛魄散。",
    # "<@611388157010771989>在公司辦公室的水龍頭中放了顏料，導致同事們打開水龍頭時被噴灑得全身都是顏料，成了彩虹人。",
    # "<@614357104735682560>偷偷在公司的電梯裡放了一群蜜蜂，結果引發了一場驚慌失措的電梯事件。",
    # "<@632446444648792064>在公司的停車場裡放了一個氣球地雷，當同事們開車進入時，地雷爆炸了，汽車輪胎全都被刺破。",
    # "<@516602109391798274>把公司辦公室的香水噴霧換成了螢光塑料彩帶，導致同事們噴了香水後身上全是五顏六色的塑料帶子。",
    # "<@632444792026169364>在公司的電子郵件系統中寄發了一封假的遺囑，聲稱公司老闆將全部財產捐給了他，引起了一場極大的混亂和不滿。"
]

meow_responses = [
    '喵~',
    '喵喵!',
    '喵喵喵~',
    '喵嗚~',
    '你叫我嗎？喵~',
    '喵嗷嗷嗷~',
    '喵星人報到!',
    '我在這裡，喵~',
    '你也是喵星人嗎？',
    '喵喵呼應!',
    '來陪我玩吧，喵~',
    '喵咪生氣了！',
    '喵嗚嗚嗚~',
    '喵喵~ 什麼事？',
    '主人，你叫我嗎？喵~',
    '喵~ 有什麼好吃的嗎？',
    '喵~ 我要罐罐!',
    '喵~ 一起玩吧!',
    '喵~ 給我摸摸!',
    '喵~ 今天的天氣真好!',
    '喵~ 我好可愛!',
    '喵~ 來陪我玩!',
    '喵~ 你喜歡貓嗎？',
    '喵~ 我在這裡!',
    '喵~ 你在幹嘛？',
    '喵~ 來聽聽我唱歌!',
    '喵~ 我餓了!',
    '喵~ 一起看電影嗎？',
    '喵~ 來聊天吧!',
    '喵~ 今天的心情真好!',
    '喵~ 喜歡我的毛嗎？',
    '喵~ 我是最棒的貓咪!'
]

activities = [
    "看電影",
    "看影集",
    "玩APEX",
    "玩OVERWATCH",
    "玩Minecraft",
    '玩Pico Park',
    "聊天",
    "讀書",
    "寫程式",
    "散步",
    "打掃房間",
    "玩遊戲",
    "看漫畫",
    "看動漫",
    "聽音樂",
    "睡覺",
    '倒垃圾',
    '尻',
    'It\'s time to go to bed'
]

foods = [
    "壽司",
    "披薩",
    "漢堡",
    "炸雞",
    "拉麵",
    "牛肉麵",
    "義大利麵",
    "火鍋",
    "涼麵",
    "泡麵",
    "燒烤",
    "沙拉",
    "三明治",
    "炒飯",
    "煎餃",
    "烤肉",
    "麵包",
    "包子",
    "鍋貼",
    "蛋包飯",
    "烏龍麵",
    "咖哩飯",
    "素食",
    "牛排",
    "香腸",
    "可樂餅",
    "潛艇堡",
    "咖啡",
    "蛋糕",
    "奶茶",
    "炸魚",
    "炸蝦",
    "海鮮",
    "關東煮",
    "雞肉",
    "蔬菜",
    "水餃",
    "炒麵",
    "米飯",
    "乳酪",
    "烤雞",
    "批薩",
    "魚片",
    "魚丸",
    "烤魚",
    "魚排",
    "蛋糕捲",
    "吐司",
    "蛋塔",
    "奶酪",
    "奶昔",
    "冰淇淋",
    "香蕉",
    "蘋果",
    "芒果",
    "水果沙拉",
    "酸奶",
    "檸檬",
    "葡萄",
    "蓮霧",
    "橘子",
    "櫻桃",
    "西瓜",
    "哈密瓜",
    "木瓜",
    "草莓",
    "覆盆子",
    "蜜糖",
    "蜂蜜",
    "花生醬",
    "果凍",
    "果汁",
    "汽水",
    "可樂",
    "果醋",
    "奶油",
    "甜點",
    "雪糕",
    "冰棒",
    "巧克力",
    "糖果",
    "餅乾",
    "麻糬"
]

# 定義語言對應字典
language_mapping = {
    '繁體': 'zh-tw',
    '簡體': 'zh-cn',
    '日文': 'ja',
    '英文': 'en'
}

recommended_songs = ["psuRGfAaju4",
                     "Cwkej79U3ek",
                     "KRaWnd3LJfs",
                     "mk48xRzuNvA",
                     "mWRsgZuwf_8",
                     "oozQ4yV__Vw",
                     "Y7ix6RITXM0",
                     "H7HmzwI67ec",
                     "q74fX9CnqtQ",
                     "qV5lzRHrGeg",
                     "fWNaR-rxAic",
                     "-Lh9gqa1WBY",
                     "oxqnFJ3lp5k",
                     "gS9o1FAszdk",
                     "F90Cw4l-8NY",
                     "aatr_2MstrI",
                     "cHHLHGNpCSA",
                     "fOICI1bBhgE",
                     "IcrbM1l_BoI",
                     "sbOcVER0WqU",
                     "QJO3ROT-A4E",
                     "G5xSLbYMr-I",
                     "VT1-sitWRtY",
                     "BZsXcc_tC-o",
                     "xo1VInw-SKc",
                     "IxxstCcJlsc",
                     "m-M1AtrxztU",
                     "MzCLLHscMOw",
                     "4zbVIsL8OOY",
                     "ntSBKPkk4m4",
                     "nLnp0tpZ0ok",
                     "bxV-OOIamyk",
                     "Cx6PaF0odCw",
                     "ChukpOHfAI8",
                     "mNEUkkoUoIA",
                     "jO2viLEW-1A",
                     "EkHTsc9PU2A",
                     "EQ94zflNqn4",
                     "YAXTn0E-Zgo",
                     "7JJfJgyHYwU",
                     "Uq8Dgcy4MDY",
                     "sXd2WxoOP5g",
                     "6J1-eYBbspA",
                     "HNAM2EVXH9A",
                     "IJ-I6KviOf8",
                     "qM1YMeDsc-M",
                     "6JCLY0Rlx6Q",
                     "2tY5RErnakc",
                     "gfA-tPKPoNs",
                     "K5NEOwRXa_8",
                     "ZttNKZ6NLhs",
                     "zO8yNYEsYTc",
                     "iP3PcDNhJXI",
                     "Uv_yBmIiZTM",
                     "GeK5TmZTxXk",
                     "8ZP5eqm4JqM",
                     "kGKFs-PIROs",
                     "BHfL4ns7-CM",
                     "GVbHjcfVO50",
                     "xSxjhvy8vrU",
                     "EZlD-H-6WzU",
                     "FNJG6MsKO0k",
                     "Fh1yD5pVhMc",
                     "NbNPJr_0tqA",
                     "gF7FBLqAiQM",
                     "f_XHSsI9wBI",
                     "8L5cQlXMpeY",
                     "Odv-zbpy-Y8",
                     "xX7xWEh6ujk",
                     "q4CbHfW3Ji8",
                     "TLvMXOEXi_k",
                     "6Gp6Oxl_Vtw",
                     "pyDCubgU57g",
                     "iQs-f88RBws",
                     "YAXTn0E-Zgo",
                     "mp2-w15SXms",
                     "gsT6eKsnT0M"]

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

@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('從北京跑到巴黎'))
    load_complaints()
    print("抱怨列表已加載。")


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

# 輸入%Hello呼叫指令
@bot.command()
async def Hello(ctx: commands.Context):
    # 回覆Hello, world!
    await ctx.send("Hello, world!")


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


# JOKE
@bot.command()
async def joke(ctx):
    await ctx.send(random.choice(jokes))


# 新增晚上吃甚麼指令
@bot.command()
async def eat(ctx):
    await ctx.send(f"晚上吃甚麼？{random.choice(foods)}？")


# 新增要幹嘛指令
@bot.command()
async def do(ctx):
    await ctx.send(f"要幹嘛？{random.choice(activities)}？")


def summarize_context(context):
    # 简单的上下文摘要，仅保留系统消息和最近几条消息
    summarized_context = [context[0]]  # 系统消息
    summarized_context.extend(context[-(MAX_CONTEXT_LENGTH - 1):])  # 最近的消息
    return summarized_context


# yesorno
@bot.command()
async def yesorno(ctx, *, question):
    responses = ["是", "否", "可能", "不確定", "絕對"]
    await ctx.send(random.choice(responses))


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


def save_complaints():
    with open(COMPLAINTS_FILE, 'wb') as f:
        pickle.dump(complaints, f)


def load_complaints():
    global complaints
    try:
        with open(COMPLAINTS_FILE, 'rb') as f:
            complaints = pickle.load(f)
    except FileNotFoundError:
        complaints = []


# complain
@bot.command()
async def complain(ctx, *, complaint: str):
    complaints.append(complaint)
    save_complaints()
    await ctx.send("你的抱怨已提交!")


# show_complaint
@bot.command()
async def show_complaint(ctx):
    if complaints:
        await ctx.send(random.choice(complaints))
    else:
        await ctx.send("目前沒有抱怨")


# clear_complaint
@bot.command()
async def clear_complaint(ctx):
    global complaints
    complaints = []
    save_complaints()
    await ctx.send("抱怨箱已清空!")


# HELP
@bot.command()
async def HELP(ctx):
    help_message = """
```指令以 % 開頭，音樂機器人指令如下：
    %Hello: 向機器人打招呼，機器人將回覆"Hello, world!"
    %remind: 設定提醒功能，在一段時間後提醒用戶進行某項任務。
    %joke: 機器人將隨機傳遞一個笑話。
    %eat: 提供晚餐建議。
    %do: 提供活動建議。
    %ask: 向機器人提問問題，機器人將回答。
    %autoplay: 控制自動播放推薦清單功能的開啟和關閉。
    %sing: 播放指定的YouTube歌曲。
    %pause: 暫停當前播放的歌曲。
    %resume: 恢復播放暫停的歌曲。
    %stop: 停止播放歌曲並斷開音訊頻道。
    %skip: 跳過當前歌曲並播放下一首。
    %translate_page（已註解掉）: 翻譯網頁內容的指令。
    %translate（已註解掉）: 翻譯文本的指令。
    %yesorno: 八卦機，小凹貓會告訴你是或否 
    %calc: 小凹貓會告訴你計算結果
    %complain: 你可以和小凹貓抱怨
    %show_complaint: 看看誰都被抱怨了
    %clear_complaint: 清空抱怨箱
    %nowplaying: 獲取當前播放歌曲
```
"""
    await ctx.send(help_message)


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
