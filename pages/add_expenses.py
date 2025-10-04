import streamlit as st
import datetime
from db_utils import add_expense, get_expenses, list_expense_months

def add_expenses_page(categories):
    st.header("📝 Add Expense")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("➕ Add New Expense")
        exp_date = st.date_input("Expense Date", datetime.date.today())
        month_key = exp_date.strftime("%Y-%m")
        category = st.selectbox("Select Category", categories)
        tag = st.text_input("Optional Tag / Note")
        amount = st.number_input("Expense Amount", min_value=0.0, step=50.0)
        if st.button("Add Expense", type="primary"):
            add_expense(exp_date, month_key, category, tag, amount)
            st.success(f"Expense of ₹{amount:,.2f} added under {category} for {month_key}")
            st.rerun()
    
    with col2:
        st.subheader("📅 View Expenses by Month")
        months = list_expense_months()
        if months:
            selected_month = st.selectbox("Select Month to View", months, key="expense_month_selector")
            expenses = get_expenses(selected_month)
            if expenses:
                import pandas as pd
                df = pd.DataFrame([{
                    "Date": e.date,
                    "Category": e.category,
                    "Tag": e.tag if e.tag else "",
                    "Amount": e.amount
                } for e in expenses])
                
                # Show summary
                total_spent = df['Amount'].sum()
                expense_count = len(df)
                st.metric("Total Spent", f"₹{total_spent:,.2f}")
                st.metric("Number of Expenses", expense_count)
                
                # Show expenses table
                st.dataframe(
                    df.sort_values("Date", ascending=False).style.format({'Amount': '₹{:,.2f}'}),
                    use_container_width=True
                )
            else:
                st.info(f"No expenses found for {selected_month}")
        else:
            st.info("No expenses added yet. Add your first expense above!")
    
    # Show current month expenses below
    st.subheader(f"📋 Current Month ({month_key}) Expenses")
    current_expenses = get_expenses(month_key)
    if current_expenses:
        import pandas as pd
        df_current = pd.DataFrame([{
            "Date": e.date,
            "Category": e.category,
            "Tag": e.tag if e.tag else "",
            "Amount": e.amount
        } for e in current_expenses])
        
        # Show summary for current month
        total_current = df_current['Amount'].sum()
        count_current = len(df_current)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("This Month Total", f"₹{total_current:,.2f}")
        with col2:
            st.metric("This Month Count", count_current)
        
        st.dataframe(
            df_current.sort_values("Date", ascending=False).style.format({'Amount': '₹{:,.2f}'}),
            use_container_width=True
        )
    else:
        st.info("No expenses added yet for this month.")