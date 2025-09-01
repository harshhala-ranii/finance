import streamlit as st
from db_utils import list_balances, get_expenses

def balance_overview_page():
    st.header("📊 Balance Overview")
    balances = list_balances()
    if balances:
        for bal in balances:
            exp_df = get_expenses(bal.month)
            spent = sum([e.amount for e in exp_df]) if exp_df else 0.0
            remaining = bal.total_balance - spent
            st.subheader(f"Month: {bal.month}")
            st.write(f"➡️ Starting Balance: ₹{bal.total_balance:,.2f}")
            st.write(f"➡️ Total Spent: ₹{spent:,.2f}")
            st.write(f"✅ Remaining Balance: ₹{remaining:,.2f}")
    else:
        st.info("No balances added yet. Please add from 'Add Monthly Balance' page.")