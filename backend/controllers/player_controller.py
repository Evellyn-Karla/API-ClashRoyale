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
            "total_battles": {"$sum": 1},  # Conta o número total de batalhas
            "wins": {
                "$sum": {
                    "$cond": [{"$eq": ["$result", "win"]}, 1, 0]  # Contagem de vitórias
                }
            },
            "losses": {
                "$sum": {
                    "$cond": [{"$eq": ["$result", "loss"]}, 1, 0]  # Contagem de derrotas
                }
            }
        }
    },
    {
        "$project": {
            "total_battles": 1,  # Total de batalhas
            "wins": 1,  # Total de vitórias
            "losses": 1,  # Total de derrotas
            "win_percentage": {
                "$multiply": [{"$divide": ["$wins", "$total_battles"]}, 100]  # Cálculo de porcentagem de vitórias
            },
            "loss_percentage": {
                "$multiply": [{"$divide": ["$losses", "$total_battles"]}, 100]  # Cálculo de porcentagem de derrotas
            }
        }
    }
]

    # Executar a agregação
    result = list(battles_collection.aggregate(pipeline))
    if not result:
        return {"total_battles": 0, "wins": 0, "losses": 0, "win_percentage": 0, "loss_percentage": 0} 

    return result[0]


def zebra_victories(card_name, start_date, end_date, percent):
    db = get_database()
    battles_collection = db['battles']

    
    start_time = format_to_timestamp(start_date)
    end_time = format_to_timestamp(end_date)
    
   
    pipeline = [
        {
            "$match": {
                "cards_used": {"$eq": card_name},  
                "timestamp": {
                    "$gte": start_time,
                    "$lte": end_time
                },
                "lost_crowns": {"$gte": 2}, 
                "result": "win"  
            }
        },
        {
            "$addFields": {
                "trophy_difference": {
                    "$subtract": ["$opponent_trophies", "$player_trophies"]  
                },
                "required_difference": {
                    "$multiply": ["$player_trophies", percent / 100]  
                }
            }
        },
        {
            "$match": {
                "$expr": {
                    "$lte": ["$trophy_difference", "$required_difference"] 
                }
            }
        },
        {
            "$count": "total_victories"  
        }
    ]

    
    result = list(battles_collection.aggregate(pipeline))
    
   
    if not result:
        return {"total_victories": 0}

    
    return result[0]

def combo_percent(card_names, percent, start_date, end_date):
    db = get_database()
    battles_collection = db['battles']

    start_time = format_to_timestamp(start_date)
    end_time = format_to_timestamp(end_date)
    
    pipeline = [
        {
            "$match": {
                "cards_used": {"$all": [{"$elemMatch": {"$eq": card}} for card in card_names]},  # Filtra todas as cartas
                "timestamp": {
                    "$gte": start_time,
                    "$lte": end_time
                }
            }
        },
        {
            "$group": {
                "_id": "$cards_used",  # Agrupa por combinação de cartas
                "total_battles": {"$sum": 1},  # Conta o número total de batalhas
                "wins": {
                    "$sum": {
                        "$cond": [{"$eq": ["$result", "win"]}, 1, 0]  # Contagem de vitórias
                    }
                },
                "losses": {
                    "$sum": {
                        "$cond": [{"$eq": ["$result", "loss"]}, 1, 0]  # Contagem de derrotas
                    }
                }
            }
        },
        {
            "$project": {
                "total_battles": 1,
                "wins": 1,
                "losses": 1,
                "win_percentage": {
                    "$multiply": [{"$divide": ["$wins", "$total_battles"]}, 100]  # Calcula a porcentagem de vitórias
                }
            }
        },
        {
            "$match": {  # Filtra os resultados onde a porcentagem de vitórias é maior que "percent"
                "win_percentage": {"$gte": percent}
            }
        },
        {
            "$sort": {"win_percentage": -1}  # Ordena os resultados pela maior porcentagem de vitórias
        }
    ]
    
    result = list(battles_collection.aggregate(pipeline))
    if not result:
        return []

    return result[0]

