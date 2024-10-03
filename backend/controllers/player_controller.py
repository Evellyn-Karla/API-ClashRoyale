from api.clashroyale import fetch_player_data
from models.player import Player

def get_player_info(player_tag):
    player_data = fetch_player_data(player_tag)
    
    if player_data:
        player = Player(
            nickname=player_data['name'], trophies=player_data['trophies'], level=player_data['expLevel'],
            wins= player_data['wins'],
            losses = player_data['losses'],
            battleCount = player_data['battleCount'],
            clan = player_data['clan'])
        player.save_to_db()  
        return player_data
    else:
        return {"error": "Jogador não encontrado."}
