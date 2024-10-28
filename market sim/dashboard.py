import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def create_dashboard(engine, trades, symbols):
    st.title("Advanced Trading Engine Simulation")

    # Performance Metrics
    st.header("Performance Metrics")
    col1, col2, col3 = st.columns(3)
    total_orders = sum(len(engine.order_books[symbol]['buy']) + len(engine.order_books[symbol]['sell']) for symbol in symbols)
    with col1:
        st.metric("Total Orders", total_orders)
    with col2:
        st.metric("Total Trades", len(trades))
    with col3:
        st.metric("Symbols Traded", len(symbols))

    # Order Book Visualization
    st.header("Order Books")
    symbol = st.selectbox("Select Symbol", symbols)
    
    col1, col2 = st.columns(2)
    with col1:
        buy_orders = engine.order_books[symbol]['buy']
        buy_df = pd.DataFrame([(o.price, o.quantity) for o in buy_orders], columns=["Price", "Quantity"])
        buy_df = buy_df.groupby("Price").sum().reset_index().sort_values("Price", ascending=False)
        fig_buy = px.bar(buy_df, x="Price", y="Quantity", title=f"Buy Orders - {symbol}")
        fig_buy.update_traces(marker_color="green")
        st.plotly_chart(fig_buy, use_container_width=True)

    with col2:
        sell_orders = engine.order_books[symbol]['sell']
        sell_df = pd.DataFrame([(o.price, o.quantity) for o in sell_orders], columns=["Price", "Quantity"])
        sell_df = sell_df.groupby("Price").sum().reset_index().sort_values("Price")
        fig_sell = px.bar(sell_df, x="Price", y="Quantity", title=f"Sell Orders - {symbol}")
        fig_sell.update_traces(marker_color="red")
        st.plotly_chart(fig_sell, use_container_width=True)

    # Trade Visualization
    st.header("Recent Trades")
    trade_df = pd.DataFrame(trades, columns=["Buy Order ID", "Sell Order ID", "Quantity", "Price"])
    trade_df['Trade ID'] = range(1, len(trade_df) + 1)
    st.dataframe(trade_df.sort_values('Trade ID', ascending=False).head(10), use_container_width=True)

    # Price Chart
    st.subheader("Price History")
    fig_price = px.line(trade_df, x='Trade ID', y='Price', title='Price History')
    st.plotly_chart(fig_price, use_container_width=True)

    # Volume Chart
    st.subheader("Volume History")
    fig_volume = px.bar(trade_df, x='Trade ID', y='Quantity', title='Trade Volume History')
    st.plotly_chart(fig_volume, use_container_width=True)