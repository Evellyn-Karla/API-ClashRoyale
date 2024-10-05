from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.database.mongodb import get_database
from backend.api.clashroyale import fetch_player_data
from backend.controllers.player_controller import get_player_info, win_loss_cards

app = Flask(__name__)

CORS(app)
CORS(app, origins=["http://127.0.0.1:5500"])


# Conexão com o banco de dados MongoDB
get_database()

@app.route('/')
def home():
    return "API Clash Royale"

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
    
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)