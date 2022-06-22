import os
import io
from caseSys import *
from PIL import Image

skins_missing = []

if not os.path.exists("cases"):
    os.mkdir("cases")

if not os.path.exists("cases\\knifes"):
    os.mkdir("cases\\knifes")

f = open('cases\\knifes\\knifes.txt', 'w')

for str_skin_knife_type in CASES_DROP_KNIFE_TYPE:
    for str_skin_knife in CASES_DROP_KNIFES:
        f.write(str_skin_knife_type + '_' + str_skin_knife + '\n')
        print(str_skin_knife_type + '_' + str_skin_knife)
        for str_skin_quality in SKINS_QUALITY:
            str_skin = '★ ' + str_skin_knife_type + ' | ' + str_skin_knife

            qual_index = 0
            skin_request = str_skin + f' ({str_skin_quality})' # Итоговый аргумент для отправки запроса
                    
            str_skin_quality.replace(" ", '_')

            print('--' + str_skin_quality, end=' ')
            # Определение цены
            while True:
                json_param = {"appid": CSGO_ID, 
                              "market_hash_name": skin_request, 
                              "currency": COUNTRY_RUSSIA}            # Аргументы для запроса цены
                cost_html = requests.get(STEAM_COST_URL, json_param) # Получаем страницу с ценой

                if cost_html.status_code == 429:
                    print('Заблочили :(. Ждемс...')
                    time.sleep(300)
                    continue

                if cost_html.status_code != 200: # Если не нашли, значит стим заблочил наш IP, пишем ошибку
                    print(f'-1 Ошибка чтения html для цены. {cost_html.status_code}')
                    f.write('    ' + str_skin_quality + ' -1\n')
                    break
                

                cost_json = json.loads(cost_html.text) # Получаем json

                if (cost_json == ValueError):  # Обработка ошибок
                    print(f'-1 Ошибка чтения JSON для цены. {cost_html.status_code}')
                    f.write('    ' + str_skin_quality + ' -1\n')
                    break

                if not 'lowest_price' in cost_json: # Обработка ошибок
                    print(f'-1 Нет цены. {cost_html.status_code}')
                    f.write('    ' + str_skin_quality + ' -1\n')
                    break

                if not cost_json['lowest_price']: # Обработка ошибок
                    print(f'-1 Нет цены. {cost_html.status_code}')
                    f.write('    ' + str_skin_quality + ' -1\n')
                    break

                cost = int(float(cost_json['lowest_price'].replace(",", '.').replace("pуб.", '')))+1

                f.write('    ' + str_skin_quality + ' ' + str(cost) + '\n')
                print(cost)
                break
f.close()

# for str_skin_knife_type in CASES_DROP_KNIFE_TYPE:
#     for str_skin_knife in CASES_DROP_KNIFES:
#         str_skin = '★ ' + str_skin_knife_type + ' | ' + str_skin_knife

#         print('    > '+str_skin+'...')

#         qual_index = 0
#         skin_request = str_skin + f' ({SKINS_QUALITY[0]})' # Итоговый аргумент для отправки запроса
                
#         # Определение цены
#         while True:
#             html = requests.get(STEAM_URL + skin_request) # Получаем страницу из тороговой площадки
#             soup = BeautifulSoup(html.text, 'html.parser')  # Переводим ее в текст

#             div_img = soup.find('div', class_='market_listing_largeimage') # Ищем ссылку на картинку

#             if div_img == None: # Если не нашли, значит стим заблочил наш IP, пишем ошибку
#                 print(f'Ошибка загрузки картинки. {STEAM_URL + skin_request}')
#                 text = soup.find('div', {"id": "message"}) 

#                 if text != None:
#                     print(text.find('h3'))
#                     time.sleep(300)
#                 else:
#                     if qual_index >= 4:
#                         print("Увы :( Данный экземпляр отсутствует в продаже!")
#                         skins_missing.append(str_skin)
#                         break

#                     print("Нет в продаже!")
#                     qual_index += 1
#                     skin_request = str_skin + f' ({SKINS_QUALITY[qual_index]})' 
#                     print("Пробуем " + skin_request + "...")
#                 continue

#             url_img = div_img.find('img').get('src') # получаем ссылку на картинку

#             # Запись картинки в файл
#             pic = requests.get(url_img)
#             str_skin = str_skin.replace(' | ', '_')

#             img_bytes = io.BytesIO(pic.content)
#             img = Image.open(img_bytes)

#             img_bg = Image.open('gold.png')
#             img_bg.paste(img, (0, 0), img)
#             img_bg.save('cases\\knifes\\'+str_skin+'.png')

#             break




# print('С какого кейса продолжить?')
# continue_case = input()

# if not continue_case in CASES:
#     continue_case = '0'

# for case_name in CASES:
#     if continue_case != '0' and case_name != continue_case:
#         continue 

#     print(f'> Парсим кейс "{case_name}"...')

#     if not os.path.exists("cases\\"+case_name):
#         os.mkdir("cases\\"+case_name)

#     for i in range(4):
#         skins = []
#         img_bg = None
#         img_bg_str = ''
#         if i == 0:
#             skins = CASES[case_name].rare_drop
#             img_bg_str = 'blue.png'
#             print(f'  > Синька')
#         elif i == 1:
#             skins = CASES[case_name].myth_drop
#             img_bg_str = 'violet.png'
#             print(f'  > Фиолетовое')
#         elif i == 2:
#             skins = CASES[case_name].legend_drop
#             img_bg_str = 'pink.png'
#             print(f'  > Розовое')
#         elif i == 3:
#             skins = CASES[case_name].ancient_drop
#             img_bg_str = 'red.png'
#             print(f'  > Красное')

#         for str_skin in skins:
#             print('    > '+str_skin+'...')

#             qual_index = 0
#             skin_request = str_skin + f' ({SKINS_QUALITY[0]})' # Итоговый аргумент для отправки запроса
            
#             # Определение цены
#             while True:
#                 html = requests.get(STEAM_URL + skin_request) # Получаем страницу из тороговой площадки
#                 soup = BeautifulSoup(html.text, 'html.parser')  # Переводим ее в текст

#                 div_img = soup.find('div', class_='market_listing_largeimage') # Ищем ссылку на картинку

#                 if div_img == None: # Если не нашли, значит стим заблочил наш IP, пишем ошибку
#                     print(f'Ошибка загрузки картинки. {STEAM_URL + skin_request}')
#                     text = soup.find('div', {"id": "message"}) 

#                     if text != None:
#                         print(text.find('h3'))
#                         time.sleep(300)
#                     else:
#                         if qual_index >= 4:
#                             print("Увы :( Данный экземпляр отсутствует в продаже!")
#                             skins_missing.append(str_skin)
#                             break

#                         print("Нет в продаже!")
#                         qual_index += 1
#                         skin_request = str_skin + f' ({SKINS_QUALITY[qual_index]})' 
#                         print("Пробуем " + skin_request + "...")
#                     continue

#                 url_img = div_img.find('img').get('src') # получаем ссылку на картинку

#                 # Запись картинки в файл
#                 pic = requests.get(url_img)
#                 str_skin = str_skin.replace(' | ', '_')

#                 img_bytes = io.BytesIO(pic.content)
#                 img = Image.open(img_bytes)

#                 img_bg = Image.open(img_bg_str)
#                 img_bg.paste(img, (0, 0), img)
#                 img_bg.save('cases\\'+case_name+'\\'+str_skin+'.png')

#                 break
#     print(f'> Кейс "{case_name}" успешно загружен!')
print('Парсинг кейсов успешно завершен!')
print('Отсутствующие скины: ')
print(skins_missing)