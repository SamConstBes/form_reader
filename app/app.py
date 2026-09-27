from flask import Flask, request, redirect, flash, render_template, jsonify, send_from_directory, url_for, g, session, current_app
from werkzeug.utils import secure_filename

from .models import *
from .services import process_data, process_settings, load_settings, load_file
from .config import app_config, row_config, blog_config, obj_config, logger, form_data, FIELD_CONFIG, PAGE_CONFIGS

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
    is_updating = session.get('is_updating', False)
    value = current_app.config['IS_UPDATE'].get('saveTable')
    
    prod_data = value if is_updating else current_app.config['DATA'].get('dostavka')
    return render_template('catalogue.html', current_page='catalogue', forms=prod_data, row=obj_config)


@app.route('/blog', methods=['GET'])
def blog_page():
    is_updating = session.get('is_updating', False)
    value = current_app.config['IS_UPDATE'].get('saveTable')

    # prod_data = value if is_updating else current_app.config['DATA'].get('dostavka') 
    # form_data["head"] = PAGE_CONFIGS.get("products").get("head")
    # form_data["formNаme"] = PAGE_CONFIGS.get("products").get("formNаme")
    # form_data["formAction"] = PAGE_CONFIGS.get("products").get("formAction")
    # form_data["tabs"] =  prod_data
    text = [
                    "Есть в тюльпанах что‑то неуловимо трогательное — то ли в их строгой форме, то ли в хрупкой грации тонкого стебля. Они появляются ранней весной, когда земля ещё хранит зимнюю прохладу, а небо только учится быть по‑настоящему голубым. И уже одним своим присутствием сообщают: всё будет хорошо. ",
                    "Многие уверены, что тюльпаны — изобретение Голландии. На деле их родина — степи и горные районы Центральной Азии, где дикие виды цветут и по сей день. В Европу они попали в XVI веке через Османскую империю, а в Нидерландах обрели вторую жизнь. Голландцы не просто полюбили эти цветы — они превратили их в символ нации, в предмет страсти, в искусство. ",
                    "Степные тюльпаны — особая история. Они не похожи на своих пышных садовых собратьев: скромные, невысокие, с узкими листьями и некрупными цветками. Но в их простоте — невероятная сила. Они выживают в суровых условиях, цветут под палящим солнцем и холодными ветрами, напоминая: красота не всегда требует роскоши. ",
                    "Голландия же подарила тюльпанам мировую славу. Здесь, на бескрайних полях, они превращаются в разноцветные моря — то алые, то жёлтые, то лиловые. Каждый год тысячи людей приезжают сюда, чтобы увидеть это чудо: волны бутонов, колышущиеся на ветру, словно живое полотно, которое природа рисует заново каждую весну. ",
                    "Символика тюльпанов богата и многогранна. В разных культурах они означают любовь, надежду, возрождение, чистоту и даже славу. Красные — признание в страсти, жёлтые — пожелание радости, белые — знак искренности и нежности. Розовые тюльпаны говорят о зарождающихся чувствах, а фиолетовые — о величии и достоинстве. ",
                    "В быту тюльпаны удивительно неприхотливы. Простой букет в стеклянной вазе способен преобразить любое пространство: добавить света кухне, оживить гостиную, привнести ноту свежести в рабочий кабинет. Их красота не кричит — она шепчет, ненавязчиво, но убедительно. ",
                    "Эти цветы универсальны в подарке. Их дарят на 8 Марта, дни рождения, свидания, новоселья. Они уместны и в торжественном букете, и в скромном знакомстве. Тюльпаны не требуют повода — они сами становятся поводом для улыбки. ",
                    "Уход за срезанными тюльпанами прост, но имеет свои тонкости. Воду в вазе нужно менять ежедневно, подрезая стебли под углом. Лучше держать букет в прохладном месте, вдали от батарей и прямых солнечных лучей. Если хочется вырастить тюльпаны самостоятельно, достаточно посадить луковицы осенью — и следующей весной они порадуют первыми бутонами. ",
                    "История тюльпанов хранит удивительные страницы. В XVII веке в Голландии разразилась настоящая «тюльпанная лихорадка»: редкие сорта оценивались дороже золота. Люди продавали дома и земли, чтобы приобрести заветную луковицу. Сегодня тюльпаны доступны каждому, но их магия осталась прежней — они по‑прежнему способны завораживать. ",
                    "Любопытно, что тюльпаны умеют «расти» даже после срезки. В вазе они могут вытянуться на несколько сантиметров, будто стремясь дотянуться до солнца. Это придаёт букетам особую живость: каждый день они выглядят чуть иначе, раскрывая новые грани своей красоты. ",
                    "В искусстве тюльпаны стали излюбленным мотивом. Их изображали на полотнах голландских мастеров, воспевали в стихах, посвящали им музыкальные произведения. Они вдохновляют и сегодня — от дизайна одежды до интерьерных решений. Их форма, цвет, даже тень, которую они отбрасывают на стену, превращаются в источник творчества. ",
                    "Тюльпаны умеют говорить без слов. Их бутоны, раскрывающиеся навстречу утру, их лёгкий наклон под ветром, их молчаливое присутствие в доме — всё это части большого диалога между природой и человеком. Они напоминают: красота может быть простой, но от этого не менее волнующей. ",
                    "Каждый год, когда появляются первые тюльпаны, мир будто становится ярче. Они — как маленькие праздники, которые природа дарит нам без повода. И в этом их главное чудо: они умеют делать обыденность чуть более волшебной, а сердце — чуть более открытым для радости. "
                    ]
    content = [
           {"id": "item1",
            "name": "Фестиваль тюльпанов",
            "text": '\n'.join(text),
            "photo": "static/loads/flowers.png"},
            {"id": "item2",
            "name": "Фестиваль",
            "text": '\n'.join(text),
            "photo": "static/loads/flowers.png"}
            ]
    return render_template('blog.html', current_page='blog', form=content, row=blog_config)


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
    flash('Данные отправлены!')
    return jsonify({
            "status": "success",
            "received_data": json_data
        }), 200


@app.route('/save-settings')
def save_json():
    res  = False
    flash('Данные отправлены!') if res else flash('Ошибка отправки данных!')
    
    return redirect(url_for('main_page'))