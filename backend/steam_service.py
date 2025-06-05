import requests

# Lista de juegos a consultar
GAME_IDS = [
    440, 570, 730
]

def fetch_game_data_for_database(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    if not data.get(str(app_id), {}).get("success"):
        return None
    
    data = data.get(str(app_id)).get("data")
    game_info = {
            "id": app_id,
            "name": data.get("name"),
            "type": data.get("type"),
            "is_free": data.get("is_free"),
            "required_age": data.get("required_age"),
            "description": data.get("short_description"),
            "website": data.get("website"),
            "header_image": data.get("header_image"),
            #"screenshots": data.get("screenshots", []),
            "price": data.get("price_overview", {}).get("final_formatted", "Gratis"),
            #"genres": [g["description"] for g in data.get("genres", [])],
            #"category_ids": data.get("categories"),
            #"videos": [m.get("mp4", {}).get("max") for m in data.get("movies", []) if m.get("mp4")]
        }
    return game_info

def fetch_game_data(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    if not data.get(str(app_id), {}).get("success"):
        return None
    
    data = data.get(str(app_id)).get("data")
    game_info = {
            "id": app_id,
            "name": data.get("name"),
            "type": data.get("type"),
            "is_free": data.get("is_free"),
            "required_age": data.get("required_age"),
            "description": data.get("short_description"),
            "website": data.get("website"),
            "header_image": data.get("header_image"),
            "screenshots": data.get("screenshots", []),
            "price": data.get("price_overview", {}).get("final_formatted", "Gratis"),
            "genres": [g["description"] for g in data.get("genres", [])],
            "category_ids": data.get("categories"),
            "videos": [m.get("mp4", {}).get("max") for m in data.get("movies", []) if m.get("mp4")]
        }
    return game_info

def get_all_games_data():
    games = []
    categories_map = {} 

    for app_id in GAME_IDS:
        data = fetch_game_data_for_database(app_id)
        if not data:
            continue

        #for cat in data.get("categories", []):
        #    categories_map[cat["id"]] = cat["description"]

    
        games.append(data)
    

    return games, categories_map