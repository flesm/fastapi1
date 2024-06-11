import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="my_app"
)


# possible set of variables
class DegreeType(Enum):
    jun = 'junior'
    mid = 'middle'
    sen = 'senior'


class Degree(BaseModel):
    id: int
    type: DegreeType


# model
class Trade(BaseModel):
    id: int
    currency: str = Field(max_length=20)  # something like parameters in django's models
    proces: str
    market: str
    rating: int = Field(ge=0)  # gives the opportunity to install the borders in user's request (ge - greater or equels)
    degree: Optional[Degree]  # class, which defines contains variables of degree


db_users = [
    {'id': 1, 'name': "Max", 'role': 'programmer'},
    {'id': 2, 'name': "Petya", 'role': 'petuh'},
    {'id': 3, 'name': "Dima", 'role': 'striper'},
    {'id': 4, 'name': "Ian", 'role': 'trader'}
]

db_trades = [
    {'id': 1, 'currency': 'BTC', 'proces': 'buy', 'market': 'Binance'},
    {'id': 2, 'currency': 'ETH', 'proces': 'sell', 'market': 'Bybit'},
    {'id': 3, 'currency': 'NOT', 'proces': 'buy', 'market': 'BingX', 'degree': {'id': 1, 'type': 'senior'}}
]


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return [user['name'] for user in db_users if user.get('id') == user_id]


@app.post("/users/{user_id}}")
def change_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get('id') == user_id, db_users))[0]
    current_user['name'] = new_name
    return {'status': 200, 'info': new_name}


# List[Trade] forms from model list and forms value trades, then add it to db_trades
@app.post('/trades')
def add_trade(trades: List[Trade]):
    db_trades.extend(trades)
    return {'status': 200, 'info': db_trades}
