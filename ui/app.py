import streamlit as st

import plotly.express as px
from services_call import Simcel as cel
from services_call import Yfin as fin

st.set_page_config(page_title="CEL project", layout='wide')

# Initialization
if 'favorites' not in st.session_state:
    st.session_state['favorites'] = set()
if 'current_code' not in st.session_state:
    st.session_state['current_code'] = ''
if 'period' not in st.session_state:
    st.session_state['period'] = ''


#=================== > Section 3 < =======================#

st.header(':red[1. Cleaned CEL data]')
pad, ct = st.columns([1, 12])

ct.subheader('1.1. Simcel data')

simcel_data = cel.simcel_data()
ct.dataframe(simcel_data, use_container_width=True)


ct.subheader('1.2. All outlets')

outlets_data = cel.outlets_data()
ct.dataframe(outlets_data, use_container_width=True)


ct.subheader('1.3. All items')

items_data = cel.items_data()
ct.dataframe(items_data, use_container_width=True)


#=================== > Section 3 < =======================#

st.header(':red[2. Data exploration]')

pad, ct = st.columns([1, 12])

# Pie chart 1
ct.subheader('2.1. Number of outlet based on outlet attibute' )
fields = ['Outlet_Size', 'Outlet_Type', 'Outlet_Location_Type']
# dropdown selection
outlet_attr = ct.selectbox('Choose attribute', fields)
# fetch data
pie_1_data = cel.pie_chart_1(outlet_attr)
col1, col2 = ct.columns([1, 2])

col1.dataframe(pie_1_data)

fig = px.pie(pie_1_data, names=outlet_attr, 
            values='Num',
            height=300, width=200
            )
fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
col2.plotly_chart(fig, use_container_width=True)

# Pie chart 2
ct.subheader('2.2. Proportion of items by type')

field_2 = 'Item_Type'
pie_2_data = cel.pie_chart_2(field_2)
col2_1, col2_2 = ct.columns([1, 2])

col2_1.dataframe(pie_2_data)

fig_2 = px.pie(pie_2_data, names=field_2, 
            values='Num',
            height=300, width=200
            )

fig_2.update_layout(margin=dict(l=20, r=20, t=30, b=0),)

col2_2.plotly_chart(fig_2, use_container_width=True)

# bar chart 2
ct.subheader('2.3. Sales of outlets')
outlet_sale_data = cel.outlet_sales()

col3_1, col3_2 = ct.columns([1, 2])
col3_1.dataframe(outlet_sale_data)
fig_3 = px.bar(outlet_sale_data, x='Outlet_Identifier', y='Total sales')
col3_2.plotly_chart(fig_3, use_container_width=False)


#=================== > Section 3 < =======================#

st.header(":red[3. Stock price app]")
pad, ct = st.columns([1, 12])

# Element components
code = ct.text_input("Input code", value="NVDA", placeholder="Input code")
# The chart will come here
chart_area, side_info = ct.columns([3, 2])

placeholder = chart_area.empty()

period = chart_area.radio(
    "period", 
    ["1d", "5d", "1mo", "6mo", "1y", "5y"],
    key="1mo",
    horizontal=True,
    label_visibility='hidden'
)

import pandas as pd
import utils

# Actions

if code != st.session_state['current_code']:
    st.session_state['current_code'] = code
if period != st.session_state['period']:
    st.session_state['period'] = period # Update current code of session
    
ticket_data = pd.DataFrame(fin.fetch(code, period))
fig_stock = utils.draw_stock_history(ticket_data, period=period)

placeholder.plotly_chart(fig_stock, use_container_width=True)

with side_info:
    add_fav = side_info.checkbox("Add to favorite", value=False)

    if add_fav:
        cur_cod = st.session_state['current_code']
        st.session_state['favorites'].add(cur_cod.upper())
    else:
        cur_cod = st.session_state['current_code'].upper()
        if cur_cod in st.session_state['favorites']:
            st.session_state['favorites'].remove(cur_cod)


#=================== > Section 4 < =======================#

st.header(":red[3. Favorite tickers]")
pad, ct = st.columns([1, 12])

chart_area, side_info = ct.columns([3, 2])
placeholder = chart_area.empty()

import plotly.graph_objects as go

fig = go.Figure(
        data = None
    )

for cod in st.session_state['favorites']:
    _dta = pd.DataFrame(fin.fetch(cod, period))
    fig.add_trace(go.Scatter(
            x = _dta['Datetime'],
            y = _dta['Open'],
            mode='lines', 
            name=cod
        )
    )

placeholder.plotly_chart(fig)