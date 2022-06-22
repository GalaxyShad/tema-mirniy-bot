import os
import discord
import random 
import time
import datetime
import requests

from man_of_day import ManOfDay   # Волк дня
from case_sys import CaseMgr     # Открытие кейсов
from thief_sys import *

from bs4 import BeautifulSoup

from private_stuff import TOKEN, CREATOR_ID

DEBUG = False

# === Константы ===
QUOTES_URL = "https://socratify.net/quotes"  # Сайт с цитатами

DAY_WOLF_PATH = "wolf_of_day\\"
THIEF_PATH = "thiefs\\"

CASE_COST = 50              # Цена кейсов
WOLF_DAY_REWARD = 125       # Награда волку дня
TEN_WOLF_DAY_REWARD = 500   # Награда за 10 становление волком дня

# === Варианты сообщений ===
# Cообщения для волка дня
MSGS_WOLF = [
    [
        'ВЕЧЕР В ХАТУ!', 
        'Ща поищем...',
        'Волки начали поиск!',
        'Скидадл-скидудл',
        'Запускаем шарманку...',
        'Ну что, кто же лютый волчара?',
        'А.У.Ф бомба сброшена! Все в укрытие...',
        'Wolf.exe activated...',
        'Посмотрим...'
    ],
    [
        'Идет поиск...',
        'Проверка ваших аккаунтов на pornhub...',
        'Чекаем историю вашего браузера...',
        'Сканирование сохраненных фотографий...',
        'Смотрим ваши библиотеки Steam...',
        'Звоним президенту...',
        'Советуемся с братками...'
    ],
    
    [
        'Итак, что тут у нас?',
        'Опа!',
        'ОГО-ГО',
        'Едрить-колотить!',
        'Ахуеть!',
        'Ля!',
        'Нихуя се!'
    ],
    [
        'Лютый! - ',
        'Мои поздравления! Ты настоящий пацан - ',
        'Стоять! Не двигаться! Вы объявлены оффником дня, ',
        'Кто бы мог подумать, но волчара дня — ',
        'Вжух! Ты волчара, ',
        'Что? Где? Когда? А ты волчара дня — '
    ]
]
# Ответы на АУЕ
MSGS_AYE = [ 
    'Воистину АУЕ, брат', 
    'АУЕ', 
    'АУЕ, брат', 
    'ЕУА', 
    'УАЕ', 
    'Реально, АУЕ', 
    'Арестантский Уклад Един',
    'А. У. Е',
    'АУЕ, бродяги',
    'Ауе, жизнь бобрам',
    'Ауе, жизнь ворам',
    'Ауе. Ауе? Ауе!',
    'Всегда АУЕ, брат',
    'Аууууууууууууууе',
    'Ииииууу АУЕ ес же',
    'Ааааааааа Ууууууууу ЕЕЕееееее',
    'Ае Ауе',
    'Ауе е е ее',
    'Ауе когда ауе',
    'Без ауе и ауе не ауе', 
]
# Ответы на Кто
MSGS_WHO = [
    'Ну я.',
    'Я',
    'Я кнш',
    'Я, бля',
    'Кнш Я',
    'Не я',
    'Точно не я',
    'Ну давай я',
    'Допустим я',
    'А Никто нахуй',
    'Кто-то',
]

# Смайлы для обозначения качества шмоток кейсов
DROP_SMILES = [
    ':blue_square:', 
    ':purple_square:', 
    ':small_red_triangle_down:', 
    ':red_square:', 
    ':yellow_square:'
]

# === Переменные ===
client = discord.Client()

msg = []  # Принимаемое сообщение

cur_date = datetime.datetime.now()

is_case_opening = False
case_spam_counter = 0


@client.event
async def on_ready():
    print('Залогинен, как {0.user}'.format(client))
    if not os.path.exists(DAY_WOLF_PATH):
        os.mkdir(DAY_WOLF_PATH)
    if not os.path.exists(THIEF_PATH):
        os.mkdir(THIEF_PATH)


@client.event
async def on_message(message):
    msg = message.content.lower().split()

    # Закрепление сообщения с редким дропом
    if message.author == client.user:
        if (len(message.embeds) != 0):
            emb = message.embeds[0]
            if (emb.title[1] == 'y' or emb.title[1] == 'r'):
                await message.pin()
        return

    # Проверка, что мы находимся в беседе
    if DEBUG and (message.guild != None or message.author.id != CREATOR_ID):
        return

    if len(msg) == 0:
        return

    # чеиз [парам 1] [парам 2] ... [парам n] - выбирает один из вариантов, 
    # перечисленных через пробел
    if msg[0] == 'чеиз':
        if len(msg) == 1:
            await message.channel.send('[:no_entry: Ошибка] Не указано ни одного варианта!')
            return

        if len(msg) == 2:
            await message.channel.send('[:no_entry: Ошибка] Гениально, на 1 вариант делать прокрутку.')
            return
        
        msg.remove('чеиз')
        await message.channel.send('Хм... Дайте подумать... :thinking:')
        time.sleep(4)
        await message.channel.send(f'Мой вариант - "{random.choice(msg)}" :wink:')
        return

    # сервертайм - выводит текущее время сервера
    if msg[0] == 'сервертайм':
        cur_date = datetime.datetime.now()
        await message.channel.send(f'{cur_date.hour:02}:{cur_date.minute:02} {cur_date.day}.{cur_date.month}.{cur_date.year}')
        return

    # инфа/вероятность/шанс/процент - выводит рандомное число от 0 до 100
    if msg[0] == 'инфа' or msg[0] == 'вероятность' or msg[0] == 'шанс' or msg[0] == 'процент':
        val = random.randint(0, 100)
        if val == 100:
            val = ':100:'
        await message.channel.send(f'"{message.content}" :point_right:  {val}%')
        return

    # цитата - парсит и выводит рандомную цитату с сайта QUOTES_URL
    if msg[0] == 'цитата':
        html = requests.get(QUOTES_URL)
        if html.status_code != 200:
            await message.channel.send('[:no_entry: Ошибка] Сервер цитат недоступен!')
            return

        soup = BeautifulSoup(html.text, 'html.parser')

        quotes_classes = soup.find_all('a', class_='b-list-quote2__item-text js-quote-text')
        quote = random.choice([item.get_text() for item in quotes_classes])

        await message.channel.send('    _"'+quote.strip()+'"_:point_up_tone1::rose:')
        return

    # кейслист - выводит список всех кейсов
    if msg[0] == 'кейслист':
        await message.channel.send('Список доступных кейсов:\n' + CaseMgr.get_str_cases_names())
        return

    # кейдроп [название кейса] - выводит весь дроп из указанного кейса
    if msg[0] == 'кейсдроп':
        str_drop_list = CaseMgr.get_str_case_drop(msg[1])

        if str_drop_list == ValueError:
            await message.channel.send('[:no_entry: Ошибка] Нужно указать кейс! Список кейсов - "кейслист"')
            return

        await message.channel.send(str_drop_list)
        return

    # опенкейс [название кейса] - открывает указанный кейс,
    # если же кейс не указан, то откроет рандомный
    if msg[0] == 'опенкейс':
        # Проверка, вор ли пользователь...
        file_name = 'debug'
        if (message.guild != None and not DEBUG):
            file_name = str(message.guild.id)
        
        file_name = THIEF_PATH+file_name+'.txt'

        wd_code = vor_withdraw_from_balance(file_name, str(message.author.id), CASE_COST)
        if wd_code == 0:
            await message.channel.send(f'[:no_entry: Ошибка] {message.author.mention},' + \
                f'для использования этой комманды нужно завести кошелек вора. **Пиши: "темахелп" для вызова справки.**')
            return
        elif wd_code == 2:
            wallets = vor_get_all_wallets(file_name)
            await message.channel.send(f'Эй, {message.author.mention}, на твоем балансе недостаточно денег!\n' + \
                f':credit_card: **Ваш баланс:** {wallets[str(message.author.id)]} руб.')
            return

        global is_case_opening
        global case_spam_counter

        is_case_opening = True

        case_name = 'random'
        if len(msg) != 1:
            await message.channel.send('Рандомный выбор кейса.')
            case_name = msg[1]

        cool = CaseMgr.open_case(case_name)
        drop = cool[0]
        if (type(drop) == int):
            if (drop == -1):
                await message.channel.send(f'Эй, {message.author.mention}, такого кейса не существует!\n' + \
                    'Пиши "кейслист", чтобы узнать список доступных кейсов.')
                is_case_opening = False
                return
            else:
                await message.channel.send(f'[:no_entry: Ошибка] {message.author.mention},' + \
                    f'превышено количество запросов на сервер! Попробуйте еще раз через {drop} минут(ы).')
                is_case_opening = False
                return

        
        if (case_name == "random"):
            await message.channel.send(f'Открытие рандомного кейса для {message.author.mention} за {CASE_COST} руб. ...')
        else:
            await message.channel.send(f'Открытие кейса "{case_name.upper()}" для {message.author.mention} за {CASE_COST} руб. ...')

        # Руссификаця качества
        quality = ''

        if drop.quality == 'Factory New':
            quality = 'Прямо с завода'
        elif drop.quality == 'Minimal Wear':
            quality = 'Немного поношенное'
        elif drop.quality == 'Field-Tested':
            quality = 'После полевых испытаний'
        elif drop.quality == 'Well-Worn':
            quality = 'Поношенное'
        elif drop.quality == 'Battle-Scarred':
            quality = 'Закаленное в боях'

        color = [0x45abfe, 0x792cb6, 0xdc10d0, 0xc93330, 0xffe000]
        cost = int(float(drop.cost.replace(",", '.').replace("pуб.", '')))+1

        emb = discord.Embed(title=f'{DROP_SMILES[drop.color]} {drop.name} {DROP_SMILES[drop.color]}', color=color[drop.color])
        emb.add_field(name='Качество:', value=quality)
        emb.add_field(name=':dollar: Цена:', value=(str(cost) + ' руб.'))
        # if drop.color < 3:
        #     emb.set_thumbnail(url=drop.img)
        # else: 
        #     emb.set_image(url=drop.img)
        
        vor_add_to_balance(file_name, str(message.author.id), cost)
        wallets = vor_get_all_wallets(file_name)
        await message.channel.send(f':fire: Поздравляем, {message.author.mention}!!! :fire:\n' + \
            f':credit_card: **Ваш текущий баланс:** {wallets[str(message.author.id)]} руб.', embed=emb, 
            file=discord.File(f'cases\\{cool[1]}\\{drop.name.replace(" | ", "_")}.png') )  #, file=discord.File(drop.img, 'drop.png'))
        is_case_opening = False
        return 

    # волкрег - регистрирует пользователя в рулетке
    if msg[0] == 'волкрег':
        file_name = 'debug'
        if (message.guild != None and not DEBUG):
            file_name = str(message.guild.id)

        if ManOfDay.reg(DAY_WOLF_PATH+file_name+'.txt', str(message.author.id)):
            await message.channel.send(f'{message.author.mention}, регистрация прошла успешно!')
        else:
            await message.channel.send(f'Лее, {message.author.mention}, ты уже в игре!')

        return

    # волкдня - рандомно выбирает зарегистрированного пользователя
    if msg[0] == 'волкдня':
        file_name = 'debug'
        if (message.guild != None and not DEBUG):
            file_name = str(message.guild.id)

        user = ManOfDay.get(DAY_WOLF_PATH+file_name+'.txt')

        if user == None:
            await message.channel.send(f'[:no_entry: Ошибка] Сначала нужно зарегистрироваться! **Пиши - волкрег.**')
            return 

        if user[0] == '!':
            await message.channel.send(':fire: Волк дня - ' + '<@' + user + '> :fire:')
            return

        await message.channel.send('**' + random.choice(MSGS_WOLF[0]) + '**')
        time.sleep(2)
        await message.channel.send('**' + random.choice(MSGS_WOLF[1]) + '**')
        time.sleep(2)
        await message.channel.send('**' + random.choice(MSGS_WOLF[2]) + '**')
        time.sleep(2)
        await message.channel.send('**' + random.choice(MSGS_WOLF[3]) + '<@' + user +'>' + '**')

        # Добавляем денег участникам воров
        reward = WOLF_DAY_REWARD

        # Награда за юбилейное становление волком дня
        top = ManOfDay.get_top(DAY_WOLF_PATH+file_name+'.txt')
        if top[user] % 10 == 0:
            reward = TEN_WOLF_DAY_REWARD
            await message.channel.send(f':fire::partying_face: **Поздравляем, <@{user}>! Вы достигли юбилейного значения, награда зачислена на ваш счет!** :partying_face::fire:')
                
        if vor_add_to_balance(THIEF_PATH+file_name+'.txt', user, reward) == 1:
            await message.channel.send(f':money_with_wings: <@{user}> Ваш баланс был пополнен на {reward} руб!')

        return
    
    # волкдня - выводит топ участников рулетки
    if msg[0] == 'волктоп':
        file_name = 'debug'
        if (message.guild != None and not DEBUG):
            file_name = str(message.guild.id)

        users = ManOfDay.get_top(DAY_WOLF_PATH+file_name+'.txt')

        if users == None:
            await message.channel.send(f'[:no_entry: Ошибка] Сначала нужно провести розыгрыш! **Пиши - волкдня.**')
            return

        string = ''
        i = 0
        for user in users:   
            smile = ''
            if i == 0:
                smile = ':smiling_imp:'
            elif i == 1:
                smile = ':sunglasses:'
            elif i == 2:
                smile = ':call_me_tone1:'
            else: 
                smile = '      '
            string += smile + ' ' + str(i+1) + '. <@' + user + '> - ' + str(users[user]) + ' раз(а)\n'
            i += 1
                
        await message.channel.send(string)
    
    # воррег - заводит виртуальный кошелек для пользователя
    if msg[0] == 'воррег':
        file_name = 'debug'
        if (message.guild != None and not DEBUG):
            file_name = str(message.guild.id)
        
        file_name = THIEF_PATH+file_name+'.txt'

        if vor_reg(file_name, str(message.author.id)):
            await message.channel.send(f'{message.author.mention}, \
                регистрация прошла успешно!\n:credit_card: **Ваш баланс:** {START_THIEF_BALANCE} руб.')
            return
        else:
            await message.channel.send(f'Лее, {message.author.mention}, ты уже в игре!')
            return

    # воррег - отображает топ кошельков игроков
    if msg[0] == 'ворбаланс' or msg[0] == 'вортоп':
        file_name = 'debug'
        if (message.guild != None and not DEBUG):
            file_name = str(message.guild.id)
        
        file_name = THIEF_PATH+file_name+'.txt'
        wallets = vor_get_all_wallets(file_name)

        if wallets == None:
            await message.channel.send(f'[:no_entry: Ошибка] Не найдено ни одного кошелька! **Чтобы завести кошелек, пиши - воррег.**')
            return
            
        # Великая сортировка от Максима Заказчика
        wallets = {k: v for k, v in sorted(wallets.items(),
               key=lambda item: item[1])[::-1]}

        ans = 'Топ воров за все время:\n'
        i = 0
        for wallet in wallets:
            ans += '**' + str(i+1) + '.**  :credit_card: <@' + wallet + '> - ' + str(wallets[wallet]) + ' руб.\n'
            i += 1
    
        await message.channel.send(ans)
        
    # Тригеры на слова
    if msg[0] == 'так' and msg[1] == 'но':
        await message.channel.send('хуйНО блять')
        return
    if msg[0] == 'по' and msg[1] == 'кайфу':
        await message.channel.send('Внатуре по кайфу ☝🏻')
        return
    if msg[0] == 'ауф':
        await message.channel.send('АУФ, брат :rose:☝🏻')
        return
    if msg[0] == 'похуй':
        await message.channel.send('ВООБЩЕ ПОЕБАТЬ')
        return
    if ('ауе' in msg) or ('ауе!' in msg) or ('ауе?' in msg) or ('ауе.' in msg):
        await message.channel.send(random.choice(MSGS_AYE) + '! 😈☝🏻')
        return
    if ('кто' in msg or 'кто?' in msg):
        await message.channel.send(random.choice(MSGS_WHO) + ':wolf:')
        return

    # Хелпа
    if msg[0] == 'темахелп':
        answer = \
        'Всем участникам беседы салам!\n' + \
        'Бот тригерится на слова: **"ауе"**, **"ауф"**, **"похуй"**, **"кто"**.\n' + \
        'А также на фразы **"так но"** и **"по кайфу"**\n' + \
        'Че по функциям, то:\n' + \
        '   :small_orange_diamond: **"чеиз [парам 1] [парам 2] ... [парам n]"** - выбирает один из вариантов, перечисленных через пробел.\n' + \
        '   :small_orange_diamond: **"сервертайм"** - выводит текущее время сервера (нужна тут для проверки работоспособности бота).\n' + \
        '   :small_orange_diamond: **"инфа/вероятность/шанс/процент [сообщение]"** - выводит рандомное число от 0 до 100.\n' + \
        '   :small_orange_diamond: **"цитата"** - выводит рандомную цитату.\n' + \
        '   ----------\n' + \
        f'   :small_orange_diamond: **"воррег"** - регистрация кошелька Вора с изначальной суммой - {START_THIEF_BALANCE} руб. Заработать деньги можно путем награды за должность Волк Дня или испытывая удачу открытием кейсов за {CASE_COST} руб.\n' + \
        '   :small_orange_diamond: **"ворбаланс/вортоп"** - выводит баланс всех "Воров", начиная с самого богатого.\n' + \
        '   ----------\n' + \
        f'   :small_orange_diamond: **"опенкейс [кейс]"** (только для тех у кого есть кошелек Вора) - открывает кейс из CS:GO, если же кейс не указан, то откроет рандомный. Если вы Вор, то цена открытия кейса - {CASE_COST} руб. Шансы выпадения предметов: Нож - 1%, Красное - 2%, Розовое - 5%, Фиолетовое - 12%, Синька - 80%.\n' + \
        '   :small_orange_diamond: **"кейслист"** - выводит список всех доступных кейсов из CS:GO.\n' + \
        '   :small_orange_diamond: **"кейсдроп [кейс]"** - выводит весь дроп который может выпасть из указанного кейса.\n' + \
        '   ----------\n' + \
        '   :small_orange_diamond: **"волкрег"** - зарегистрироваться в рулетке, определяющей настоящего B♂ss ♂f the gym дня :sunglasses:.\n' + \
        '   :small_orange_diamond: **"волктоп"** - выводит топ волков дня.\n' + \
        f'   :small_orange_diamond: **"волкдня"** - определяет волка дня, если вы Вор и Волк дня, то получите награду - {WOLF_DAY_REWARD} руб.\n'
        await message.channel.send(answer)

client.run(TOKEN)  # Запуск бота
