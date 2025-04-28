from textwrap import indent
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json

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


@app.route("/api/anime/<int:anime_id>")
def get_anime(anime_id):
    # Проверяем кеш
    if anime_id in ANIME_CACHE:
        return jsonify(ANIME_CACHE[anime_id])

    try:
        mal_data, consument_data = fetch_data_from_mal_and_consument(anime_id)

        # Форматируем данные
        anime_data = {
            "id": anime_id,
            "title": mal_data.get("title"),
            "title_english": consument_data.get("title", {}).get("english"),
            "title_japanese": consument_data.get("title", {}).get("romaji"),
            "image": mal_data.get("images", {}).get("webp", {}).get("image_url"),
            "large_image": mal_data.get("images", {}).get("webp", {}).get("large_image_url"),
            "youtube_embed": mal_data.get("trailer", {}).get("embed_url"),
            "score": mal_data.get("score"),
            "scored_by": mal_data.get("scored_by"),
            "type": mal_data.get("type"),
            "source": mal_data.get("source"),
            "episodeDuration": consument_data.get("duration"),
            "totalEpisodes": consument_data.get("totalEpisodes"),
            "currentEpisode": consument_data.get("currentEpisode"),
            "status": consument_data.get("status"),
            "releaseDate": consument_data.get("releaseDate"),
            "startDate": consument_data.get("startDate"),
            "endDate": consument_data.get("endDate"),
            "nextAiringEpisode": consument_data.get("nextAiringEpisode"),
            "rating": mal_data.get("rating"),
            "season": mal_data.get("season"),
            "year": mal_data.get("year"),
            "synopsis": consument_data.get("description"),
            "genres": [genre.get("name") for genre in mal_data.get("genres", [])],
        }

        return jsonify(anime_data)

    except Exception as e:
        print(e)
        return jsonify({"error": "Anime not found"}), 404

def fetch_mal(anime_id):
    """
    Функция для получения данных с MyAnimeList по ID
    """
    r = requests.get(f"https://api.jikan.moe/v4/anime/{anime_id}")
    return r.json()["data"]

def fetch_consument_by_name(anime_name):
    """
    Функция для поиска аниме в Consument API (Anilist) по названию
    """
    r = requests.get(f"http://0.0.0.0:3000/meta/anilist/{anime_name}")
    return r.json()

def fetch_data_from_mal_and_consument(anime_id):
    """
    Получаем данные сначала с MyAnimeList, затем с Consument API, используя название
    """
    mal_data = fetch_mal(anime_id)
    anime_name = mal_data["title"]

    consument_data = fetch_consument_by_name(anime_name)

    consument_anime_request = requests.get(f"http://0.0.0.0:3000/meta/anilist/info/{consument_data["results"][0]["id"]}")

    return mal_data, consument_anime_request.json()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
