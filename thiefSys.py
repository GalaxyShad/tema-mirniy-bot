import os

START_THIEF_BALANCE = 250

# Загрузка всех кошельков из файла
def vor_get_all_wallets(file_name):
    if not os.path.isfile(file_name):  
        return None

    wallets = {}

    f = open(file_name, 'r')
    file_str = f.read().split()
    f.close()

    for i in range(len(file_str) // 2):
        wallets[file_str[i*2]] = int(file_str[i*2+1])

    return wallets


# Сохранение всех кошельков в файл
def vor_save_all_wallets(file_name, wallets):
    # Запись в файл
    f = open(file_name, 'w')
    for wallet_id in wallets:
        f.write(wallet_id + ' ' + str(wallets[wallet_id]) + '\n')
    f.close()


# Регистрация кошелька
def vor_reg(file_name, wallet_id):   
    wallets = vor_get_all_wallets(file_name)
    if wallets == None:
        wallets = {wallet_id: START_THIEF_BALANCE}
        vor_save_all_wallets(file_name, wallets)
        return 1

    if wallet_id in wallets:  # Если участник уже есть в списке вернем 0
        return 0
    else:   # Иначе добавим его туда
        wallets[wallet_id] = START_THIEF_BALANCE
        vor_save_all_wallets(file_name, wallets)
        return 1


# Добавление денег в кошелек
def vor_add_to_balance(file_name, wallet_id, money):
    wallets = vor_get_all_wallets(file_name)
    if wallets == None:
        return None

    if wallet_id in wallets:
        wallets[wallet_id] += money
        vor_save_all_wallets(file_name, wallets)
        return 1
    else:
        return 0


# Вычет денег из кошелька
def vor_withdraw_from_balance(file_name, wallet_id, money):
    wallets = vor_get_all_wallets(file_name)
    if wallets == None:
        return 0

    if wallet_id in wallets:
        if wallets[wallet_id] >= money:
            wallets[wallet_id] -= money
            vor_save_all_wallets(file_name, wallets)
            return 1
        else:
            return 2
    else:
        return 0
