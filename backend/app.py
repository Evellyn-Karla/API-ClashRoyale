from flask import Flask
from database.mongodb import connect_to_mongo
from api.clashroyale import fetch_player_data
from controllers.player_controller import get_player_info

app = Flask(__name__)

# Conexão com o banco de dados MongoDB
connect_to_mongo()

@app.route('/')
def home():
    return "API Clash Royale"

# Rota para obter informações do jogador
@app.route('/player/<player_tag>', methods=['GET'])
def player(player_tag):
    return get_player_info(player_tag)

if __name__ == '__main__':
    app.run(debug=True)
