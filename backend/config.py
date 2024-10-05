from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Acessar as variáveis do .env
API_KEY = os.getenv('AUTHORIZATION')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

