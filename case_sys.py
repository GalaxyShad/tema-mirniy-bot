
import json
import random 
import io

from PIL import Image, ImageDraw, ImageColor
from utils import o_load

CASES_PATH = 'static\\cases\\'
CASES_RARITY = {
    'blue':   'Армейское', 
    'purple': 'Запрещенное', 
    'pink':   'Засекреченное', 
    'red':    'Тайное', 
    'gold':   'Редкое', 
}
CASES_QUALITY = {
    'Factory New': 'Прямо с завода',
    'Minimal Wear': 'Немного поношенное',
    'Field-Tested': 'После полевых испытаний',
    'Well-Worn': 'Поношенное',
    'Battle-Scarred': 'Закаленное в боях'
}



def get_random_rarity():
    # return 'gold'

    chance = random.random() * 100

    if chance <= 0.26:
        return 'gold'
    elif chance <= 0.90:
        return 'red'
    elif chance <= 4.10:
        return 'pink'
    elif chance <= 20.08:
        return 'purple'
    else:
        return 'blue'

    return "it can't be..."


class CsGoCaseMgr:
    def __init__(self):
        self.cases = o_load(CASES_PATH + 'cases.json')
        self.cur_case_path = None
        self.cur_case_info = None


    def open_case(self, case_name = None):

        if case_name is None:
            case_name = random.choice(list(self.cases))
        elif type(case_name) == str:
            if not case_name in self.cases:
                return (False, 'Указанного кейса не существует.', None)
        else:
            return (False, 'Аргумент case_name инвалидный', None)

        rarity = get_random_rarity()
        
        case = self.cases[case_name]
        case_path = CASES_PATH + case['path'] 
        case_info = o_load(case_path + 'case_drop.json')

        if rarity == 'gold':
            knifes = o_load(CASES_PATH + 'knifes.json')
            knife_type = random.choice(list(knifes))
            knife_name = random.choice(list(knifes[knife_type]))
            knife = knifes[knife_type][knife_name]

            knife_quality = random.choice(list(knife['rus_prices']))

            drop = {
                'name': knife_type + ' | ' + knife_name,
                'quality': knife_quality,
                'rarity': CASES_RARITY['gold'],
                'price': knife['rus_prices'][knife_quality],
                "img_url": knife['img_url'],
                "img_file": knife['img_path']
            }

            img_path = CASES_PATH + 'knifes\\' + drop['img_file']
        else:
            drop = self.get_drop_from_case(case_info, rarity)
            img_path = CASES_PATH + case['path'] + drop['img_file']

        images = self.make_images(case_info, case_path, img_path, rarity)
        csgo_roll = CsGoRoll(images)
        gif = csgo_roll.bmake_gif()

        if drop['quality'] in CASES_QUALITY:
            drop['quality'] = CASES_QUALITY[drop['quality']]

        drop['rarity_color'] = rarity
        drop['case_name'] = case_info['case_name_rus']
        drop['case_img_url'] = case_info['case_img_url']
        drop['gif_time'] = (csgo_roll.get_max_frames() * 20) / 1000 + 0.65

        return (True, drop, gif)


    def get_cases_names(self):
        res = []

        for case_name in self.cases:
            res.append({'en': case_name, 'ru': self.cases[case_name]['name_rus']})

        return res


    def get_drop_from_case(self, case_info, rarity):
        weapon_name = random.choice(list(case_info['items'][rarity]))
        weapon = case_info['items'][rarity][weapon_name]

        weapon_quality = random.choice(list(weapon['rus_prices']))
        if not weapon['rus_prices'][weapon_quality]:
            for quality in weapon['rus_prices']:
                if weapon['rus_prices'][quality]:
                    weapon_quality = quality
                    break

        drop = {
            'name': weapon['name_rus'],
            'quality': weapon_quality,
            'rarity': CASES_RARITY[rarity],
            'price': weapon['rus_prices'][weapon_quality],
            "img_url": weapon['img_url'],
            "img_file": weapon['img_path']
        }

        return drop


    def make_images(self, case_info, case_path, win_drop_img_path, win_drop_color):
        images = {}

        img = Image.open(win_drop_img_path)
        img.thumbnail((64, 64))
        images['win_drop'] = img
        images['win_drop_color'] = win_drop_color

        case_items = case_info['items']
        for rarity in case_items:
            if not case_items[rarity]:
                continue

            images[rarity] = []
            for item_name in case_items[rarity]:
                item = case_items[rarity][item_name]

                img = Image.open(case_path + item['img_path'])
                img.thumbnail((64, 64))
                images[rarity].append(img)

        return images
                

class CsGoRoll:
    def __init__(self, images):
        self.ITEM_SIZE = 64
        self.GAP       = 4

        self.WIDTH  = 400
        self.HEIGHT = 100

        self.start_spd = 15#15
        self.spd = self.start_spd
        self.x = 0
        self.items = []

        item_delta = self.ITEM_SIZE + self.GAP
        self.s = random.randrange(40, 50, 1) * item_delta\
                 + random.randrange(2, 62)
        self.dec = self.spd**2 / (2 * self.s - 400 + self.spd)

        self.load_images()

        for i in range(int(self.s // self.ITEM_SIZE) + 6):
            # quality = get_random_rarity()
            quality = random.choice(('blue', 'purple', 'pink', 'red'))

            item = {
                'x':    i * item_delta,
                'col':  quality
            }

            if (self.s // item_delta) * item_delta == (item['x'] // item_delta) * item_delta:
                item['img'] = images['win_drop']
                item['col'] = images['win_drop_color']
            elif item['col'] != 'gold':
                item['img'] = random.choice(images[quality])


            if item['col'] == 'gold':
                item['img'] = self.img_rare_item

            self.items.append(item)

        

    def load_images(self):
        path = 'static\\case_roll_hud\\'
    
        self.img_tm = {}

        self.img_tm['blue'] = Image.open(path+'blue.png')
        self.img_tm['purple'] = Image.open(path+'purple.png')
        self.img_tm['pink'] = Image.open(path+'pink.png')
        self.img_tm['red'] = Image.open(path+'red.png')
        self.img_tm['gold'] = Image.open(path+'gold.png')

        self.img_effects = Image.open(path+'effects.png')

        self.img_bg = Image.open(path+'bg.png')

        self.img_rare_item = Image.open(path+'rare_item.png')
        self.img_rare_item.thumbnail((64, 64))



    def next_frame(self):
        image = Image.new("RGBA", (self.WIDTH, self.HEIGHT))
        draw = ImageDraw.Draw(image)

        
        draw.rectangle((0, 0, self.WIDTH, self.HEIGHT),  fill='#191721')
        y_delta = (self.HEIGHT - self.ITEM_SIZE) // 2

        for item in self.items:
            _, img_height = item['img'].size

            image.paste(
                self.img_tm[item['col']], 
                (int(item['x']), int(y_delta)),
                self.img_tm[item['col']]
            )
            image.paste(item['img'], (int(item['x']), int(y_delta) + (64 - img_height) // 2), item['img'])
        
  
        image.paste(self.img_effects, (0, 0), self.img_effects)
        draw.rectangle((200, 0, 202, 100), fill='white')
        # draw.rectangle((self.s-self.x, 0, self.s+2-self.x, 100), fill='red')

        self.update()

        return image
    

    def update(self):
        self.spd -= self.dec

        if self.spd < 0:
            self.spd = 0

        self.x += self.spd

        for i in range(len(self.items)):
            self.items[i]['x'] -= self.spd


    def get_max_frames(self):
        return int(self.start_spd / self.dec) 


    def bmake_gif(self):
        frames = []
        for number in range(self.get_max_frames()):
            frames.append(self.next_frame())

        buf = io.BytesIO()
        frame_one = frames[0]
        frame_one.save(buf, format="GIF", append_images=frames,
                       save_all=True, duration=20, optimize=True, loop=1)

        return buf
     


if __name__ == '__main__':
    csgo_case_mgr = CsGoCaseMgr()

    status, drop, gif = csgo_case_mgr.open_case()

    print(status, drop)
    with open('lol.gif', 'wb') as fo:
        fo.write(gif.getbuffer())




    

