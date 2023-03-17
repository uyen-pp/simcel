import streamlit as st

import plotly.express as px
from services_call import Simcel as cel

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
ct.header('Cleaned Data')

ct.subheader('1. Simcel data')

simcel_data = cel.simcel_data()
ct.dataframe(simcel_data, use_container_width=True)


ct.subheader('2. All outlets')

outlets_data = cel.outlets_data()
ct.dataframe(outlets_data, use_container_width=True)


ct.subheader('3. All items')

items_data = cel.items_data()
ct.dataframe(items_data, use_container_width=True)

ct.header('Data exploration')

# Pie charts

# Pie chart 1
ct.subheader('1. Number of outlet based on outlet attibute' )
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
ct.subheader('2. Proportion of items by type')

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
ct.subheader('2. Sales of outlets')
outlet_sale_data = cel.outlet_sales()

col3_1, col3_2 = ct.columns([1, 2])
col3_1.dataframe(outlet_sale_data)
fig_3 = px.bar(outlet_sale_data, x='Outlet_Identifier', y='Total sales')
col3_2.plotly_chart(fig_3, use_container_width=False)

