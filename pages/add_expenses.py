import streamlit as st
import datetime
from db_utils import add_expense, get_expenses, list_expense_months, delete_expense, get_expense_by_id

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
                
                # Show expenses table with delete functionality
                st.dataframe(
                    df.sort_values("Date", ascending=False).style.format({'Amount': '₹{:,.2f}'}),
                    use_container_width=True
                )
                
                # Delete expense section
                st.subheader("🗑️ Delete Expense")
                if len(df) > 0:
                    # Create a selectbox for expense selection
                    expense_options = []
                    for _, row in df.iterrows():
                        expense_options.append(f"{row['Date']} - {row['Category']} - ₹{row['Amount']:,.2f}")
                    
                    selected_expense = st.selectbox(
                        "Select expense to delete:", 
                        expense_options,
                        key=f"delete_expense_{selected_month}"
                    )
                    
                    if selected_expense and st.button("Delete Selected Expense", type="secondary"):
                        # Find the expense ID
                        selected_index = expense_options.index(selected_expense)
                        expense_row = df.iloc[selected_index]
                        
                        # Get the actual expense from database to get ID
                        expenses = get_expenses(selected_month)
                        expense_to_delete = None
                        for exp in expenses:
                            if (str(exp.date) == str(expense_row['Date']) and 
                                exp.category == expense_row['Category'] and 
                                exp.amount == expense_row['Amount']):
                                expense_to_delete = exp
                                break
                        
                        if expense_to_delete:
                            if delete_expense(expense_to_delete.id):
                                st.success(f"✅ Expense deleted: {expense_row['Category']} - ₹{expense_row['Amount']:,.2f}")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete expense. Please try again.")
                        else:
                            st.error("❌ Could not find expense to delete.")
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
        
        # Delete expense section for current month
        st.subheader("🗑️ Delete Current Month Expense")
        if len(df_current) > 0:
            # Create a selectbox for expense selection
            current_expense_options = []
            for _, row in df_current.iterrows():
                current_expense_options.append(f"{row['Date']} - {row['Category']} - ₹{row['Amount']:,.2f}")
            
            selected_current_expense = st.selectbox(
                "Select expense to delete:", 
                current_expense_options,
                key=f"delete_current_expense_{month_key}"
            )
            
            if selected_current_expense and st.button("Delete Selected Expense", type="secondary", key="delete_current_btn"):
                # Find the expense ID
                selected_index = current_expense_options.index(selected_current_expense)
                expense_row = df_current.iloc[selected_index]
                
                # Get the actual expense from database to get ID
                expenses = get_expenses(month_key)
                expense_to_delete = None
                for exp in expenses:
                    if (str(exp.date) == str(expense_row['Date']) and 
                        exp.category == expense_row['Category'] and 
                        exp.amount == expense_row['Amount']):
                        expense_to_delete = exp
                        break
                
                if expense_to_delete:
                    if delete_expense(expense_to_delete.id):
                        st.success(f"✅ Expense deleted: {expense_row['Category']} - ₹{expense_row['Amount']:,.2f}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete expense. Please try again.")
                else:
                    st.error("❌ Could not find expense to delete.")
    else:
        st.info("No expenses added yet for this month.")