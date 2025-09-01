import streamlit as st
import datetime
from db_utils import add_balance, get_balance

def add_balance_page(categories):
    st.header("💵 Add Monthly Balance")
    selected_date = st.date_input("Select Month", datetime.date.today())
    month_key = selected_date.strftime("%Y-%m")
    prev_balance = st.number_input("Carry Forward from Previous Month", min_value=0.0, step=100.0)
    this_month = st.number_input("Income / Added Amount for this Month", min_value=0.0, step=100.0)
    if st.button("Save Balance"):
        add_balance(month_key, prev_balance, this_month)
        st.success(f"Balance for {month_key} saved.")
    st.subheader("Current Balance for Selected Month")
    bal = get_balance(month_key)
    if bal:
        st.write(f"Month: {bal.month}")
        st.write(f"Prev Balance: ₹{bal.prev_balance:,.2f}")
        st.write(f"This Month: ₹{bal.this_month:,.2f}")
        st.write(f"Total Balance: ₹{bal.total_balance:,.2f}")
    else:
        st.info("No balance set for this month.")