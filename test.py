import requests
import os
from dotenv import load_dotenv

# Carregar as variáveis de ambiente
load_dotenv()

# Definir a chave de autorização e o playerTag (ID do jogador)
AUTH_HEADER = os.getenv('AUTHORIZATION')
player_tag = "#C2UVLQ28J"  # Substitua pela tag do jogador (inclua o #)

# Definir o endpoint para obter o log de batalhas
url = f'https://api.clashroyale.com/v1/players/{player_tag.replace("#", "%23")}/battlelog'
headers = {
    'Content-Type': 'application/json',
    'Authorization': AUTH_HEADER
}

# Fazer a requisição para a API do Clash Royale
response = requests.get(url, headers=headers)

if response.status_code == 200:
    battle_log = response.json()
    
    # Definir a carta que você quer filtrar (exemplo: "Mega Minion")
    carta_nome = "Royal Hogs"
    
    total_batalhas = 0
    vitorias = 0

    # Iterar sobre o histórico de batalhas
    for battle in battle_log:
        # Verificar se a carta foi usada no deck do jogador
        jogador_cartas = [card['name'] for card in battle['team'][0]['cards']]
        
        if carta_nome in jogador_cartas:
            total_batalhas += 1
            # Verificar se foi uma vitória
            if battle['team'][0]['crowns'] > battle['opponent'][0]['crowns']:
                vitorias += 1
    
    if total_batalhas > 0:
        porcentagem_vitorias = (vitorias / total_batalhas) * 100
        print(f'A porcentagem de vitórias da carta {carta_nome} é: {porcentagem_vitorias:.2f}%')
    else:
        print(f'A carta {carta_nome} não foi encontrada em nenhuma batalha.')

else:
    print(f"Erro ao acessar a API: {response.status_code}")
