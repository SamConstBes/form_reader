#services.py
import json
import os

from glob import glob as allglob

def process_data(json_data):
    cmd = json_data['action']
    del json_data['action']
    match cmd:
        case 'saveTable':
            #--Список товаров-----------
            updateSettings('saveTable', json_data['data'])
            res = 'products'
        case 'composition':
            #--Галерея композиции
            save_settings(cmd, json_data)
            res = 'catalogue'
        case 'wedding':
             #--Галерея свадебные букеты
            save_settings(cmd, json_data)
            res = 'catalogue'
        case 'session':
            #--Галерея фотосессии
            save_settings(cmd, json_data)
            res = 'catalogue'
        case 'design':
            #--Галерея оформления
            save_settings(cmd, json_data)
            res = 'catalogue'
        case _:
            res = False
    return res


def save_settings(s_name, data):
    set_name = f'settings/{s_name}.json'
    data[s_name] = transform_flat_to_nested(data)
    data_to_save = {
        s_name: transform_flat_to_nested(data)
    }

    with open(set_name, 'w') as fp:
        json.dump(data_to_save, fp, ensure_ascii=False, indent=4)


def updateSettings(cmd_name, data):
    app_data = load_settings('default-content')

    app_data[cmd_name] = data
    settings_file = 'default-content'
    simple_save(settings_file, app_data)


def simple_save(cmd_name, data):
    """Func for save file in json"""
    set_name = f'settings/{cmd_name}.json'
    with open(set_name, 'w') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)


def transform_flat_to_nested(flat_data):
    nested = {}
    for key, value in flat_data.items():
        if key.startswith(('prodName_', 'prodPrice_', 'prodPhoto_', 'prodLink_')):
            prefix, name = key.split('_', 1)
            field = prefix.replace('prod', 'prod_')  # prodName_ → prod_name_
            if name not in nested:
                nested[name] = {}
            nested[name][field] = value
    return nested


def process_settings(action, data):
    """Save socials, policy, terms from main page.
    Empty values don`t change default table"""
    #--Cохранить ссылки и телефон
    data_to_save = None
    cmd_name = action
    set_name = f'settings/{cmd_name}.json'
    match cmd_name:
        case 'hrefs':
            data_to_save = {
                    "telega": data.tgLink,
                    "avito": data.avitoLink,
                    "flowwow": data.flowLink,
                    "vkmess": data.vkMess,
                    "vk": data. vkLink,
                    "yula": data.youlaLink,
                    "phone": data.phone
                }
        case 'soglashenie':
            data_to_save = [data.docText]
        case 'politika':
            data_to_save = [data.docText]
    updateSettings(cmd_name, data_to_save)


def save_all_json():
    merged = []
    try:
        for filename in allglob("settings/*.json"):  # или укажите конкретные файлы
            with open(filename, 'w', encoding='utf-8') as f:
                data = json.load(f)
                merged.append(data)  # добавляет элементы списка

        with open('settings/settings.json', 'r', encoding='utf-8') as f:
            json.dump(merged, f, ensure_ascii=False, indent=4)
            return True
    except Exception as error:
        print(str(error))
        return False
    

def load_settings(name):
    with open(f'settings/{name}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def load_file(upload_path, file, filename):
    save_path = os.path.join(upload_path, filename)
    file.save(save_path)
    relative_path = f'static/loads/{filename}'
    return relative_path