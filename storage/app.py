from flask import Flask, send_from_directory, abort,request
import json
import uuid

app = Flask(__name__)

# 
# Все Эндпоинты начинаются с /storage/ 
# 

# path to csv
PATH = f'csv/'

# метод принимает json с суммами столбцов запрашиваемого файла
@app.route("/storage/store_json", methods=['POST'])
def store_json():
    # создаём уникальный id для названия файла
    json_uid = uuid.uuid4().hex
    r = request.json
    # сохраняем данные в файл
    with open(f'./json/{json_uid}.json', 'w') as json_file:
        json.dump(r, json_file)
    # уменьшаем счётчик активных задач
    decrease_counter()
    return(json.dumps({"Task started, your id":json_uid}))

# увеличиваем счётчик активных задач на вычисление
@app.route("/storage/increase_counter", methods=['POST'])
def increase_counter():
    with open('counter.json', "r+") as f:
        data = json.load(f)
        data["counter"] = data["counter"] + 1
        f.seek(0)
        f.write(json.dumps(data))
        f.truncate()
        return("",200)

# уменьшаем счётчик активных задач на вычисление
def decrease_counter():
    with open('counter.json', "r+") as f:
        data = json.load(f)
        data["counter"] = data["counter"] - 1
        f.seek(0)
        f.write(json.dumps(data))
        f.truncate()
        return("",200)

# возвращает количество активных задач из counter.json
@app.route("/storage/get_counter", methods=['GET'])
def get_counter():
    with open('counter.json', "r") as f:
        data = json.load(f)
        tasks_conuter = data['counter']
        return(json.dumps({"ongoing_tasks":tasks_conuter}))

# возвращает файл с указанным именем
@app.route("/storage/get_csv/<csv_id>", methods=['POST','GET'])
def get_csv(csv_id):
    filename = f"{csv_id}"
    try:
        return send_from_directory(PATH, filename)
    except FileNotFoundError:
        abort(404)

# возвращает вычисленные суммы по id задачи
@app.route("/storage/get_json/<json_uuid>", methods=['POST','GET'])
def some_j(json_uuid):
    with open(f'./json/{json_uuid}.json', 'r') as json_file:
        my_dict = {}
        my_dict = json.load(json_file)
        return(json.dumps(my_dict))

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)
