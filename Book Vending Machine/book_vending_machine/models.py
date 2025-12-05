from dataclasses import dataclass

@dataclass
class Book():
    title: str
    description: str
    category: str
    rating: int
    price: float
    in_stock: bool