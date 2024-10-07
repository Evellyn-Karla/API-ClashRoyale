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

def win_loss_cards(card_names, start_date, end_date):
    db = get_database()
    battles_collection = db['battles']

    start_time = format_to_timestamp(start_date)
    end_time = format_to_timestamp(end_date)
    
    pipeline = [
        {
            "$match": {
                "cards_used": {"$all": [{"$elemMatch": {"$eq": card}} for card in card_names]},  # Usa $all para todas as cartas
                "timestamp": {
                    "$gte": start_time,
                    "$lte": end_time
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "total_battles": {"$sum": 1},
                "wins": {
                    "$sum": {
                        "$cond": [{"$eq": ["$result", "win"]}, 1, 0]
                    }
                }
            }
        },
        {
            "$project": {
                "total_battles": 1,
                "wins": 1,
                "losses": {
                    "$subtract": ["$total_battles", "$wins"]
                },
                "win_percentage": {
                    "$multiply": [{"$divide": ["$wins", "$total_battles"]}, 100]
                },
                "loss_percentage": {
                    "$multiply": [{"$divide": [{"$subtract": ["$total_battles", "$wins"]}, "$total_battles"]}, 100]
                }
            }
        }
    ]

    # Executar a agregação
    result = list(battles_collection.aggregate(pipeline))
    if not result:
        return {"total_battles": 0, "wins": 0, "losses": 0, "win_percentage": 0, "loss_percentage": 100}  # Retorne um resultado padrão se não houver partidas

    return result[0]
