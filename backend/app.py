from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])


@app.route("/api/top-anime", methods=["GET"])
def trending_anime():
    filter_param = request.args.get("filter", "bypopularity")
    params = {"type": "tv", "filter": filter_param, "sfw": "true", "limit": 5}
    response = requests.get("https://api.jikan.moe/v4/top/anime", params=params)
    filtered_list = []
    if response.status_code == 200:
        for anime in response.json()["data"]:
            filtered_list.append(
                {
                    "mal_id": anime["mal_id"],
                    "title": anime["titles"][0]["title"],
                    "cover": anime["images"]["webp"]["image_url"],
                }
            )
        return jsonify(filtered_list)
    else:
        return jsonify({"error": "Failed to fetch data from the API"}), 500

ANIME_CACHE = {}

@app.route('/api/anime/<int:anime_id>')
def get_anime(anime_id):
    # Проверяем кеш
    if anime_id in ANIME_CACHE:
        return jsonify(ANIME_CACHE[anime_id])
    
    # Запрос к внешнему API (пример для Jikan API)
    try:
        response = requests.get(f'https://api.jikan.moe/v4/anime/{anime_id}')
        data = response.json()['data']
        
        # Форматируем данные
        anime_data = {
            'id': anime_id,
            'title': data['title'],
            'title_english': data['title_english'],
            'title_japanese': data['title_japanese'],
            'trailer': data['trailer'],
            'image': data['images']['jpg']['image_url'],
            'background': data['background'],
            'type': data['type'],
            'source': data['source'],
            'episodes': data['episodes'],
            'status': data['status'],
            'rating': data['rating'],
            'season': data['season'],
            'year': data['year'],
            'synopsis': data['synopsis'],
            'genres': [genre['name'] for genre in data['genres']],
        }
        
        # КешируемIMEIME_CACHE[anime_id] = anime_data
        return jsonify(anime_data)
    
    except Exception as e:
        print(e)
        return jsonify({'error': 'Anime not found'}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)
