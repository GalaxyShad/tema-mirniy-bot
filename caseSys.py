
from bs4 import BeautifulSoup

import json
import random 
import time
import requests

# Ссылки на торговую площадку стима
STEAM_URL       = "http://steamcommunity.com/market/listings/730/" # Торговая площадка
STEAM_COST_URL  = "http://steamcommunity.com/market/priceoverview" # Стоимость

CSGO_ID = 730
COUNTRY_RUSSIA = 5

# Изношенность скина
SKINS_QUALITY = [
    'Factory New', 
    'Minimal Wear', 
    'Field-Tested', 
    'Well-Worn', 
    'Battle-Scarred'
    ]

# Виды ножей
CASES_DROP_KNIFE_TYPE = [
    'Bayonet',
    'Butterfly Knife',
    'Classic Knife',
    'Falchion Knife',
    'Flip Knife',
    'Gut Knife',
    'Huntsman Knife',
    'Karambit',
    'M9 Bayonet',
    'Shadow Daggers',
    'Bowie Knife',
    'Ursus Knife',
    'Navaja Knife',
    'Stiletto Knife',
    'Talon Knife',
    'Nomad Knife',
    'Skeleton Knife',
    'Survival Knife',
    'Paracord Knife']

# Ножи
CASES_DROP_KNIFES = [
    'Stained',
    'Slaughter',
    'Fade',
    'Case Hardened',
    'Crimson Web',
    'Scorched',
    'Marble Fade',
    'Doppler',
    'Tiger Tooth',
    'Damascus Steel',
    'Lore',
    'Night']

# Кейсы
CASES = {
    'фрактал': (
        ('Negev | Ultralight', 'P2000 | Gnarled', 'SG 553 | Ol\' Rusty',
         'SSG 08 | Mainframe 001', 'P250 | Cassette', 'P90 | Freight', 'PP-Bizon | Runic'),

        ('MAG-7 | Monster Call', 'Tec-9 | Brother', 'MAC-10 | Allure',
         'Galil AR | Connexion', 'MP5-SD | Kitbash'),

        ('M4A4 | Tooth Fairy', 'Glock-18 | Vogue', 'XM1014 | Entombed'),

        ('Desert Eagle | Printstream', 'AK-47 | Legion of Anubis'),
    ),
    'спектрум': (
        ('PP-Bizon | Jungle Slipstream', 'SCAR-20 | Blueprint', 'Desert Eagle | Oxide Blaze',
            'Five-SeveN | Capillary', 'MP7 | Akoben', 'P250 | Ripple', 'Sawed-Off | Zander'),

        ('Galil AR | Crimson Tsunami', 'M249 | Emerald Poison Dart',
         'MAC-10 | Last Dive', 'UMP-45 | Scaffold', 'XM1014 | Seasons'),

        ('AWP | Fever Dream', 'CZ75-Auto | Xiangliu', 'M4A1-S | Decimator'),

        ('AK-47 | Bloodsport', 'USP-S | Neo-Noir')
    ),
    'спектрум2': (     
        ('Sawed-Off | Morris',
        'AUG | Triqua',
        'G3SG1 | Hunter',
        'Glock-18 | Off World',
        'MAC-10 | Oceanic',
        'Tec-9 | Cracked Opal',
        'SCAR-20 | Jungle Slipstream'),
        ('MP9 | Goo',
        'SG 553 | Phantom',
        'CZ75-Auto | Tacticat',
        'UMP-45 | Exposure',
        'XM1014 | Ziggy'),
        ('PP-Bizon | High Roller',
        'M4A1-S | Leaded Glass',
        'R8 Revolver | Llama Cannon'),
        ('AK-47 | The Empress',
        'P250 | See Ya Later')
    ),
    'горизонт': (
        ('AUG | Amber Slipstream',
         'Dual Berettas | Shred',
         'Glock-18 | Warhawk',
         'MP9 | Capillary',
         'P90 | Traction',
         'R8 Revolver | Survivalist',
         'Tec-9 | Snek-9'),
        ('CZ75-Auto | Eco',
         'G3SG1 | High Seas',
         'Nova | Toy Soldier',
         'AWP | PAW',
         'MP7 | Powercore'),
        ('M4A1-S | Nightmare',
         'Sawed-Off | Devourer',
         'FAMAS | Eye of Athena'),
        ('AK-47 | Neon Rider',
         'Desert Eagle | Code Red')
    ),
    'феникс': (
        ('UMP-45 | Corporal',
        'Negev | Terrain',
        'Tec-9 | Sandstorm',
        'MAG-7 | Heaven Guard'),
        ('MAC-10 | Heat',
        'SG 553 | Pulse',
        'FAMAS | Sergeant',
        'USP-S | Guardian'),
        ('AK-47 | Redline',
        'P90 | Trigon',
        'Nova | Antique'),
        ('AWP | Asiimov',
        'AUG | Chameleon')
    ),
    'фальшион': (
        ('Galil AR | Rocket Pop',
        'Glock-18 | Bunsen Burner',
        'Nova | Ranger',
        'P90 | Elite Build',
        'UMP-45 | Riot',
        'USP-S | Torque'),
        ('FAMAS | Neural Net',
        'M4A4 | Evil Daimyo',
        'MP9 | Ruby Poison Dart',
        'Negev | Loudmouth',
        'P2000 | Handgun'),
        ('CZ75-Auto | Yellow Jacket',
        'MP7 | Nemesis',
        'SG 553 | Cyrex'),
        ('AK-47 | Aquamarine Revenge',
        'AWP | Hyper Beast')
    ),
    'револьвер': (
        ('R8 Revolver | Crimson Web',
        'AUG | Ricochet',
        'Desert Eagle | Corinthian',
        'P2000 | Imperial',
        'Sawed-Off | Yorick',
        'SCAR-20 | Outbreak'),
        ('PP-Bizon | Fuel Rod',
        'Five-SeveN | Retrobution',
        'Negev | Power Loader',
        'SG 553 | Tiger Moth',
        'Tec-9 | Avalanche',
        'XM1014 | Teclu Burner'),
        ('AK-47 | Point Disarray',
        'G3SG1 | The Executioner',
        'P90 | Shapewood'),
        ('M4A4 | Royal Paladin',
        'R8 Revolver | Fade')
    ),
    'призма': (
        ('FAMAS | Crypsis',
        'AK-47 | Uncharted',
        'MAC-10 | Whitefish',
        'Galil AR | Akoben',
        'MP7 | Mischief',
        'P250 | Verdigris',
        'P90 | Off World'),
        ('AWP | Atheris',
        'Tec-9 | Bamboozle',
        'Desert Eagle | Light Rail',
        'MP5-SD | Gauss',
        'UMP-45 | Moonrise'),
        ('R8 Revolver | Skull Crusher',
        'AUG | Momentum',
        'XM1014 | Incinegator'),
        ('Five-SeveN | Angry Mob',
        'M4A4 | The Emperor')
    ),
    'призма2': (
        ('AUG | Tom Cat',
        'AWP | Capillary',
        'CZ75-Auto | Distressed',
        'Desert Eagle | Blue Ply',
        'MP5-SD | Desert Strike',
        'Negev | Prototype',
        'R8 Revolver | Bone Forged'),
        ('P2000 | Acid Etched',
        'Sawed-Off | Apocalypto',
        'SCAR-20 | Enforcer',
        'SG 553 | Darkwing',
        'SSG 08 | Fever Dream'),
        ('AK-47 | Phantom Disruptor',
        'MAC-10 | Disco Tech',
        'MAG-7 | Justice'),
        ('M4A1-S | Player Two',
        'Glock-18 | Bullet Queen')
    ),
    'хрома': (
        ('Glock-18 | Catacombs',
        'M249 | System Lock',
        'MP9 | Deadly Poison',
        'SCAR-20 | Grotto',
        'XM1014 | Quicksilver'),
        ('Dual Berettas | Urban Shock',
        'Desert Eagle | Naga',
        'MAC-10 | Malachite',
        'Sawed-Off | Serenity'),
        ('AK-47 | Cartel',
        'M4A4 | 龍王 (Dragon King)',
        'P250 | Muertos'),
        ('AWP | Man-o\'-war',
        'Galil AR | Chatterbox')
    ),
    'хрома2': (
        ('AK-47 | Elite Build',
        'MP7 | Armor Core',
        'Desert Eagle | Bronze Deco',
        'P250 | Valence',
        'Negev | Man-o\'-war',
        'Sawed-Off | Origami'),
        ('AWP | Worm God',
        'MAG-7 | Heat',
        'CZ75-Auto | Pole Position',
        'UMP-45 | Grand Prix'),
        ('Five-SeveN | Monkey Business',
        'Galil AR | Eco',
        'FAMAS | Djinn'),
        ('M4A1-S | Hyper Beast',
        'MAC-10 | Neon Rider')
    ),
    'хрома3': (
        ('Dual Berettas | Ventilators',
        'G3SG1 | Orange Crash',
        'M249 | Spectre',
        'MP9 | Bioleak',
        'P2000 | Oceanic',
        'Sawed-Off | Fubar',
        'SG 553 | Atlas'),
        ('CZ75-Auto | Red Astor',
        'Galil AR | Firefight',
        'SSG 08 | Ghost Crusader',
        'Tec-9 | Re-Entry',
        'XM1014 | Black Tie'),
        ('AUG | Fleet Flock',
        'P250 | Asiimov',
        'UMP-45 | Primal Saber'),
        ('PP-Bizon | Judgement of Anubis',
        'M4A1-S | Chantico\'s Fire')
    ),
    'денжерзон': (
        ('MP9 | Modest Threat',
        'Glock-18 | Oxide Blaze',
        'Nova | Wood Fired',
        'M4A4 | Magnesium',
        'Sawed-Off | Black Sand',
        'SG 553 | Danger Close',
        'Tec-9 | Fubar'),
        ('G3SG1 | Scavenger',
        'Galil AR | Signal',
        'MAC-10 | Pipe Down',
        'P250 | Nevermore',
        'USP-S | Flashback'),
        ('UMP-45 | Momentum',
        'Desert Eagle | Mecha Industries',
        'MP5-SD | Phosphor'),
        ('AK-47 | Asiimov',
        'AWP | Neo-Noir')
    ),
    'cs20': (
        ('Dual Berettas | Elite 1.6',
        'Tec-9 | Flash Out',
        'MAC-10 | Classic Crate',
        'MAG-7 | Popdog',
        'SCAR-20 | Assault',
        'FAMAS | Decommissioned',
        'Glock-18 | Sacrifice'),
        ('M249 | Aztec',
        'MP5-SD | Agent',
        'Five-SeveN | Buddy',
        'P250 | Inferno',
        'UMP-45 | Plastique'),
        ('MP9 | Hydra',
        'P90 | Nostalgia',
        'AUG | Death by Puppy'),
        ('AWP | Wildfire',
        'FAMAS | Commemoration')
    ),
    'гамма': (
        ('Five-SeveN | Violent Daimyo',
        'MAC-10 | Carnivore',
        'Nova | Exo',
        'P250 | Iron Clad',
        'PP-Bizon | Harvester',
        'SG 553 | Aerial',
        'Tec-9 | Ice Cap'),
        ('AUG | Aristocrat',
        'AWP | Phobos',
        'P90 | Chopper',
        'R8 Revolver | Reboot',
        'Sawed-Off | Limelight'),
        ('M4A4 | Desolate Space',
        'P2000 | Imperial Dragon',
        'SCAR-20 | Bloodsport'),
        ('Glock-18 | Wasteland Rebel',
        'M4A1-S | Mecha Industries')
    ),
    'гамма2': (
        ('CZ75-Auto | Imprint',
        'Five-SeveN | Scumbria',
        'G3SG1 | Ventilator',
        'Negev | Dazzle',
        'P90 | Grim',
        'UMP-45 | Briefing',
        'XM1014 | Slipstream'),
        ('Desert Eagle | Directive',
        'Glock-18 | Weasel',
        'MAG-7 | Petroglyph',
        'SCAR-20 | Powercore',
        'SG 553 | Triarch'),
        ('AUG | Syd Mead',
        'MP9 | Airlock',
        'Tec-9 | Fuel Injector'),
        ('AK-47 | Neon Revolution',
        'FAMAS | Roll Cage') 
    ),
    'клатч': (
        ('PP-Bizon | Night Riot',
        'Five-SeveN | Flame Test',
        'MP9 | Black Sand',
        'P2000 | Urban Hazard',
        'R8 Revolver | Grip',
        'SG 553 | Aloha',
        'XM1014 | Oxide Blaze'),
        ('Glock-18 | Moonrise',
        'Negev | Lionfish',
        'Nova | Wild Six',
        'MAG-7 | SWAG-7',
        'UMP-45 | Arctic Wolf'),
        ('AUG | Stymphalian',
        'AWP | Mortis',
        'USP-S | Cortex'),
        ('M4A4 | Neo-Noir',
        'MP7 | Bloodsport')
    ),
    'shadow': (
        ('Dual Berettas | Dualing Dragons',
        'FAMAS | Survivor Z',
        'Glock-18 | Wraiths',
        'MAC-10 | Rangeen',
        'MAG-7 | Cobalt Core',
        'SCAR-20 | Green Marine',
        'XM1014 | Scumbria'),
        ('Galil AR | Stone Cold',
        'M249 | Nebula Crusader',
        'MP7 | Special Delivery',
        'P250 | Wingshot'),
        ('AK-47 | Frontside Misty',
        'G3SG1 | Flux',
        'SSG 08 | Big Iron'),
        ('M4A1-S | Golden Coil',
        'USP-S | Kill Confirmed') 
    ),
    'wildfire': (
        ('PP-Bizon | Photic Zone',
        'Dual Berettas | Cartel',
        'MAC-10 | Lapis Gator',
        'SSG 08 | Necropos',
        'Tec-9 | Jambiya',
        'USP-S | Lead Conduit'),
        ('FAMAS | Valence',
        'Five-SeveN | Triumvirate',
        'Glock-18 | Royal Legion',
        'MAG-7 | Praetorian',
        'MP7 | Impire'),
        ('AWP | Elite Build',
        'Desert Eagle | Kumicho Dragon',
        'Nova | Hyper Beast'),
        ('AK-47 | Fuel Injector',
        'M4A4 | The Battlestar')
    ),
    'vanguard': (
        ('G3SG1 | Murky',
        'MAG-7 | Firestarter',
        'MP9 | Dart',
        'Five-SeveN | Urban Hazard',
        'UMP-45 | Delusion'),
        ('Glock-18 | Grinder',
        'M4A1-S | Basilisk',
        'M4A4 | Griffin',
        'Sawed-Off | Highwayman'),
        ('P250 | Cartel',
        'SCAR-20 | Cardiac',
        'XM1014 | Tranquility'),
        ('AK-47 | Wasteland Rebel',
        'P2000 | Fire Elemental') 
    ),
    'клык': (
        ('CZ75-Auto | Vendetta',
        'P90 | Cocoa Rampage',
        'G3SG1 | Digital Mesh',
        'Galil AR | Vandal',
        'P250 | Contaminant',
        'M249 | Deep Relief',
        'MP5-SD | Condition Zero'),
        ('AWP | Exoskeleton',
        'Dual Berettas | Dezastre',
        'Nova | Clear Polymer',
        'SSG 08 | Parallax',
        'UMP-45 | Gold Bismuth'),
        ('Five-SeveN | Fairy Tale',
        'M4A4 | Cyber Security',
        'USP-S | Monster Mashup'),
        ('M4A1-S | Printstream',
        'Glock-18 | Neo-Noir')
    )}


def open_case(case_name):
    case_chance = random.randint(0, 100) # Шанс выпадения предмета
    case = CASES[case_name]

    quality  = random.choice(SKINS_QUALITY) # Определение изношенности
    str_skin = 'err'                        # Скин
    color    = 0                            # Редкость

    # - Значения из CSGO - #
    # Синие — 79.92%
    # Фиолетовые — 15.98%
    # Розовые — 3.2%
    # Красные — 0.64%
    # Золотые — 0.26%
    # -------------------- #

    # Смотрим, что выпало
    if case_chance <= 80: # Синька
        color = 0
        str_skin = random.choice(case[0])
    elif case_chance > 80 and case_chance <= 92: # Фиолетовое
        color = 1
        str_skin = random.choice(case[1]) 
    elif case_chance > 92 and case_chance <= 97: # Розовое
        color = 2
        str_skin = random.choice(case[2]) 
    elif case_chance > 97 and case_chance <= 99: # Красное
        color = 3
        str_skin = random.choice(case[3])
    else: # Желтое
        color = 4
        str_skin = f'★ ' + random.choice(CASES_DROP_KNIFE_TYPE) + ' | ' + random.choice(CASES_DROP_KNIFES)

    skin_request = str_skin + ' (' + quality + ')' # Итоговый аргумент для отправки запроса
        
    # Определение цены
    json_param = {"appid": CSGO_ID, 
                  "market_hash_name": skin_request, 
                  "currency": COUNTRY_RUSSIA}            # Аргументы для запроса цены
    cost_html = requests.get(STEAM_COST_URL, json_param) # Получаем страницу с ценой

    if (cost_html.status_code != 200): # Обработка ошибок
        print(f'Ошибка чтения html для цены.')
        print(skin_request)
        print(f'Код доступа: {cost_html.status_code}')
        return open_case()

    cost_json = json.loads(cost_html.text) # Получаем json

    if (cost_json == ValueError):  # Обработка ошибок
        print(f'Ошибка чтения JSON для цены: {skin_request}')
        return open_case()

    if not cost_json['lowest_price']: # Обработка ошибок
        print(f'Ошибка определения цены для: {skin_request}')
        print(cost_html.text)
        return open_case()

    cost = cost_json['lowest_price'] # Стоимость

    return Skin(str_skin, quality, cost, str_skin, color)

class CaseMgr:
    def get_str_cases_names():
        ans = ''
        for case in CASES.keys():
            ans += '📦 ' + case + ',\n'
        return ans

    def get_str_case_drop(case_name, smiles = ['😬','😃','😜','😎','⭐']):
        if (case_name not in CASES):
            return ValueError
        
        ans = ''
        for item in CASES[case_name].rare_drop:
            ans += smiles[0] + ' ' + item + '\n'
        for item in CASES[case_name].myth_drop:
            ans += smiles[1] + ' ' + item + '\n'
        for item in CASES[case_name].legend_drop:
            ans += smiles[2] + ' ' + item + '\n'
        for item in CASES[case_name].ancient_drop:
            ans += smiles[3] + ' ' + item + '\n'
        ans += smiles[4] + ' ★ или крайне редкий предмет!'
        
        return ans

    def open_case(case_name):
        if (case_name != "random" and case_name not in CASES):
            return -1

        global case_acces_time
        delta_time = int((time.time() - case_acces_time) // 60) # Время прошедшее с момента блокировки
        if (BAN_TIME - delta_time > 0):
            return (BAN_TIME - delta_time)
        
        if (case_name == "random"):
            list_case_names = list(CASES.keys())
            case_name = random.choice(list_case_names)

        skin = CASES[case_name].open_case()
        if (skin == "ERR_IP_BLOCKED"):
            case_acces_time = time.time()
            return BAN_TIME

        return [skin, case_name]
     






    

