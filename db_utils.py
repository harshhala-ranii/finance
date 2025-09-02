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