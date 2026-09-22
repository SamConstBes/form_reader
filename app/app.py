from flask import Flask, request, redirect, flash, render_template, jsonify, send_from_directory, url_for, g, session, current_app
from werkzeug.utils import secure_filename

from .models import *
from .services import process_data, process_settings, load_settings, load_file
from config import app_config, row_config, obj_config, logger, form_data, FIELD_CONFIG, PAGE_CONFIGS

from .testing import result, raw_data

app = Flask(__name__, instance_relative_config=False)

app.secret_key = 'my_super_secret_key_123'
app.config['IS_UPDATE'] = load_settings('default-content')
app.config['DATA'] = load_settings('default-settings')
app.config['UPLOAD_FOLDER'] = app_config.UPLOAD_FOLDER

data = content = {}


@app.before_request
def before_request():
    if request_id := request.headers.get("Request-Id"):
        g.request_id = request_id
    else:
        g.request_id = str(1)  
    app.logger.debug(f"{request}, data: {str(request.get_data())[:200]}")


@app.route('/', methods=['GET'])
def main_page():
    is_updating = session.get('is_updating', False)
    data = current_app.config['IS_UPDATE'] if is_updating else current_app.config['DATA']
    return render_template('index.html',current_page='home', config=data)


@app.route('/products', methods=['GET'])
def prod_page():
    is_updating = session.get('is_updating', False)
    value = current_app.config['IS_UPDATE'].get('saveTable')

    prod_data = value if is_updating else current_app.config['DATA'].get('dostavka') 
    form_data["head"] = PAGE_CONFIGS.get("products").get("head")
    form_data["formNаme"] = PAGE_CONFIGS.get("products").get("formNаme")
    form_data["formAction"] = PAGE_CONFIGS.get("products").get("formAction")
    form_data["tabs"] =  prod_data
 
    return render_template('products.html', current_page='products', result=prod_data, form=form_data, row=row_config)


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
    return render_template('config.html', current_page='config', forms=[], row=obj_config)


@app.route('/catalogue', methods=['GET'])
def cat_page():
    return render_template('catalogue.html', current_page='catalogue', forms=raw_data)


@app.route('/blog', methods=['GET'])
def blog_page():
    return render_template('blog.html', current_page='blog', result=result)


@app.route('/action', methods=['GET'])
def act_page():
    return render_template('action.html', current_page='action', result=result)


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
        process_settings('hrefs', social)
        # Обновляем состояние перед редиректом
        session['is_updating'] = True
        app.config['IS_UPDATE'] = load_settings('default-content')
        logger.info("Success to save social links")
        flash('Социальные ссылки сохранены!')
    except Exception as error:
        logger.error("Failed to save social links: %", error)
        flash('Ошибка при сохранении социальных ссылок!', 'error')
        return redirect(url_for('main_page'))
        
    return redirect(url_for('main_page'))


@app.route('/docPath', methods=['POST'])
def save_docs():
    """Endpoint for saving texts"""
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
    session['is_updating'] = True
    app.config['IS_UPDATE'] = load_settings('default-content')
    return redirect(url_for('main_page'))


@app.route('/saveTable', methods=['POST'])
def save_products():
    try:
        content_type = request.headers.get('Content-Type', '')
        json_data = request.json
        if json_data is None:
            # Если JSON не получен, пробуем прочитать тело запроса как текст
            raw_data = request.get_data(as_text=True)
            return jsonify({
                "error": "Invalid Content-Type or malformed JSON",
                "received_content_type": content_type,
                "raw_body": raw_data
            }), 400
        res = json_data

        template = process_data(json_data)
        app.config['IS_UPDATE'] = load_settings('default-content')
        form_data = {
        "formNаme": "Настройки таблицы товаров",
        "formAction": "/saveTable",
        "formId": "saveTable",
        "labelBtn": "Сохранить данные",
        "head":["Товар", "Стоимость", "Ссылка", "Фото", "Изображение"],
        "tabs": res['data']
        }

        session['is_updating'] = True
        return render_template(f'{template}.html', result = res, form = form_data, row=row_config)
    except Exception as error:
        logger.error("Failed to save products: %", error)


@app.route('/uploadFile', methods=['POST'])
def upload_file():
    
    if 'userFile' not in request.files:
        return jsonify({'error': 'File not found'}), 400
    file = request.files['userFile']
    if file.filename == '':
        return jsonify({'error': 'File name empty'}), 400
    if file and file.filename != '':
        file_name =  secure_filename(file.filename)
        upload_path = current_app.config['UPLOAD_FOLDER']
        result = load_file(upload_path, file, file_name)
    return jsonify({"success": result}), 200


@app.route('/add', methods=['POST'])
def add_data():
    json_data = None
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
    res  = False
    flash('Данные отправлены!') if res else flash('Ошибка отправки данных!')
    
    return redirect(url_for('main_page'))