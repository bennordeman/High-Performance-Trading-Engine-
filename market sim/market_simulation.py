import random
import time
from order import Order, OrderType, TimeInForce
from order_matching_engine import OrderMatchingEngine

class MarketSimulation:
    def __init__(self, symbols):
        self.engine = OrderMatchingEngine()
        self.symbols = symbols
        self.last_prices = {symbol: 100.0 for symbol in symbols}

    def generate_orders(self, num_orders):
        orders = []
        for i in range(num_orders):
            symbol = random.choice(self.symbols)
            is_buy = random.choice([True, False])
            
            # Increase likelihood of market orders
            order_type = random.choices([OrderType.MARKET, OrderType.LIMIT], weights=[0.4, 0.6])[0]
            time_in_force = random.choice(list(TimeInForce))
            
            if order_type == OrderType.MARKET:
                price = None
            else:
                # Narrow the price range for more matches
                price = round(self.last_prices[symbol] * random.uniform(0.98, 1.02), 2)
            
            order = Order(
                order_id=i,
                symbol=symbol,
                price=price,
                quantity=random.randint(1, 100),
                is_buy=is_buy,
                order_type=order_type,
                time_in_force=time_in_force
            )
            orders.append(order)
        return orders

    def simulate_market(self, num_orders):
        orders = self.generate_orders(num_orders)
        trades = []
        
        start_time = time.time()
        
        for i, order in enumerate(orders):
            self.engine.add_order(order)
            
            # Match orders more frequently
            if i % 100 == 0:
                for symbol in self.symbols:
                    new_trades = self.engine.match_orders(symbol)
                    trades.extend(new_trades)
                    if new_trades:
                        self.last_prices[symbol] = new_trades[-1][3]  # Update last price
        
        # Final matching round
        for symbol in self.symbols:
            trades.extend(self.engine.match_orders(symbol))
        
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        orders_per_second = num_orders / elapsed_time
        
        return trades, orders_per_second