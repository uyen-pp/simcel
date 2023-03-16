import streamlit as st
import pandas as pd
from os import path as osp
import os 


st.set_page_config(page_title="CEL project", layout="wide")
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        width: 400px;
        margin-left: -400px;
    }
     
    """,
    unsafe_allow_html=True,
)

# Layout
sb, ct = st.columns([1, 4])

# Object notation


ROOT_DIR = './simcel' # change this
DATA_PATH = osp.join(ROOT_DIR, 'data', 'raw')
raw_data_file = osp.abspath(osp.join(DATA_PATH, 'simcel-6pk70-1jk5iqdp-train_v9rqX0R.csv'))
df = pd.read_csv(raw_data_file)

ct.write('Data')
ct.experimental_data_editor(df, use_container_width=True)

ct.write('Some charts')
