from pymongo import MongoClient
from backend.config import DB_NAME, DB_PASSWORD, DB_USERNAME
from backend.api.clashroyale import fetch_player_data, fetch_top_players

def __init__(self) -> None:
        self.__connection_string = f'mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@cluster0.cek6z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
        self.__database_name = DB_NAME
        self.__client = None


def get_database():
    uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@cluster0.cek6z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    db = client[DB_NAME]
    return db


def save_player_data(player_data):
    db = get_database()
    players_collection = db['players']
    players_collection.insert_one(player_data)

def save_matches_data(player_tag, battles):
    db = get_database()
    matches_collection = db['matches']
    
    for battle in battles:
        match_document = {
            "player_tag": player_tag,
            "result": "win" if battle['team'][0]['crowns'] > battle['opponent'][0]['crowns'] else "loss",
            "cards_used": [card['name'] for card in battle['team'][0]['cards']],
            "timestamp": battle['battleTime'], 
            "opponent": battle['opponent'][0]['tag'],
            "battle_mode": battle['type']
        }
        
        matches_collection.insert_one(match_document)

def save_top_players():
    player_tags = fetch_top_players()
    if player_tags:
        for tag in player_tags:
            player_data = fetch_player_data(tag.strip('#')) 
            if player_data:
                save_player_data(player_data)
