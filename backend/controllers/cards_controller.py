from pymongo import MongoClient
from datetime import datetime
from backend.database.mongodb import get_database, format_to_timestamp

def get_decks_percent(start_date, end_date, min_win_percentage):
    
    db = get_database()
    battles_collection = db['battles']
    
    start_time = format_to_timestamp(start_date)
    end_time = format_to_timestamp(end_date)
    
    # Pipeline de agregação
    pipeline = [
        {
            "$match": {
                "timestamp": {
                    "$gte": start_time,
                    "$lte": end_time
                }
            }
        },
        # Verificar que o deck tem exatamente 8 cartas
        {
            "$match": {
                "$expr": {
                    "$eq": [{"$size": "$cards_used"}, 8]
                }
            }
        },
        {
            "$group": {
                "_id": "$cards_used",  # Agrupar por cartas usadas (deck)
                "total_wins": {
                    "$sum": {"$cond": [{"$eq": ["$result", "win"]}, 1, 0]}
                },
                "total_losses": {
                    "$sum": {"$cond": [{"$eq": ["$result", "loss"]}, 1, 0]}
                }
            }
        },
        {
            "$project": {
                "win_percentage": {
                    "$multiply": [
                        {"$divide": ["$total_wins", {"$add": ["$total_wins", "$total_losses"]}]},
                        100
                    ]
                },
                "deck": "$_id"  # Atribuir o deck usado no resultado
            }
        },
        {
            "$match": {
                "win_percentage": {"$gt": min_win_percentage}
            }
        }
    ]

    results = list(battles_collection.aggregate(pipeline))
   
    return results