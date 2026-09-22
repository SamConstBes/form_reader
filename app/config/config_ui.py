#config.py

#---Настройка типов полей---
FIELD_CONFIG = { 
    "prodName": {"type": "text", "label": "Название"},
    "prodPrice": {"type": "text", "label": "Фото"},
    "prodPhoto": {"type": "file", "label": "Фото"},
    "prodLink": {"type": "textarea", "label": "Описание"} 
    }

#---Настройка формы добавления товара---
row_config = {
    "objname": "Добавить товар",
    "action": "/add",
    "id": "add",
    "fields": FIELD_CONFIG,
    "inputs":{
    "Наименование": "prodName",
    "Стоимость": "prodPrice",
    "Ссылка на товар": "prodLink", 
    "Фото": "prodPhoto",
    }
}

#---Настройка формы добавления объекта данных---
obj_config = {
    "objname": "Добавить объект",
    "action": "/add",
    "id": "add",
    "inputs":{
    "наименование": "prodNewName", 
    "эндпойнт": "prodNewPhoto",
    "эндпойнт2": "prodNewPhoto2",
    "путь": "prodNewPrice",
    "Заголовки": ["Блок","путь", "ссылка"] 
    }
}

form_data = {
        "formNаme": "Настройки таблицы товаров",
        "formAction": "/saveTable",
        "formId": "saveTable",
        "labelBtn": "Сохранить данные",
        "head":[],
        "tabs": None
    }

PAGE_CONFIGS = {
    "products":
            {
            "formAction": "/saveTable",
            "formNаme": "Настройки таблицы товаров",
            "head":["Товар", "Стоимость", "Ссылка", "Фото", "Изображение"],
            },
    "content": {}
}