import streamlit as st
import plotly.express as px
from db_utils import list_expense_months, get_expenses

def analysis_page():
    st.header("📈 Expense Analysis")
    months = list_expense_months()
    if months:
        selected_month = st.selectbox("Select Month for Analysis", months)
        expenses = get_expenses(selected_month)
        if expenses:
            import pandas as pd
            df_month = pd.DataFrame([{
                "Date": e.date,
                "Category": e.category,
                "Amount": e.amount
            } for e in expenses])
            st.subheader("🍕 Expense Distribution by Category")
            pie_chart = px.pie(df_month, names="Category", values="Amount", title=f"Expenses for {selected_month}")
            st.plotly_chart(pie_chart)
            st.subheader("📅 Daily Spending")
            daily_spending = df_month.groupby("Date")["Amount"].sum().reset_index()
            bar_chart = px.bar(daily_spending, x="Date", y="Amount", title=f"Daily Expenses in {selected_month}")
            st.plotly_chart(bar_chart)
            st.subheader("📋 Expense Summary")
            summary = df_month.groupby("Category")["Amount"].sum().reset_index().sort_values("Amount", ascending=False)
            st.dataframe(summary)
        else:
            st.info("No expenses recorded for this month.")
    else:
        st.info("No expenses added yet. Go to 'Add Expenses' page first.")