import streamlit as st
import datetime
from db_utils import add_expense, get_expenses

def add_expenses_page(categories):
    st.header("📝 Add Expense")
    exp_date = st.date_input("Expense Date", datetime.date.today())
    month_key = exp_date.strftime("%Y-%m")
    category = st.selectbox("Select Category", categories)
    tag = st.text_input("Optional Tag / Note")
    amount = st.number_input("Expense Amount", min_value=0.0, step=50.0)
    if st.button("Add Expense"):
        add_expense(exp_date, month_key, category, tag, amount)
        st.success(f"Expense of ₹{amount:,.2f} added under {category} for {month_key}")
    st.subheader(f"📋 Expense Log for {month_key}")
    expenses = get_expenses(month_key)
    if expenses:
        import pandas as pd
        df = pd.DataFrame([{
            "Date": e.date,
            "Category": e.category,
            "Tag": e.tag,
            "Amount": e.amount
        } for e in expenses])
        st.dataframe(df.sort_values("Date", ascending=False))
    else:
        st.info("No expenses added yet for this month.")