result = {
"rose":{
    'prod_photo_name': 'rose.jpg',
    'prod_price': 100,
    'prid_link': 'https://t.me/prolivstalina',
    'src': '/static/loads/red-rose.png'
},
"gooo":{
    'prod_photo_name': 'rose.jpg',
    'prod_price': 200,
    'prid_link': 'https://t.me/prolivstalina',
    'src': '/static/loads/autumn-flowers.png'
},
"orchid":{
    'prod_photo_name': 'rose.jpg',
    'prod_price': 1100,
    'prid_link': 'https://t.me/prolivstalina',
    'src': '/static/loads/buketi-belom.png'
},
"peon":{
    'prod_photo_name': 'rose.jpg',
    'prod_price': 130,
    'prid_link': 'https://t.me/prolivstalina',
    'src': '/static/loads/blog-pion.jpg'
},
"tulpan":{
    'prod_photo_name': 'rose.jpg',
    'prod_price': 100,
    'prid_link': 'https://t.me/prolivstalina',
    'src': '/static/loads/red-rose.png'
},
}

raw_products = [
    {"name": "Роза", "price": 100, "link": "...", "photo": "/static/loads/red-rose.png"},
    {"name": "Пион", "price": 130, "link": "...", "photo": "/static/loads/blog-pion.jpg"},
    # ...
]

# Превращаем список в словарь с унифицированными ключами
tabs = {}
for index, prod in enumerate(raw_products, start=1):
    key = f"item_{index}"
    tabs[key] = {
        "prod_Name": prod["name"],
        "prod_Price": prod["price"],
        "prod_Link": prod["link"],
        "prod_Photo": prod["photo"]
    }

