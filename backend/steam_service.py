import requests

# Lista de juegos a consultar
GAME_IDS = [
    440, 570, 730, 578080, 271590, 292030, 359550, 252490, 381210, 105600,
    275850, 346110, 812140, 1091500, 1174180, 230410, 1085660, 1245620, 945360,
    8930, 620, 400, 550, 10, 70, 80, 221100, 513710, 1222670, 1063730, 1604030,
    1222140, 1716740, 289070, 1172620, 1811260, 552500, 108600, 703080, 1551360,
    1250410, 1056960, 1938090, 1675200, 39210, 1623730, 1693980
]

def fetch_game_data(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    if not data.get(str(app_id), {}).get("success"):
        return None
    
    data = data.get(str(app_id)).get("data")
    print(data)
    game_info = {
            "id": app_id,
            "name": data.get("name"),
            "description": data.get("short_description"),
            "header_image": data.get("header_image"),
            "price": data.get("price_overview", {}).get("final_formatted", "Gratis"),
            "genres": [g["description"] for g in data.get("genres", [])],
            "category_ids": data.get("categories")
        }
    return game_info

def get_all_games_data():
    games = []
    categories_map = {} 

    for app_id in GAME_IDS:
        data = fetch_game_data(app_id)
        if not data:
            continue

        # Mapear categorías
        for cat in data.get("categories", []):
            categories_map[cat["id"]] = cat["description"]

    
        games.append(data)

    return games, categories_map