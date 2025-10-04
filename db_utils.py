from sqlalchemy import create_engine, Column, Integer, Float, String, Date, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd
import datetime
import os
from dotenv import load_dotenv
# Update with your actual PostgreSQL credentials
load_dotenv()
DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Balance(Base):
    __tablename__ = "balances"
    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(String, index=True)
    prev_balance = Column(Float)
    this_month = Column(Float)
    total_balance = Column(Float)

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    month = Column(String, index=True)
    category = Column(String)
    tag = Column(String)
    amount = Column(Float)

Base.metadata.create_all(engine)

def add_balance(month, prev_balance, this_month):
    session = SessionLocal()
    total_balance = prev_balance + this_month
    bal = session.query(Balance).filter_by(month=month).first()
    if bal:
        bal.prev_balance = prev_balance
        bal.this_month = this_month
        bal.total_balance = total_balance
    else:
        bal = Balance(month=month, prev_balance=prev_balance, this_month=this_month, total_balance=total_balance)
        session.add(bal)
    session.commit()
    session.close()

def get_balance(month):
    session = SessionLocal()
    bal = session.query(Balance).filter_by(month=month).first()
    session.close()
    return bal

def list_balances():
    session = SessionLocal()
    bals = session.query(Balance).order_by(Balance.month.desc()).all()
    session.close()
    return bals

def add_expense(date, month, category, tag, amount):
    session = SessionLocal()
    exp = Expense(date=date, month=month, category=category, tag=tag, amount=amount)
    session.add(exp)
    session.commit()
    session.close()

def get_expenses(month):
    session = SessionLocal()
    exps = session.query(Expense).filter_by(month=month).all()
    session.close()
    return exps

def list_expense_months():
    session = SessionLocal()
    months = session.query(Expense.month).distinct().all()
    session.close()
    return sorted(set([m[0] for m in months]))

def get_all_expenses():
    """Get all expenses across all months"""
    session = SessionLocal()
    exps = session.query(Expense).order_by(Expense.date.desc()).all()
    session.close()
    return exps

def get_expenses_by_category(category=None, month=None):
    """Get expenses filtered by category and/or month"""
    session = SessionLocal()
    query = session.query(Expense)
    if category:
        query = query.filter_by(category=category)
    if month:
        query = query.filter_by(month=month)
    exps = query.order_by(Expense.date.desc()).all()
    session.close()
    return exps

def get_monthly_summary():
    """Get summary data for all months"""
    session = SessionLocal()
    # Get all months that have either balances or expenses
    balance_months = session.query(Balance.month).distinct().all()
    expense_months = session.query(Expense.month).distinct().all()
    all_months = sorted(set([m[0] for m in balance_months + expense_months]))
    
    summary_data = []
    for month in all_months:
        # Get balance for this month
        bal = session.query(Balance).filter_by(month=month).first()
        total_balance = bal.total_balance if bal else 0.0
        
        # Get expenses for this month
        expenses = session.query(Expense).filter_by(month=month).all()
        total_spent = sum([e.amount for e in expenses]) if expenses else 0.0
        remaining = total_balance - total_spent
        
        summary_data.append({
            'month': month,
            'total_balance': total_balance,
            'total_spent': total_spent,
            'remaining': remaining,
            'expense_count': len(expenses)
        })
    
    session.close()
    return summary_data

def delete_expense(expense_id):
    """Delete an expense by ID"""
    session = SessionLocal()
    try:
        expense = session.query(Expense).filter_by(id=expense_id).first()
        if expense:
            session.delete(expense)
            session.commit()
            session.close()
            return True
        else:
            session.close()
            return False
    except Exception as e:
        session.rollback()
        session.close()
        return False

def get_expense_by_id(expense_id):
    """Get a specific expense by ID"""
    session = SessionLocal()
    expense = session.query(Expense).filter_by(id=expense_id).first()
    session.close()
    return expense