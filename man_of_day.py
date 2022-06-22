import time
import datetime
import random
import os


class ManOfDay:
    # Регистрация нового пользователя
    def reg(file_name, member_id):
        if not os.path.isfile(file_name):  # Если файла нет, надо его создать
            f = open(file_name, 'w')
            f.write('-1 -1 -1\n')
            f.write('none\n')
            f.close()

        # Формат файла
        # [день] [месяц] [год]
        # [неиспользуемая строка]
        # [1 участник] [его счетчик ]
        # ...
        # [N участник] [его счетчик]

        # Чтение файла
        f = open(file_name, 'r')
        members = f.read().split()
        f.close()

        if member_id in members:  # Если участник уже есть в списке вернем 0
            return 0
        else:   # Иначе добавим его туда
            f = open(file_name, 'a')
            f.write(member_id + ' 0\n')
            f.close()
            return 1

    # Сама функция рулетки, вернет участника в виде строки
    def get(file_name):
        # Выводим ошибку если нет файла
        if not os.path.isfile(file_name):
            return None

        cur_date = datetime.datetime.now()  # Получение текущий даты

        # Читаем файл и записываем все содержимое в переменную inf
        f = open(file_name, 'r')
        inf = f.read().split()
        f.close()

        if not(int(inf[0]) == cur_date.day and
                int(inf[1]) == cur_date.month and
                int(inf[2]) == cur_date.year):
            members_len = (len(inf)-4) // 2  # Количество участников
            member_index = 4 + random.randint(0, members_len-1)*2  # рулетка
            member_count = int(inf[member_index+1]) + 1

            f = open(file_name, 'w')
            f.write(f'{cur_date.day} {cur_date.month} {cur_date.year}\n')
            f.write('none\n')  # Не знаю зачем это поле, но пусть будет
            f.write(f'{inf[member_index]} {member_count}\n')

            user = inf[4]

            del inf[member_index]  # удаление id человека из списка
            del inf[member_index]  # удаление счетчика человека из списка

            # Записываем остальных участников
            for i in range(4, len(inf)):
                f.write(inf[i])
                if i % 2 != 0:  # если индекс четный
                    f.write('\n')  # значит это счетчик,
                    # поэтому переходим на следующую строку
                else:
                    f.write(' ')

            f.close()
            return user
        else:
            f = open(file_name, 'r')
            return '!'+inf[4]
            f.close()

    # Получить список топа, вернет словарь участников
    # отсортированый по убыванию счетчика
    def get_top(file_name):
        if not os.path.isfile(file_name):
            return None

        top = {}

        f = open(file_name, 'r')
        inf = f.read().split()
        f.close()

        # -1 сигнализирует о том, что розыгрыш ни разу не проводился
        if inf[0] == '-1':
            return None

        members_len = (len(inf)-4) // 2  # Количество участников
        for i in range(0, members_len):
            member_index = 4+i*2
            member_count = member_index+1
            top[inf[member_index]] = int(inf[member_count])

        # Великая сортировка от Максима Заказчика
        top = {k: v for k, v in sorted(top.items(),
               key=lambda item: item[1])[::-1]}

        return top

    # Устанавливает всем учатникам 0 очков
    def reset(file_name):
        if not os.path.isfile(file_name):
            return None

        f = open(file_name, 'r')
        inf = f.read().split()
        f.close()

        # -1 сигнализирует о том, что розыгрыш ни разу не проводился
        if inf[0] == '-1':
            return None

        f = open(file_name, 'w')
        for i in range(4, len(inf)):
            if i % 2 == 0:
                f.write(inf[i]+' ')
            else:
                f.write('0\n')
        f.close()


        
        

