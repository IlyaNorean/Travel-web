from flask import Flask, render_template, request, jsonify
import json


app = Flask(__name__, static_folder='static')


# Чтение данных о достопримечательностях и городах из файла JSON
with open('attractions_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Разделение данных на отдельные словари для достопримечательностей и городов
attractions_data = data.get('attractions', {}).decode("utf-8")
cities_data = data.get('cities', {}).decode("utf-8")

def search_query_in_string(query, string):
    return query.lower() in string.lower()

@app.route('/')
def index():
    return render_template('index.html', cities=cities_data)

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query').lower()
    results = []

    # Поиск городов и достопримечательностей по части названия
    for city in cities_data:
        if search_query_in_string(query, city):
            results.extend([{'type': 'attraction', 'city': city, 'attraction': a} for a in attractions_data.get(city, [])])
    for city, attractions in attractions_data.items():
        for attraction in attractions:
            if search_query_in_string(query, attraction):
                results.append({'type': 'attraction', 'city': city, 'attraction': attraction})

    return jsonify(results)

@app.route('/attraction/<city>/<attraction_name>', methods=['GET', 'POST'])
def attraction(city, attraction_name):
    # Получаем информацию о достопримечательности
    attraction_info = attractions_data.get(city, {}).get(attraction_name, {})
    return render_template('attraction.html', city=city, attraction_name=attraction_name, attraction_info=attraction_info)

if __name__ == '__main__':
    app.run(debug=False)
