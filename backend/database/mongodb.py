from pymongo import MongoClient
from backend.config import DB_NAME, DB_PASSWORD, DB_USERNAME
from backend.api.clashroyale import fetch_player_data, fetch_top_players, fetch_all_battles, fetch_cards
from datetime import datetime
_client = None

def get_database():
    global _client
    if _client is None:
        uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@cluster0.cek6z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        _client = MongoClient(uri)
    db = _client[DB_NAME]
    return db

def save_cards_data(cards):
    try:
        db = get_database()
        cards_collection = db['cards']
        
        sorted_cards = sorted(cards, key=lambda x: x['name'])
        
        cards_collection.insert_many(sorted_cards)
        print(f"{len(sorted_cards)} cartas salvas com sucesso.")
        
    except Exception as e:
        print(f"Erro ao salvar dados da carta: {e}")


def save_player_data(player_data):
    try:
        db = get_database()
        players_collection = db['players']
        players_collection.insert_one(player_data)
    except Exception as e:
        print(f"Erro ao salvar dados do jogador {player_data['tag']}: {str(e)}")


def save_battles_data(battles):
    db = get_database()
    battles_collection = db['battles']
    
    for battle in battles:
        battle_document = {
            "player_tag": battle['team'][0]['tag'],
            "result": "win" if battle['team'][0]['crowns'] > battle['opponent'][0]['crowns'] else "loss",
            "lost_crowns": battle['opponent'][0]['crowns'],
            "win_crowns": battle['team'][0]['crowns'],
            "player_trophies": battle['team'][0].get('startingTrophies', 0),  
            "opponent_trophies": battle['opponent'][0].get('startingTrophies', 0),
            "cards_used": [card['name'] for card in battle['team'][0]['cards']],
            "timestamp": battle['battleTime'], 
            "opponent_tag": battle['opponent'][0]['tag'],
            "battle_mode": battle['type']
        }
        
        battles_collection.insert_one(battle_document)



def save_top_players():
    try:
        player_tags = fetch_top_players()
        if player_tags:
            for tag in player_tags:
                try:
                    player_data = fetch_player_data(tag.replace("#", "%23")) 
                    if player_data:
                        save_player_data(player_data)
                except Exception as e:
                    print(f"Erro ao salvar dados do jogador {tag}: {str(e)}")
        return 'sucesso'
    except Exception as e:
        print(f"Erro ao salvar top players: {str(e)}")
        return 'erro'
    


# Formatação de hora

def format_to_timestamp(data):
    # Converte a string ISO para um objeto datetime
    n_data = datetime.fromisoformat(data.replace('Z', '+00:00'))  # Ajuste para o formato compatível
    # Formata para o formato desejado
    data_formatada = n_data.strftime('%Y%m%dT%H%M%S.000Z')
    return data_formatada



# inicializacao do banco

def clear_collections():
    db = get_database()
    players_collection = db['players']
    players_collection.delete_many({}) 

    
    battles_collection = db['battles']
    battles_collection.delete_many({})  
  
    """ cards_collection = db['cards']
    cards_collection.delete_many({})  
 """
    print("Todas as coleções foram limpas.")

def initialize_database():
    clear_collections()

    result = save_top_players()
    if result != 'sucesso':
        print("Erro ao salvar jogadores.")
        return

    
    battles = fetch_all_battles()
    if battles:
        save_battles_data(battles)
        print("Dados de batalhas salvos com sucesso.")
    else:
        print("Nenhuma batalha encontrada para salvar.")

   
    """ cards = fetch_cards()
    if cards:
        save_cards_data(cards)
        print("Dados salvos com sucesso.")
    else:
        print("erro")
 """
   



