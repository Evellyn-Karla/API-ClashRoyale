from flask import Flask, request, jsonify
from flask_cors import CORS 
from backend.api.clashroyale import fetch_all_battles,fetch_battle_data
from backend.controllers.player_controller import get_player_info, win_loss_cards
from backend.database.mongodb import initialize_database

app = Flask(__name__)

CORS(app)
CORS(app, origins=["http://127.0.0.1:5500"])



with app.app_context():
   initialize_database() 
    
    

@app.route('/')
def home():
    #battles = fetch_all_battles()
    battles = fetch_battle_data('#UUQ9G902P')
    return battles

# Rota para obter informações do jogador
@app.route('/player/<player_tag>', methods=['GET'])
def player(player_tag):
    return get_player_info(player_tag)


@app.route('/win-loss-percentage', methods=['POST'])
def calculate_win_loss_percentage():
    data = request.json
    

    card_name = data.get('card_name', '')
    start_date = data.get('start_date', 0)  # Assumindo que você enviará o timestamp no frontend
    end_date = data.get('end_date', 0)
    
    if not card_name:
        return jsonify({"error": "Nome da carta é obrigatório."}), 400
    
    
    result = win_loss_cards(card_name, start_date, end_date)
    print(result)
    return jsonify(result)


@app.route('/battles', methods=['GET'])
def test():
    batalha = fetch_all_battles()
    return batalha

if __name__ == '__main__':
    app.run(debug=True)
