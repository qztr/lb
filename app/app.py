from flask import Flask, abort
import pandas as pd
import json
import requests

app = Flask(__name__)

# storage api url
API_URL = 'http://storage:5000/storage'

# считываем файл и записываем суммы столбцов в resp
def summ_cols(filename):
    # проверяем валидность названия файла
    read_file(filename)
    csv_file = './data.csv'
    resp = {}
    # считываем данные из csv
    df = pd.read_csv(csv_file, sep="/?,", engine='python')
    df.columns = df.columns.str.replace('\"', '')
    for n in range(len(df.columns.tolist()) - 1):
        if (n % 10 == 0):
            total = df[f'col{n}'].sum()
            resp[f"col{n}"] = total
    return(resp)

# функция возвращает 404, если файла с таким именем нет в хранилище
def read_file(filename):
    # пытаемся получить файл из хранилища
    r = requests.post(url=f'{API_URL}/get_csv/{filename}')
    if r.status_code == 200:
        # записываем данные в локальный файл для дальнейшей обработки
        with open(filename, 'w') as csv_file:
            csv_file.write(r.text)
            csv_file.close()
        # посылаем запрос, который увеличит счётчик активныъ задач
        requests.post(url=f'{API_URL}/increase_counter')
    else:
        abort(404,"File not found")

# workers api endpoint
@app.route('/csv_name=<filename>')
def csv_name(filename):
    sum =  summ_cols(filename)
    # вычисленные суммы отправляем в хранилице в формате json
    r = requests.post(url=f'{API_URL}/store_json', json = json.dumps(sum))
    return(r.json())

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
