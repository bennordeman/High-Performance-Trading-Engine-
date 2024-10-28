import heapq
from collections import defaultdict
from order import Order, OrderType

class OrderMatchingEngine:
    def __init__(self):
        self.order_books = defaultdict(lambda: {'buy': [], 'sell': []})

    def add_order(self, order):
        if order.order_type == OrderType.MARKET:
            self._process_market_order(order)
        elif order.order_type == OrderType.LIMIT:
            heapq.heappush(self.order_books[order.symbol]['buy' if order.is_buy else 'sell'], order)

    def _process_market_order(self, order):
        opposite_side = 'sell' if order.is_buy else 'buy'
        order_book = self.order_books[order.symbol][opposite_side]
        
        while order.quantity > 0 and order_book:
            matching_order = heapq.heappop(order_book)
            matched_quantity = min(order.quantity, matching_order.quantity)
            order.quantity -= matched_quantity
            matching_order.quantity -= matched_quantity
            
            if matching_order.quantity > 0:
                heapq.heappush(order_book, matching_order)

    def match_orders(self, symbol):
        buy_orders = self.order_books[symbol]['buy']
        sell_orders = self.order_books[symbol]['sell']
        trades = []

        while buy_orders and sell_orders:
            if buy_orders[0].order_type == OrderType.MARKET or sell_orders[0].order_type == OrderType.MARKET or buy_orders[0].price >= sell_orders[0].price:
                buy_order = heapq.heappop(buy_orders)
                sell_order = heapq.heappop(sell_orders)
                trade_quantity = min(buy_order.quantity, sell_order.quantity)
                trade_price = sell_order.price if sell_order.order_type == OrderType.LIMIT else buy_order.price
                trades.append((buy_order.order_id, sell_order.order_id, trade_quantity, trade_price))
                
                buy_order.quantity -= trade_quantity
                sell_order.quantity -= trade_quantity
                
                if buy_order.quantity > 0:
                    heapq.heappush(buy_orders, buy_order)
                if sell_order.quantity > 0:
                    heapq.heappush(sell_orders, sell_order)
            else:
                break

        return trades