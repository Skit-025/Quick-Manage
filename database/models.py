from dataclasses import dataclass ,field
from datetime import datetime, date
from typing import Optional

@dataclass
class User:
    name: str
    email: str
    password: str
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Category:
    name: str
    budget_limit: float = 0.0
    id: Optional[int] = None

@dataclass
class Expense:
    user_id: int
    category_id: int
    amount: float
    date_: date
    description_: Optional[str] = None
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Budget:
    user_id: int
    category_id: int
    amount: float
    month_: str
    id: Optional[int] = None