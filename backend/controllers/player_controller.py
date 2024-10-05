from backend.api.clashroyale import fetch_player_data, fetch_top_players
from backend.database.mongodb import get_database
from backend.models.player import Player
from datetime import datetime

def get_player_info(player_tags):
    players_data = []
    for tag in player_tags:
        player_data = fetch_player_data(tag)
        
        if player_data:
            
            player = Player(
                nickname=player_data['name'], 
                trophies=player_data['trophies'], 
                level=player_data['expLevel'],
                wins= player_data['wins'],
                losses= player_data['losses'],
                battleCount= player_data['battleCount'],
                clan= player_data['clan']
            )
            player.save_to_db()
            
            
            players_data.append({
                "nickname": player_data['name'],
                "trophies": player_data['trophies'],
                "level": player_data['expLevel'],
                "wins": player_data['wins'],
                "losses": player_data['losses'],
                "battleCount": player_data['battleCount'],
                "clan": player_data['clan']
            })
        else:
            players_data.append({
                "error": f"Jogador com tag {tag} não encontrado."
            })
    
    return players_data

def win_loss_cards(card_name, start_date, end_date):
    db = get_database()
    matches_collection = db['matches']
    player_tags = fetch_top_players()
    
    if player_tags is None or not player_tags:
        return {"message": "Nenhum jogador encontrado."}
    
    start_time = datetime.fromtimestamp(start_date)
    end_time = datetime.fromtimestamp(end_date)
    
    query = {
        "player_tag": {"$in": player_tags},
        "cards_used": card_name,
        "timestamp": {
            "$gte": start_time,
            "$lte": end_time
        }
    }
    
    matches = list(matches_collection.find(query))
    
    total_matches = len(matches)
    if total_matches == 0:
        return {"message": "Nenhuma partida encontrada para os parâmetros fornecidos."}
    
    wins = len([match for match in matches if match['result'] == 'win'])
    losses = total_matches - wins
    
    win_percentage = (wins / total_matches) * 100
    loss_percentage = (losses / total_matches) * 100
    
    return {
        "total_matches": total_matches,
        "wins": wins,
        "losses": losses,
        "win_percentage": win_percentage,
        "loss_percentage": loss_percentage
    }

