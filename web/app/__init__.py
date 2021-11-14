from flask import Flask, render_template, url_for, request, redirect
from redis import Redis
from app.my_config import Config
from app import tools as tl
# from my_config import Config
# import tools as tl


app = Flask(__name__)
app.db = Redis(**Config['REDIS_KWARGS'], decode_responses=True)

@app.route('/')
@app.route('/main_page', methods=['GET'])
def main_page():
    return render_template('main_page.html')

# <li><a href="{{ url_for('new_data') }}">Добавить новые данные</a></li>
@app.route('/new_data', methods=['GET', 'POST'])
def new_data():
    if request.method == "POST":
        if ("new_class" in request.form) and (request.form.get("new_class") != ''):
            try:
                app.db.sadd('labels', request.form["new_class"])
            except:
                return "При добавлении класса произошла ошибка"
        elif ("new_subclass" in request.form) and (request.form.get("new_subclass") != ''):
            try:
                class_name = request.form.get("class_select")
                dict_class = app.db.hgetall(class_name)
                if request.form["text_subclass"]=='':
                    dict_class[request.form["new_subclass"]] = 'Нет данных'
                else:
                    dict_class[request.form["new_subclass"]] = request.form["text_subclass"]
                app.db.hmset(class_name, dict_class)
            except:
                return "При добавлении подкласса произошла ошибка"
            return redirect('/class_data')
    labels = [lbl for lbl in app.db.smembers('labels') if lbl != b''] 
    return render_template('new_data.html', labels=labels)

@app.route('/info_data', methods=['GET'])
def info_data():
    flag_label = False
    try:
        labels = [lbl for lbl in app.db.smembers('labels') if lbl != ''] 
        info = {lbl: app.db.hgetall(lbl) for lbl in labels if app.db.hgetall(lbl)}
        if len(labels):
            flag_label = True
    except:
        return "Ошибка чтения данных"
    graphJSON = tl.create_map(labels, info)
    return render_template('info_data.html', graphJSON=graphJSON, flag_label=flag_label)

@app.route('/class_data', methods=['GET'])
def class_data():
    try:
        labels = [lbl for lbl in app.db.smembers('labels') if lbl != ''] 
        info = {lbl: app.db.hgetall(lbl) for lbl in labels if app.db.hgetall(lbl)}
    except:
        return "Ошибка чтения данных"
    return render_template('class_data.html', labels=labels, info=info)

@app.route('/class_data/<string:name_class>/<string:name_subclass>', methods=['GET'])
def subclass_data(name_class, name_subclass):
    try:
        labels = [lbl for lbl in app.db.smembers('labels') if lbl != ''] 
        info = {lbl: app.db.hgetall(lbl) for lbl in labels if app.db.hgetall(lbl)}
    except:
        return "Ошибка чтения данных"
    info_subclass = {'name_class': name_class, 'name_subclass': name_subclass}
    return render_template('class_data_info.html', labels=labels, info=info, info_subclass=info_subclass)

@app.route('/class_data/<string:name_class>/<string:name_subclass>/del', methods=['GET'])
def subclass_data_del(name_class, name_subclass):
    try:
        dict_class = app.db.hgetall(name_class)
        if name_subclass in dict_class:
            dict_class.pop(name_subclass, None)
            app.db.delete(name_class)
            app.db.hmset(name_class, dict_class)
    except:
        return "Ошибка удаления"
    return redirect('/class_data')

if __name__ == '__main__':
    app.run(debug=True)
    

app.db.close()