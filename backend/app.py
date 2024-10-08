from flask import Flask, request, jsonify
from flask_cors import CORS 
from backend.api.clashroyale import fetch_all_battles
from backend.controllers.player_controller import  win_loss_cards, zebra_victories, combo_percent
from backend.controllers.cards_controller import get_decks_percent
from backend.database.mongodb import initialize_database, get_database

app = Flask(__name__)

CORS(app)
CORS(app, origins=["http://127.0.0.1:5500"])



with app.app_context():
   initialize_database() 
    
    
@app.route('/cards')
def get_card_names():
    try:
        db = get_database()
        cards_collection = db['cards']
        # Busca todas as cartas e retorna apenas o campo 'name'
        cards = cards_collection.find({}, {'_id': 0, 'name': 1, })
        
        # Extrai os nomes das cartas e os transforma em uma lista
        card_names = [card['name'] for card in cards]
        
        return card_names
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Rota para obter informações do jogador


@app.route('/win-loss-percentage', methods=['POST'])
def calculate_win_loss_percentage():
    data = request.json
    

    card_name = data.get('selected_cards', [])
    start_date = data.get('start_date', 0)  
    end_date = data.get('end_date', 0)
    
    if not card_name:
        return jsonify({"error": "Nome da carta é obrigatório."}), 400
    
    
    result = win_loss_cards(card_name, start_date, end_date)
    return jsonify(result)



@app.route('/combo-percent', methods=['POST'])
def calculate_combo_percent():
    data = request.json
    

    card_name = data.get('selected_cards', [])
    percent = data.get('percent', 0) 
    start_date = data.get('start_date', 0)  
    end_date = data.get('end_date', 0)
    
    if not card_name:
        return jsonify({"error": "Nome da carta é obrigatório."}), 400
    
    
    result = combo_percent(card_name, percent, start_date, end_date)
    print('result', result)
    return jsonify(result)


@app.route('/zebra-victories', methods=['POST'])
def calculate_zebras():
    data = request.json

    card_name = data.get('card_name', []) 
    start_date = data.get('start_date', 0)  
    end_date = data.get('end_date', 0)      
    percent = data.get('percent_diff', 7)  

    if not card_name:
        return jsonify({"error": "Nome da carta é obrigatório."}), 400

    result = zebra_victories(card_name, start_date, end_date, percent)
    return jsonify(result)
    


@app.route('/battles', methods=['GET'])
def test():
    batalha = fetch_all_battles()
    return batalha

@app.route('/decks', methods=['POST'])
def get_decks():
    data = request.json
    

    start_date = data.get('start_date', 0)  # Assumindo que você enviará o timestamp no frontend
    end_date = data.get('end_date', 0)
    min_win_percentage = float(data.get('min_win_percentage', 0))

    # Chama a função que executa a consulta no banco de dados
    decks = get_decks_percent(start_date, end_date, min_win_percentage)
    return jsonify(decks)



if __name__ == '__main__':
    app.run(debug=True)

