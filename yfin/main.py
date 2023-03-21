import os
import json
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel
import yfinance as yf

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

df_companies = pd.read_csv('./companies.csv')
df_companies.rename(dict([(o, '_'.join(o.split())) for o in df_companies.columns]), axis=1, inplace=True)

with open("./config.json") as f:
    config = json.load(f)

class OutputModel(BaseModel):
    status = 100
    data: str
     
class InputModel(BaseModel):
    code: str
    period: str

app = FastAPI()

@app.post("/data")
def fetch_data(inp:InputModel) -> OutputModel:

    tic = yf.Ticker(inp.code)
    
    interval_map = {
        '1D': '5M',
        '5D': '30m',
        '1MO': '1d',
        '6MO': '1d',
        '1Y': '1d',
        '5Y': '5d'
    }

    interval = interval_map[inp.period.upper()]
    dta = tic.history(period=inp.period, interval=interval)
    dta.reset_index(drop=False, inplace=True)

    # [['Open', 'Volume']]
    if 'Date' in dta.columns:
        dta.rename({'Date': 'Datetime'}, axis=1, inplace=True)

    dta['Datetime'] = dta['Datetime'].apply(lambda x: x.to_datetime64()).apply(lambda x: str(x))
    
    dta = dta[['Datetime', 'Open', 'Close', 'High', 'Low', 'Volume']]

    return OutputModel(status=200, data=dta.to_json())

@app.post("/company")
def get_info(inp:InputModel) -> OutputModel:
    ques = inp.code.strip().lower()
    dta = df_companies.query('@ques == ticker.str.lower() or @ques == company_name.str.lower() or @ques==short_name.str.lower()')
    
    dta = dta.iloc[0].to_dict() if len(dta) == 1 else None
    js = json.dumps(dta)
    return OutputModel(status=200, data=js)
    

@app.get("/")
async def root(): 
    return {"message": "Hi I'm Mei <3"}


import uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=10002)