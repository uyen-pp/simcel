import streamlit as st

import plotly.express as px
from services_call import Simcel as cel
from services_call import Yfin as fin
import pandas as pd
import utils

st.set_page_config(page_title="CEL project", layout='wide')

# Initialization
if 'favorites' not in st.session_state:
    st.session_state['favorites'] = set()
if 'current_code' not in st.session_state:
    st.session_state['current_code'] = ''
if 'period' not in st.session_state:
    st.session_state['period'] = ''

# primaryColor="#b11c1c"

tab1, tab2, tab3, tab4 = st.tabs(["CEL Data", "CEL Exploration", "YFIN Chart", "Favorites"])

with tab1: 
    #=================== > Section 1 < =======================#

    st.header('Cleaned CEL data')
    st.write("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
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

with tab2: 
    st.header('2. Data exploration')
    st.write("Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of de Finibus Bonorum et Malorum (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, Lorem ipsum dolor sit amet.., comes from a line in section 1.10.32.")

    pad, ct = st.columns([1, 12])

    # Pie chart 1
    ct.subheader('2.1. Number of outlet based on outlet attibute' )

    fields = ['Outlet_Size', 'Outlet_Type', 'Outlet_Location_Type']
    # dropdown selection
    outlet_attr = ct.selectbox('Choose attribute', fields)

    # fetch data
    pie_1_data = cel.pie_chart_1(outlet_attr)

    # Add padding
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

with tab3:
    st.header("3. Stock price app")
    st.write("It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).")

    pad, ct = st.columns([1, 12])

    # Element components
    input = ct.text_input("ticker", value="NVDA", placeholder="Input code", label_visibility='hidden')
    company_inf = fin.get_company_info(code=input)
    code = company_inf['ticker']

    # Some statistic
    stat_holder = ct.container()
    
    # The chart will come here
    chart_area, side_info = ct.columns([3, 2])
    
    chart_holder = chart_area.empty()

    period = chart_area.radio(
        "period", 
        ["1d", "5d", "1mo", "6mo", "1y", "5y"],
        key=3,
        horizontal=True,
        label_visibility='hidden'
    )

    # Actions
    if code != st.session_state['current_code']:
        # Check if code is valid?
        st.session_state['current_code'] = code
    if period != st.session_state['period']:
        st.session_state['period'] = period # Update current code of session

    with side_info:
        if company_inf is not None:
            st.write(f'{company_inf["description"]}')
            st.write(f'Industry: {company_inf["industry"]}')
            st.write(f'Website: {company_inf["website"]}')
            st.write(f'CEO: {company_inf["ceo"]}')
            st.write(f'Exchange: {company_inf["exchange"]}')
        else: 
            st.caption('Ticker not found. Please retry...')

    ticket_data = pd.DataFrame(fin.fetch(code, period))
    fig_stock = utils.draw_stock_history(ticket_data, period=period)

    with stat_holder:
        # st.write(company_inf)
        st.header(company_inf['company_name'])
        st.subheader(f'{company_inf["ticker"]}')
        st.caption(f'Market cap: {"{:,}".format(float(company_inf["market_cap"]))}')
    
        add_fav = st.checkbox("Add to favorite", value=False)
        if add_fav:
            cur_cod = st.session_state['current_code']
            st.session_state['favorites'].add(cur_cod.upper())
        else:
            cur_cod = st.session_state['current_code'].upper()
            if cur_cod in st.session_state['favorites']:
                st.session_state['favorites'].remove(cur_cod)

    # stat_holder.write(company_inf['description'])
    chart_holder.plotly_chart(fig_stock, use_container_width=True)
        
with tab4: 
    import plotly.graph_objects as go

    st.header("3. Favorite tickers")
    pad, ct = st.columns([1, 12])

    chart_area_4, side_info_4 = ct.columns([3, 2])

    chart_holder = chart_area_4.empty()

    period_4 = chart_area_4.radio(
        "period", 
        ["1d", "5d", "1mo", "6mo", "1y", "5y"],
        key = 4,
        horizontal=True,
        label_visibility='hidden'
    )

    def reload(tic, period):
        fig = go.Figure(
                data = None,
            )
        fig.update_yaxes(title_text='USD')

        for cod, show in tic:
            if show:
                _dta = pd.DataFrame(fin.fetch(cod, period))
                fig.add_trace(go.Scatter(
                        x = _dta['Datetime'],
                        y = _dta['Open'],
                        mode='lines', 
                        name=cod
                    )
                )
        chart_holder.plotly_chart(fig)

    checkbox_status = []

    with side_info_4:
        for s in st.session_state['favorites']:
            _ = st.checkbox(f'{s}', key=s, value=True)
            checkbox_status.append((s, _))

    reload(checkbox_status, period_4)