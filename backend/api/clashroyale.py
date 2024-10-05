import requests
from backend.config import API_KEY


def fetch_player_data(player_tag):
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.get(f'https://api.clashroyale.com/v1/players/%23{player_tag}', headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_top_players():
    url = 'https://api.clashroyale.com/v1/locations/57000006/rankings/players'
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    
    params = {
        'limit': 100 
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        players = response.json().get('items', [])
        player_tags = [player['tag'] for player in players] 
        return player_tags
    else:
        return None