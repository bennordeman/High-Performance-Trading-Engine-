from enum import Enum
from dataclasses import dataclass

class OrderType(Enum):
    MARKET = 1
    LIMIT = 2
    STOP = 3

class TimeInForce(Enum):
    GTC = 1  # Good Till Cancelled
    IOC = 2  # Immediate Or Cancel
    FOK = 3  # Fill Or Kill

@dataclass
class Order:
    order_id: int
    symbol: str
    price: float
    quantity: int
    is_buy: bool
    order_type: OrderType
    time_in_force: TimeInForce
    stop_price: float = None

    def __lt__(self, other):
        if self.is_buy:
            return self.price > other.price
        return self.price < other.price