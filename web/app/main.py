from flask import Flask, render_template, url_for, request, redirect
import redis
from app import tools as tl
# import tools as tl


app = Flask(__name__)
app.db = redis.Redis(**tl.Config['REDIS_KWARGS'], decode_responses=True)

@app.route('/')
@app.route('/main_page', methods=['GET'])
def main_page():
    return render_template('main_page.html')

@app.route('/new_data', methods=['GET', 'POST'])
def new_data():
    if request.method == "POST":
        try:
            if ("new_class" in request.form) and (request.form.get("new_class") != ''):
                app.db.sadd('labels', request.form["new_class"])
            elif ("new_subclass" in request.form) and (request.form.get("new_subclass") != ''):
                class_name = request.form.get("class_select")
                dict_class = app.db.hgetall(class_name)
                if request.form["text_subclass"]=='':
                    dict_class[request.form["new_subclass"]] = 'Нет данных'
                else:
                    dict_class[request.form["new_subclass"]] = request.form["text_subclass"]
                class_name = ' '.join(class_name.split('$'))
                app.db.hmset(class_name, dict_class)
                return redirect('/class_data')
        except redis.exceptions.RedisError:
            return "При добавлении  произошла ошибка"
    labels = tl.read_labels_db(app.db)
    return render_template('new_data.html', labels=labels)

@app.route('/info_data', methods=['GET'])
def info_data():
    flag_label = False
    labels, info = tl.read_db(app.db)
    if len(labels):
        flag_label = True
    graphJSON = tl.create_map(labels, info)
    return render_template('info_data.html', graphJSON=graphJSON, flag_label=flag_label)

@app.route('/class_data', methods=['GET'])
def class_data():
    labels, info = tl.read_db(app.db)
    return render_template('class_data.html', labels=labels, info=info)

@app.route('/class_data/<string:name_class>/<string:name_subclass>', methods=['GET'])
def subclass_data(name_class, name_subclass):
    labels, info = tl.read_db(app.db)
    info_subclass = {'name_class': name_class, 'name_subclass': name_subclass}
    return render_template('class_data_info.html', labels=labels, info=info, info_subclass=info_subclass)

@app.route('/class_data/<string:name_class>/<string:name_subclass>/del', methods=['GET'])
def subclass_data_del(name_class, name_subclass):
    dict_class = app.db.hgetall(name_class)
    if name_subclass in dict_class:
        dict_class.pop(name_subclass, None)
        app.db.delete(name_class)
        if dict_class:
            app.db.hmset(name_class, dict_class)
    return redirect('/class_data')

if __name__ == '__main__':
    app.run(debug=False)
    

app.db.close()