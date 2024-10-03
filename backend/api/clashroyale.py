import requests
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv('AUTHORIZATION')

def fetch_player_data(player_tag):
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(f'https://api.clashroyale.com/v1/players/%23{player_tag}', headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
