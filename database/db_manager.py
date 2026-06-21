import os
import sys
import logging
import sqlite3 as sq
from datetime import date
from typing import Optional

# Append root path to the system so python interpreter can access everything
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DB_PATH,APP_NAME
from models import User,Category,Expense,Budget
from database.exception import(
    InvalidExpenseError,UserNotFoundError,CategoryNotFoundError,BudgetExceededError,
    DatabaseError,DuplicateEntryError
)
logger=logging.getLogger(APP_NAME)

class DatabaseManager:
    def __init__(self):
        self.db_path=DB_PATH
        self._init_db()

    def _getConnection(self):
        conn=sq.connect(self.db_path)
        conn.row_factory=sq.Row # Now the tuple is a dictionary and can be accessed like kv pair
        return conn
    
    def _init_db(self):
        try:
            schema_path=os.path.join(os.path.dirname(__file__),'schema.sql')
            with open(schema_path,'r')as f:
                schema=f.read()
            with self._getConnection() as conn:
                conn.executescript(schema)
            logger.info('Database initialized successfully')
        except Exception as e:
            logger.error(f"Database initialization failed:{e}")
            raise DatabaseError(f"Database initialization failed:{e}")

    def add_user(self,user:User)->int:
        try:
            with self._getConnection() as conn:
                cursor=conn.execute(
                "INSERT INTO USERS(NAME,EMAIL,PASSWORD) VALUES(?,?,?)",
                (user.name,user.email,user.password)
                )
                logger.info(f"User added:{user.email}")
                return cursor.lastrowid
        except sq.IntegrityError:
            raise DuplicateEntryError(f'Email already exist:{user.email}')
        except Exception as e:
            raise DatabaseError(f"add_user failed: {e}")

    def get_user(self,user_id:int)->User:
        try:
            with self._getConnection() as conn:
                row=conn.execute(
                    'SELECT * FROM USERS WHERE ID=?',(user_id,)
                ).fetchone()
            if not row:
                raise UserNotFoundError(f"No user with id {user_id}")
            return User(id=row['ID'],name=row['NAME'],email=row['EMAIL'],password=row['PASSWORD'])
        except UserNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"get_user failed: {e}")

    # Category Methods

    def add_category(self,category:Category)->int:
        try:
            with self._getConnection() as conn:
                cursor=conn.execute(
                    'INSERT INTO CATEGORIES(NAME,BUDGET_LIMIT) VALUES (?,?)',
                    (category.name,category.budget_limit)
                )
                logger.info(f"Category added:{category.name}")
                return cursor.lastrowid
        except sq.IntegrityError:
            raise DuplicateEntryError(f"Category already exists:{category.name}")
        except Exception as e:
            raise DatabaseError(f"add_category failed: {e}")

    def get_all_categories(self) -> list:
        try:
            with self._getConnection() as conn:
                rows = conn.execute("SELECT * FROM CATEGORIES").fetchall()
            return [Category(id=r["ID"], name=r["NAME"], budget_limit=r["BUDGET_LIMIT"]) for r in rows]
        except Exception as e:
            raise DatabaseError(f"get_all_categories failed: {e}")


     # ── EXPENSE METHODS ───────────────────────────────────────

    def add_expense(self, expense: Expense) -> int:
        if expense.amount <= 0:
            raise InvalidExpenseError("Amount must be greater than 0")
        try:
            with self._getConnection() as conn:
                cursor = conn.execute(
                    "INSERT INTO EXPENSES (USER_ID, CATEGORY_ID, AMOUNT, DESCRIPTION_, DATE_) VALUES (?, ?, ?, ?, ?)",
                    (expense.user_id, expense.category_id, expense.amount, expense.description_, expense.date_)
                )
                logger.info(f"Expense added: ₹{expense.amount} on {expense.date_}")
                return cursor.lastrowid
        except InvalidExpenseError:
            raise
        except Exception as e:
            raise DatabaseError(f"add_expense failed: {e}")

    def get_expenses(self, user_id: int) -> list:
        try:
            with self._getConnection() as conn:
                rows = conn.execute(
                    "SELECT * FROM EXPENSES WHERE USER_ID = ? ORDER BY DATE_ DESC", (user_id,)
                ).fetchall()
            return [
                Expense(
                    id=r["ID"], user_id=r["USER_ID"], category_id=r["CATEGORY_ID"],
                    amount=r["AMOUNT"], description_=r["DESCRIPTION_"], date_=r["DATE_"]
                ) for r in rows
            ]
        except Exception as e:
            raise DatabaseError(f"get_expenses failed: {e}")

    def delete_expense(self, expense_id: int) -> bool:
        try:
            with self._getConnection() as conn:
                conn.execute("DELETE FROM EXPENSES WHERE ID = ?", (expense_id,))
            logger.info(f"Expense deleted: id {expense_id}")
            return True
        except Exception as e:
            raise DatabaseError(f"delete_expense failed: {e}")

    # ── BUDGET METHODS ────────────────────────────────────────

    def add_budget(self, budget: Budget) -> int:
        try:
            with self._getConnection() as conn:
                cursor = conn.execute(
                    "INSERT INTO BUDGETS (USER_ID, CATEGORY_ID, AMOUNT, MONTH_) VALUES (?, ?, ?, ?)",
                    (budget.user_id, budget.category_id, budget.amount, budget.month_)
                )
                logger.info(f"Budget added: ₹{budget.amount} for {budget.month_}")
                return cursor.lastrowid
        except Exception as e:
            raise DatabaseError(f"add_budget failed: {e}")

    def get_budgets(self, user_id: int) -> list:
        try:
            with self._getConnection() as conn:
                rows = conn.execute(
                    "SELECT * FROM BUDGETS WHERE USER_ID = ?", (user_id,)
                ).fetchall()
            return [
                Budget(id=r["ID"], user_id=r["USER_ID"], category_id=r["CATEGORY_ID"],
                       amount=r["AMOUNT"], month_=r["MONTH_"]) for r in rows
            ]
        except Exception as e:
            raise DatabaseError(f"get_budgets failed: {e}")