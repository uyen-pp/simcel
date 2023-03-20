import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def draw_stock_history(df, period):
    fig = go.Figure(
        data = [go.Scatter(
            x = df['Datetime'],
            y = df['Open'],
            mode='lines', 
        )]
    )
    
    if period.upper() == '5D':
        fig = fig.update_xaxes(
            rangebreaks=[
                dict(bounds=[20, 13.5], pattern="hour", ), 
            ],
            tickformat="%H:%M\n%d-%b",
            dtick = 'm1'
        )
    elif period.upper() in '1MO':
        fig = fig.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "mon"]), #hide weekends
            ],
            ticklabelmode="period",
            dtick = 'D1',
            tickformat="%d\n%B",
        )
        
    elif period.upper() in ['6MO', '1Y']:
        fig = fig.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "mon"]), #hide weekends
            ],
            dtick="M1",
            tickformat="%b\n%Y",
            ticklabelmode="period"
        )

    
    elif period.upper() == '5Y':
        fig = fig.update_xaxes(
            dtick="M12")


    return fig