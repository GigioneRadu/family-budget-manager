"""Config package initialization"""

from .database import get_connection, init_database
from .categories import BUDGET_CATEGORIES, CATEGORY_COLORS, CATEGORY_ICONS, get_income_categories

__all__ = [
    'get_connection',
    'init_database',
    'BUDGET_CATEGORIES',
    'CATEGORY_COLORS',
    'CATEGORY_ICONS',
    'get_income_categories'
]

