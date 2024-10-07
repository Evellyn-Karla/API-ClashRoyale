import requests
from backend.config import API_KEY


def fetch_cards():
    headers = {
        'Authorization': API_KEY
    }
    response = requests.get('https://api.clashroyale.com/v1/cards', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # A API deve retornar um objeto JSON, onde as cartas estão dentro de uma chave específica (por exemplo, 'items')
        return data.get('items', [])  # 'items' é o nome provável da chave contendo as cartas
    else:
        return None

def fetch_player_data(player_tag):
    headers = {
        'Authorization': API_KEY
    }
    response = requests.get(f'https://api.clashroyale.com/v1/players/{player_tag}', headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_top_players():
    url = 'https://api.clashroyale.com/v1/locations/global/pathoflegend/2024-07/rankings/players'
    headers = {
        'Authorization': API_KEY
    }
    
    params = {
        'limit':  5
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        players = response.json().get('items', [])
        player_tags = [player['tag'] for player in players] 
        return player_tags
    else:
        return None
    
def fetch_battle_data(player_tag):
    battles_player = []
    url = f'https://api.clashroyale.com/v1/players/{player_tag.replace("#", "%23")}/battlelog'
    headers = {
        'Authorization': API_KEY
    }

    
    response = requests.get(url, headers=headers)


    
    if response.status_code == 200:
        dados = response.json()
        battles_player.extend(dados)
    else:
        print(f"Erro ao buscar dados para o jogador: {player_tag}")
        return 'erro'

    return battles_player
    
def fetch_all_battles():
    player_tags = fetch_top_players()  # Função que retorna as tags dos jogadores
    
    if player_tags:
        battles = []
        for tag in player_tags:
            battle_data = fetch_battle_data(tag)
            if battle_data != 'erro': 
                battles += battle_data
            else:
                print(f"Erro ao buscar batalhas para o jogador: {tag}")
        return battles
    else:
        print("Erro ao buscar os jogadores.")
        return []