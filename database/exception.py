class FinanceDashboardError(Exception):
    """Base exception for all project errors"""
    pass

class InvalidExpenseError(FinanceDashboardError):
    """Raised when expense data is invalid (negative amount, missing fields)"""
    pass

class UserNotFoundError(FinanceDashboardError):
    """Raised when a user doesn't exist in the DB"""
    pass

class CategoryNotFoundError(FinanceDashboardError):
    """Raised when a category doesn't exist in the DB"""
    pass

class BudgetExceededError(FinanceDashboardError):
    """Raised when an expense pushes spending over the budget limit"""
    pass

class DatabaseError(FinanceDashboardError):
    """Raised when any DB operation fails"""
    pass

class DuplicateEntryError(FinanceDashboardError):
    """Raised when trying to insert something that already exists"""
    pass