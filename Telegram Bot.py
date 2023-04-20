import telebot
import time
import wheather
import requests
import sys
import json
from telebot import custom_filters
from PIL import Image
import glob


TOKEN = '6120316368:AAGhLU0siE2r3WgISN201iRrgse9m_K9kCc'
bot = telebot.TeleBot(TOKEN)
tety=telebot.types
# telebot.apihelper.ENABLE_MIDDLEWARE = True

# @bot.middleware_handler(update_types=['message'])
# def modify_message(bot_instance, message):
#     # modifying the message before it reaches any other handler 
#     message.another_text ='/'+ message.text 







# start
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Heyyyy . Whasap? what can i do for you ma boy?\n /help")

# help
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, """
    you must use this commands:
    /start
    /help
    /wheather
    /resizer --> not working yet
    /horoscope
    """)

@bot.message_handler(commands=['wheather']) # some try 
def wheather_message(message):
    data = wheather.wheather()
    bot.reply_to(message, data)
bot.register_next_step_handler

@bot.message_handler(commands=['matin'])
def matin(message):
    # bot.send_message(message.chat.id, 'slm matin dash in ye teste...')

    # bot.send_audio(message.chat.id, audio=open(r'C:\Users\new\Desktop\CODE\mattybot\12 Nirvana - Something In The Way (Album Version).mp3','rb'))
    
    usersname=(bot.get_chat(chat_id=message.chat.id)).username
    tety.User(id=usersname,is_bot=False,first_name=usersname)

    # m=bot.get_me()
    # bot.send_message(message.chat.id, m)

@bot.message_handler(chat_id=[1570745503, -1001784204202], commands=['update'])
def update_comand(message):
    bot.set_my_commands(
        commands=[
            telebot.types.BotCommand('hi', 'description for name1'),
            telebot.types.BotCommand('name2', 'description for name2'),
            telebot.types.BotCommand('name3', 'description for name3')
        ],
        scope=telebot.types.BotCommandScopeChat(message.chat.id)
    )
bot.add_custom_filter(custom_filters.ChatFilter())





def quote(message):
    
    token = 'e8b4e8bc82027dfdea0e871ee91b90f9/'
    URL = 'https://favqs.com/api/qotd'

    response = requests.request('get',URL)
    j = (response.json())['quote']

    date = (response.json())['qotd_date']
    tags = j['tags']
    url = j['url']
    author = j['author']
    quote = j['body']
    # print(j)
    l = len(tags)
    tags = ''.join(tags)
    tags = tags.replace(' ','#')
    if l>0: 
        text = f'"{quote}"\n\n- Author: {author}\ntag: #{tags}\n{url}'
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
    else:
        text = f'"{quote}"\n\n- Author: {author}\n{url}'
        bot.send_message(message.chat.id, text, parse_mode='Markdown')



@bot.message_handler(commands=['send'])
def photo(message):
    # for file in glob.glob(r'C:\Users\new\Desktop\CODE\telegram bots\mattybot\new\*.png'):
    for i in range(20,80):
        bot.send_photo(message.chat.id, photo=open(rf'C:\Users\new\Desktop\CODE\telegram bots\mattybot\new\new{i}.png', 'rb'))    

















#                         -HOROSCOPE- 
def get_daily_horoscope(sign: str, day: str) -> dict:
    """Get daily horoscope for a zodiac sign.
    Keyword arguments:
    sign:str - Zodiac sign
    day:str - Date in format (YYYY-MM-DD) OR TODAY OR TOMORROW OR YESTERDAY
    Return:dict - JSON data
    """
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)

    return response.json()

@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = "What's your zodiac sign?\nChoose one: ♈*Aries*, ♉*Taurus*, ♊️*Gemini*, ♋️*Cancer,* ♋️*Leo*, ♍️*Virgo*, ♎️*Libra*, ♏️*Scorpio*, ♐️*Sagittarius*, ♑️*Capricorn*, ♒️*Aquarius*, and ♓️*Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

def day_handler(message):
    sign = message.text
    #make list for making vrifie error: 
    list = 'Aries Taurus Gemini Cancer Leo Virgo Libra Scorpio Sagittarius Capricorn Aquarius Pisces'
    list = list.split()
    newlist=[]
    newlist.extend(list)
    for i in list:
        i=i.lower()
        newlist.append(i)
    if sign in newlist:
        text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
        sent_msg = bot.send_message(
            message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(
            sent_msg, fetch_horoscope, sign.capitalize())
    else:
        bot.send_message(message.chat.id, 'اشتباهه')

def fetch_horoscope(message, sign):
    day = message.text
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Here's your horoscope!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")
#horoscope end*




    

@bot.message_handler(commands=["resizer"])
def resizer_message(message):
    username=(bot.get_chat(chat_id=message.chat.id)).username
    text = f"hey @{username}  send me your photo"
    userMessage = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(userMessage,resend_photo)

def resend_photo(message):
    print ('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print ('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print ('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
        




#Buttons
@bot.message_handler(func=lambda message: True)
def error_message(message):
    # bot.reply_to(message, "chi migi seyed??")
    if message.text == 'Quote':
        quote(message)
    elif message.text == 'Horoscope':
        sign_handler(message)
    elif message.text == 'Wheather':
        wheather_message(message)
    else:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
        itembt1 = telebot.types.KeyboardButton('Quote')
        itembt2 = telebot.types.KeyboardButton('Horoscope')
        itembt3 = telebot.types.KeyboardButton('Wheather')
        markup.add(itembt1, itembt2, itembt3)
        bot.send_message(message.chat.id, 'choose one option', reply_markup=markup)

bot.infinity_polling()


