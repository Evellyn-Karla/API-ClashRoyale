from backend.api.clashroyale import fetch_player_data, fetch_top_players
from backend.database.mongodb import get_database
from backend.models.player import Player
from backend.database.mongodb import format_to_timestamp


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
    battles_collection = db['battles']
    
    # Converte start_date e end_date para datetime no formato UTC (ISO 8601)
    start_time = format_to_timestamp(start_date)
    end_time = format_to_timestamp(end_date)
    
    
    
    
    query = {
        "cards_used": {"$elemMatch": {"$eq": card_name}},
        "timestamp": {
            "$gte": start_time,
            "$lte": end_time
        }
    }


    battles = list(battles_collection.find(query))
    total_battles = len(battles)

    if total_battles == 0:
        return '405'
    
    wins = len([match for match in battles if match['result'] == 'win'])
    losses = total_battles - wins
    
    win_percentage = (wins / total_battles) * 100
    loss_percentage = (losses / total_battles) * 100
    
    return {
        "total_battles": total_battles,
        "wins": wins,
        "losses": losses,
        "win_percentage": win_percentage,
        "loss_percentage": loss_percentage
    } 