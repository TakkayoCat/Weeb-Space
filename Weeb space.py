import telebot
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from time import sleep
import random

bot_name = "Weeb space"
hello = ['Привет', 'Приветик👋', 'Привет, всё готово для работы🛠']
goodbye = ['Пока', 'До встречи👋', 'Прорешаешь задачку напоследок🧠? /math']

driver = webdriver.Chrome()
 
TOKEN = "7771595576:AAHOSTYPsWLw7k0Re6i_kK6ORRi5mDboOyw"
bot = telebot.TeleBot(TOKEN)

#start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Привет', '/help', 'Пока', '/secret')
    bot.send_message(message.chat.id, "Вас приветствует " + bot_name + ", располагайтесь. Введите /help, чтобы вникнуть в атмосферу weeb'ов.", reply_markup=markup)


#help
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, """<b>

/weather - Узнать погоду в минске
/search - Поисковой запрос в Yandex
/market - Поиск на YandexМаркет
/prog_lang - Популярные языки программирования
/youtube - Поиск видео на YouTube
/subscribers - Узнать подписчиков своего youtube-канала
/games - Свежие релизы игр
/films - Новые фильмы
/math - Математическая "головоломка"

    </b>""", parse_mode='html')


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text.lower() == 'привет':
        num_expression = random.randint(0, len(hello)-1)
        bot.send_message(message.chat.id, "<b>" + hello[num_expression] + "</b>", parse_mode='html')
    if message.text.lower() == 'пока':
        num_expression = random.randint(0, len(goodbye)-1)
        bot.send_message(message.chat.id, "<b>" + goodbye[num_expression] + "</b>", parse_mode='html')


#Реализовать
@bot.message_handler(commands=['secret'])
def secret(message):
    secrets = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton(' ', callback_data='0')
    item2 = types.InlineKeyboardButton(' ', callback_data='1')
    item3 = types.InlineKeyboardButton(' ', callback_data='2')
    secrets.add(item, item1, item2)
    bot.send_message(message.chat.id, 'А вот и секрет!', reply_markup = secrets)


@bot.callback_query_handler(func=lambda call:True)
def data(call):
    if call.message:
        if call.data == '0':
            bot.send_message(call.message.chat.id, '/Приветствие/')
        elif call.data == '1':
            bot.send_message(call.message.chat.id, '/Прощание/')
        elif call.data == '2':
            bot.send_message(call.message.chat.id, '/Что нибудь ещё/')


#weather
@bot.message_handler(commands=['weather'])
def weather(message):
    driver.get("https://yandex.by/pogoda/minsk?utm_source=serp&utm_campaign=wizard&utm_medium=desktop&utm_content=wizard_desktop_main&utm_term=title")
    degrees = driver.find_element(By.XPATH, '//*[@id="content_left"]/div[2]/div[1]/div[4]/a/div/div[1]/span').text
    weather_now = driver.find_element(By.CLASS_NAME, "link__condition").text
    feels = driver.find_elements(By.CLASS_NAME, "term__value")
    feels = feeling[1].text
    bot.send_message(message.chat.id, "Сейчас в Минске " + degrees + " градусов\n" + weather_now + " \nОщущается как " + feels)


#search
@bot.message_handler(commands=["search"])
def search(message):
    msg = bot.send_message(message.chat.id, "Задайте Сети любой интересующий Вас вопрос:")     
    bot.register_next_step_handler(msg, y_search)

def y_search(message):
    bot.send_message(message.chat.id, "<i>Одну минуту...</i>", parse_mode='html')
    driver.get("https://yandex.by/search/?text=" + message.text)
    sleep(2)
    sites = driver.find_elements(By.CLASS_NAME, "organic__url")
    for i in range(len(sites)):
        if len(sites[i].get_attribute("href")) < 400:
            bot.send_message(message.chat.id, "<b>"+sites[i].text + "</b>\n" + sites[i].get_attribute("href"), parse_mode='html')
        if i > 4:
            break


#market
@bot.message_handler(commands=["market"])
def market(message):
    msg = bot.send_message(message.chat.id, "Какой товар вы ищете?")
    bot.register_next_step_handler(msg, y_market)

def y_market(message):
    product = message.text
    bot.send_message(message.chat.id, "Сейчас что-нибудь найдём...")
    driver.get("https://market.yandex.by")
    
    sleep(1)

    search_shop = driver.find_element(By.ID, "header-search")
    search_shop.send_keys(product)
    search_shop.submit()

    sleep(3)

    products = driver.find_elements(By.CLASS_NAME, "m4M-1")
    products_money = driver.find_elements(By.CLASS_NAME, "cia-cs")
    products_image = driver.find_elements(By.CLASS_NAME, "iqmYz")
    print(len(products))
    print(len(products_money))
    print(len(products_image))
    for i in range(len(products)):
        name_p = products[i].text
        money_p = products_money[i].text
        img_p = products_image[i].get_attribute("src")
        bot.send_photo(message.chat.id, img_p, caption="<b>" +name_p + "\n" + "Цена: " + money_p + "</b>", parse_mode='html')
        if i > 3:
            break
    if len(products) == 0:
        bot.send_message(message.chat.id, "Такого товара нет в нашей базе")


#prog_lang
@bot.message_handler(commands=["prog_lang"])
def prog_lang(message):
    bot.send_message(message.chat.id, "Топ языков🔝...)")
    driver.get("https://tiobe.com/tiobe-index/")

    sleep(1)

    lang = driver.find_elements(By.XPATH, '//td[5]')
    langs_list = []
    for i in range(len(lang)):
        langs_list.append(str(i+1) + ". " + lang[i].text)
        if i == 14:
            break
    langs = '\n'.join(langs_list)
    bot.send_message(message.chat.id, langs)


#youtube
@bot.message_handler(commands=["youtube"])
def youtube(message):
    msg = bot.send_message(message.chat.id, "Введите название желаемого видео")
    bot.register_next_step_handler(msg, youtube_search)

def youtube_search(message):
    driver.get("https://www.youtube.com/results?search_query=" + message.text)

    sleep(3)

    videos = driver.find_elements(By.ID, "video-title")
    bot.send_message(message.chat.id, "Сейчас постараюсь найти...⚡️")
    i = 0
    for video in videos:
        i += 1
        bot.send_message(message.chat.id, video.get_attribute("href"))
        if i > 4:
            break


#Реализовать
#subscribers
@bot.message_handler(commands=["subscribers"])
def subscribers(message):
    bot.send_message(message.chat.id, "Не забудь поблагодарить своих подписчиков! \n<i>Канал можно изменить в настройках⚙️</i>", parse_mode='html')
    channel = "https://www.youtube.com/channel/....."
    driver.get(channel)

    sleep(1)

    sub_len = driver.find_element(By.ID, "subscriber-count").text
    bot.send_message(message.chat.id, "У тебя сейчас <b>" + sub_len+"</b>", parse_mode='html')


#games
@bot.message_handler(commands=["games"])
def games(message):
    bot.send_message(message.chat.id, "🎮Давай посмотрим на 5 новых классных игр")
    driver.get("https://iwantgames.ru/newgames-pc/")
    games = driver.find_elements(By.TAG_NAME, "h2")
    games_date = driver.find_elements(By.CLASS_NAME, "date")
    games_img = driver.find_elements(By.CLASS_NAME, "attachment-game")
    for i in range(len(games)):
        name_g = games[i].text
        date_g = games_date[i].text
        img_g = games_img[i].get_attribute("src")
        bot.send_photo(message.chat.id, img_g, caption="<b>" + name_g + "</b>\n<i>" + date_g + "</i>",parse_mode="html")
        if i > 3:
            break


#films
@bot.message_handler(commands=['films'])
def films(message):
    bot.send_message(message.chat.id, "Отправляю новинки фильмов")
    driver.get("https://msk.kinoafisha.info/movies/")

    sleep(1)

    films_names = driver.find_elements(By.CLASS_NAME, "movieItem_title")
    films_images = driver.find_elements(By.CLASS_NAME, "movieItem_poster")
    for i in range(len(films_names)):
        bot.send_photo(message.chat.id, films_images[i].get_attribute("src"), caption=films_names[i].text)
        if i == 5:
            break


#math
@bot.message_handler(commands=['math'])
def math(message):
    global num
    first = random.randint(0, 300)
    second = random.randint(0, 300)
    pl_min = random.randint(0,1)
 
    if pl_min == 0:
        pl_min = "+"
    if pl_min == 1:
        pl_min = "-"
 
    msg = bot.send_message(message.chat.id, "Итак...:\n" + str(one_num) + " "+ pl_min + " " + str(two_num))
    bot.register_next_step_handler(msg, right)
    if pl_min == 0:
        num = one_num + two_num
    else:
        num = one_num - two_num
    print(num)
    
def right(message):
    try:
        if int(message.text) == num:
            bot.send_message(message.chat.id, "Правильно!✅") 
        else:
            bot.send_message(message.chat.id, "Не правильно❌")
    except:
        bot.send_message(message.chat.id, "Ёще раз🤖!!!, /math") 





bot.polling()