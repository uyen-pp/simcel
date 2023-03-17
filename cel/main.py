import os
import json
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

with open("/Users/uyen/simcel/config.json") as f:
    config = json.load(f)

df_items = pd.read_csv(os.path.join(config["DATA"]["root"], config["DATA"]["items"]))
df_outlets = pd.read_csv(os.path.join(config["DATA"]["root"], config["DATA"]["outlets"]))
df_simcel = pd.read_csv(os.path.join(config["DATA"]["root"], config["DATA"]["simcel"]))

class Output(BaseModel):
    status = 100
    data: str
     
class InputModel(BaseModel):
    data: str

@app.post("/pie")
def get_data_pie_chart(inp:InputModel) -> Output:
    attr = inp.data
    
    dta = df_outlets[['Outlet_Identifier', attr]].dropna()
    dta = dta.groupby(attr).count()
    dta.reset_index(drop=False, inplace=True)
    dta.rename({'Outlet_Identifier': 'Num'}, axis=1, inplace=True)
    return Output(status=200, data=dta.to_json())

@app.post("/pie2")
def get_data_pie_chart(inp:InputModel) -> Output:
    attr = inp.data
    
    dta = df_items[['Item_Identifier', attr]].dropna()
    dta = dta.groupby(attr).count()
    dta.reset_index(drop=False, inplace=True)
    dta.rename({'Item_Identifier': 'Num'}, axis=1, inplace=True)
    return Output(status=200, data=dta.to_json())

@app.post("/outlets")
def get_data_pie_chart_2() -> Output:
    dta = df_outlets.to_json()
    return Output(status=200, data=dta)

@app.post("/items")
def get_data_() -> Output:
    dta = df_items.to_json()
    return Output(status=200, data=dta)

@app.post("/simcel")
def get_data_() -> Output:
    dta = df_simcel.to_json()
    return Output(status=200, data=dta)

@app.post("/outlet_sales")
def get_data_pie_chart() -> Output:

    dta = df_simcel[['Outlet_Identifier', 'Item_Outlet_Sales']].dropna()
    dta = dta.groupby('Outlet_Identifier').sum()
    dta.reset_index(drop=False, inplace=True)
    dta.rename({'Item_Outlet_Sales': 'Total sales'}, axis=1, inplace=True)

    return Output(status=200, data=dta.to_json())

@app.get("/")
async def root(): 
    return {"message": "Hello World"}


