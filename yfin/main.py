import os
import json
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel
import yfinance as yf

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

with open("./config.json") as f:
    config = json.load(f)

class Output(BaseModel):
    status = 100
    data: str
     
class InputModel(BaseModel):
    code: str
    period: str

app = FastAPI()


@app.post("/data")
def fetch_data(inp:InputModel) -> Output:

    dta = yf.Ticker(inp.code)
    
    interval_map = {
        '1D': '5M',
        '5D': '30m',
        '1MO': '1d',
        '6MO': '1d',
        '1Y': '1d',
        '5Y': '5d'
    }

    interval = interval_map[inp.period.upper()]
  
    dta = dta.history(period=inp.period, interval=interval)

    dta.reset_index(drop=False, inplace=True)

    # [['Open', 'Volume']]
    if 'Date' in dta.columns:
        dta.rename({'Date': 'Datetime'}, axis=1, inplace=True)

    dta['Datetime'] = dta['Datetime'].apply(lambda x: x.to_datetime64()).apply(lambda x: str(x))
    
    dta = dta[['Datetime', 'Open', 'Close', 'High', 'Low', 'Volume']]

    return Output(status=200, data=dta.to_json())


@app.get("/")
async def root(): 
    return {"message": "Hi I'm Mei <3"}
