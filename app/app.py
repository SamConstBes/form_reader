from flask import Flask, request, redirect, flash, render_template, jsonify, send_from_directory, url_for, g

app = Flask(__name__)
app.secret_key = 'my_super_secret_key_123'
data = content = {}

from .testing import result
from .models import *
from .services import process_data, process_settings, save_all_json, load_settings


@app.before_request
def before_request():
    global data, content, result
    
    data = load_settings('default-settings')
    content = load_settings('default-content')
    if request_id := request.headers.get("Request-Id"):
        g.request_id = request_id
    else:
        g.request_id = str('1')
    app.logger.debug(f"{request}, data: {str(request.get_data())[:200]}")


@app.route('/', methods=['GET'])
def main_page():
    # print(data)
    return render_template('index.html', current_page='home')


@app.route('/config', methods=['GET'])
def config_page():
    form_data = {
        "formNаme": "products",
        "formAction": "/saveTable",
        "formId": "saveTable",
        "labelBtn": "Сохранить данные",
        "head":["name", "text", "link", "photo"],
        "tabs": result
    }
    return render_template('config.html', current_page='config', form = form_data )


@app.route('/products', methods=['GET'])
def prod_page():
    prod_data = data['dostavka']
    for d in prod_data.values():
        d['prod_Photo'] = d['prod_Photo'].replace('./', 'static/')
    form_data = {
        "formNаme": "Настройки таблицы товаров",
        "formAction": "/saveTable",
        "formId": "saveTable",
        "labelBtn": "Сохранить данные",
        "head":["Товар", "Фото", "Стоимость", "  Ссылка", "Изображение"],
        "tabs": prod_data
    }
    # print("Тип элемента:", type(result[1]))  # dict, Row, namedtuple?
    # print("Ключи:", result[1].keys() if hasattr(result[1], 'keys') else dir(result[1]))
    # print("prod_price:", result[1].get('prod_price', 'НЕТ КЛЮЧА') if isinstance(result[1], dict) else result[1].prod_price)
    return render_template('products.html', result = prod_data, current_page='products', form = form_data)


@app.route('/catalogue', methods=['GET'])
def cat_page():
    return render_template('catalogue.html', result = result, current_page='catalogue')


@app.route('/blog', methods=['GET'])
def blog_page():
    return render_template('blog.html', result = result, current_page='blog')


@app.route('/action', methods=['GET'])
def act_page():
    return render_template('action.html', result = result, current_page='action')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/social', methods=['POST'])
def save_social():
    tgLink = request.form.get('tgLink', '')
    youlaLink = request.form.get('youlaLink', '')
    flowLink = request.form.get('flowLink', '')
    avitoLink = request.form.get('avitoLink', '')
    vkLink = request.form.get('vkLink', '')
    vkMess = request.form.get('vkMess', '')
    phone = request.form.get('phone', '')
    
    social = Social(tgLink, youlaLink, flowLink, avitoLink, vkLink, vkMess, phone)
    try:
        process_settings('social',social)
        flash('Социальные ссылки сохранены!')
    except Exception as error:
        flash('Ошибка при сохранении социальных ссылок!')
        print('Error in save social', str(error))
    return redirect(url_for('main_page'))


@app.route('/docPath', methods=['POST'])
def save_docs():
    docPath = request.form.get('docPath', '')
    docPolit = request.form.get('docPolit', '')
    action = request.form.get('action', '')
    
    if action == 'soglashenie':
        docs = DockPath(docPath)
        process_settings('soglashenie', docs)
        flash('Пользовательское соглашение сохранено!')
    elif action == 'politika':
        docs = DockPath(docPolit)
        process_settings('politika', docs) 
        flash('Политика конфиденциальности сохранена!')
    
    return redirect(url_for('main_page'))


@app.route('/saveTable', methods=['POST'])
def save_products():
    try:
        content_type = request.headers.get('Content-Type', '')
        json_data = request.json
        if json_data is None:
            # Если JSON не получен, пробуем прочитать тело запроса как текст
            raw_data = request.get_data(as_text=True)
            print(f"Raw request body: {raw_data}")
            return jsonify({
                "error": "Invalid Content-Type or malformed JSON",
                "received_content_type": content_type,
                "raw_body": raw_data
            }), 400
        res = json_data
        # msg = "success" if process_data(json_data) else "error"
        template = process_data(json_data)
        # return jsonify({
        #     "status": msg,
        #     "received_data": json_data
        # }), 200
        #return redirect('/products?status=success', code=303)
        return render_template(f'{template}.html', result = res)
    except Exception as error:
        print(str(error))


@app.route('/add', methods=['POST'])
def add_data():
    try:
        content_type = request.headers.get('Content-Type', '')
        json_data = request.json
        print("Received JSON data:", json_data)
    except Exception as error:
        print(str(error))

    return jsonify({
            "status": "success",
            "received_data": json_data
        }), 200


@app.route('/save-settings')
def save_json():
    res = save_all_json()
    flash('Данные отправлены!') if res else flash('Ошибка отправки данных!')
    
    return redirect(url_for('main_page'))
