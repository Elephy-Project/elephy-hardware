import jwt
import requests

from decouple import config
from datetime import datetime, timedelta


PATH=config("TOKEN_PATH")
USERNAME=config("USERNAME")
PWD=config("PASSWORD")
SECRET_KEY=config("SECRET_KEY")
ALGORITHM=config("ALGORITHM")


class Token:
    TOKEN = None
    
    async def fetch_token():
        if Token.TOKEN == None or Token.is_token_expired():
            response = requests.post(PATH, data={"username": USERNAME, "password": PWD})
            Token.TOKEN = response.json()["access_token"]
        return Token.TOKEN


    def is_token_expired():
        try:
            payload = jwt.decode(Token.TOKEN, SECRET_KEY, algorithms=[ALGORITHM])
            exp = payload["exp"]
            if exp is None:
                return False
            return datetime.utcfromtimestamp(exp) < datetime.utcnow() - timedelta(minutes=2)
        except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidTokenError) as e:
            print(f"An error occurred: {e}")
