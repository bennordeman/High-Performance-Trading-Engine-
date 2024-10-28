import streamlit as st
from market_simulation import MarketSimulation
from dashboard import create_dashboard

def main():
    st.set_page_config(layout="wide", page_title="Advanced Trading Engine Simulation")

    st.sidebar.title("Simulation Controls")
    
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
    simulation = MarketSimulation(symbols)
    
    num_orders = st.sidebar.number_input("Number of Orders to Simulate", min_value=1000, max_value=1000000, value=100000, step=1000)
    
    if st.sidebar.button("Run Simulation"):
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()
        
        trades, orders_per_second = simulation.simulate_market(num_orders)
        
        progress_bar.progress(100)
        status_text.text(f"Processed {num_orders} orders")
        
        st.sidebar.success(f"Simulation complete!")
        st.sidebar.info(f"Executed {len(trades)} trades")
        st.sidebar.info(f"Processed {orders_per_second:.2f} orders per second")
        
        create_dashboard(simulation.engine, trades, symbols)

if __name__ == "__main__":
    main()