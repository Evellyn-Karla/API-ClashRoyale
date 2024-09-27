import requests
from mongo.models.connection import DBConnectionHandler

cartas_url = 'https://api.clashroyale.com/v1/cards'
headers= {
    'Content-type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjMzYjFiMGVlLTAxOTctNDk2ZC1hN2Q0LTgxY2QzMTU1NjM1YiIsImlhdCI6MTcyNzEwODUzNiwic3ViIjoiZGV2ZWxvcGVyLzkzZDZmZjc3LTg2MjQtZjA4Yy1jNjQzLWM0YWY0MmRhMzE3NSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIyMDEuMTQwLjIzOS43NSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.VYvav6DuplGpR9Ry871aEOn9jCwU_1GUsAfedJbWPwZ4lkNO73Xt8CvnbBAxbCUcMUPy4b2Xur5nvqq9NgQ4DQ'
}

response = requests.get(url=cartas_url, headers=headers)

if (response.status_code == 200):
    data = response.json()
    db_handle = DBConnectionHandler()
    db_handle.connectDB()
    conn = db_handle.get_db_connection()

    collection = conn.get_collection('Cartas')

    items = data['items'] 
    collection.insert_many(items)  
else:
    print(f"Erro ao acessar a API: {response.status_code}")