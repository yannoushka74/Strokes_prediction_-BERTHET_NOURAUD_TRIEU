from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.engine import create_engine
import os
import pandas as pd

server = FastAPI(title='Stroke API')


users = {
  "Nathalie": "wonderland",
  "Pierre": "builder",
  "Yann": "mandarine"
}



df = pd.read_csv('stroke_clean.csv',sep=';')

def authenticate_user(username, password):
    authenticated_user = False
    if username in users.keys():
        if users[username] == password:
            authenticated_user = True
    return authenticated_user


@server.get('/')
def get_index():
    return {
    Response(df['id'].to_json(orient="records"), media_type="application/json")
    }

@server.get('/Authorization')
async def return_permission(username: str = 'username', password: str = 'password'):
    if authenticate_user(username=username, password=password):
        return {'username': username, 'permissions': 'Utilisateur authorisé a utiliser l''API'}
    else:
        raise HTTPException(status_code=403, detail='Authentication failed')

@server.get('/status')
async def return_status():
    '''
    returns 1 if the app is up
    '''
    return 1




