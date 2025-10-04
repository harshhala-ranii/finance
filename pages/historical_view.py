import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_utils import get_all_expenses, get_monthly_summary, get_expenses_by_category, list_expense_months

def historical_view_page():
    st.header("📚 Historical Data & Analytics")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Monthly Summary", "💰 All Expenses", "🔍 Category Analysis", "📈 Trends"])
    
    with tab1:
        st.subheader("📊 Monthly Summary Overview")
        monthly_data = get_monthly_summary()
        
        if monthly_data:
            df_summary = pd.DataFrame(monthly_data)
            
            # Display summary table
            st.dataframe(
                df_summary.style.format({
                    'total_balance': '₹{:,.2f}',
                    'total_spent': '₹{:,.2f}',
                    'remaining': '₹{:,.2f}'
                }),
                use_container_width=True
            )
            
            # Create visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Monthly spending bar chart
                fig_spending = px.bar(
                    df_summary, 
                    x='month', 
                    y='total_spent',
                    title="Monthly Spending",
                    labels={'total_spent': 'Amount Spent (₹)', 'month': 'Month'}
                )
                fig_spending.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_spending, use_container_width=True)
            
            with col2:
                # Remaining balance bar chart
                fig_remaining = px.bar(
                    df_summary, 
                    x='month', 
                    y='remaining',
                    title="Remaining Balance by Month",
                    labels={'remaining': 'Remaining Balance (₹)', 'month': 'Month'},
                    color='remaining',
                    color_continuous_scale=['red', 'yellow', 'green']
                )
                fig_remaining.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_remaining, use_container_width=True)
            
            # Total statistics
            total_balance = df_summary['total_balance'].sum()
            total_spent = df_summary['total_spent'].sum()
            total_remaining = df_summary['remaining'].sum()
            avg_monthly_spending = df_summary['total_spent'].mean()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Balance", f"₹{total_balance:,.2f}")
            with col2:
                st.metric("Total Spent", f"₹{total_spent:,.2f}")
            with col3:
                st.metric("Total Remaining", f"₹{total_remaining:,.2f}")
            with col4:
                st.metric("Avg Monthly Spending", f"₹{avg_monthly_spending:,.2f}")
        else:
            st.info("No data available. Add some balances and expenses to see historical data.")
    
    with tab2:
        st.subheader("💰 All Expenses History")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            months = list_expense_months()
            selected_month = st.selectbox("Filter by Month", ["All"] + months)
        with col2:
            all_expenses = get_all_expenses()
            categories = sorted(list(set([e.category for e in all_expenses])))
            selected_category = st.selectbox("Filter by Category", ["All"] + categories)
        
        # Get filtered expenses
        if selected_month == "All" and selected_category == "All":
            expenses = all_expenses
        elif selected_month == "All":
            expenses = get_expenses_by_category(category=selected_category)
        elif selected_category == "All":
            expenses = get_expenses_by_category(month=selected_month)
        else:
            expenses = get_expenses_by_category(category=selected_category, month=selected_month)
        
        if expenses:
            # Create dataframe
            df_expenses = pd.DataFrame([{
                "Date": e.date,
                "Month": e.month,
                "Category": e.category,
                "Tag": e.tag if e.tag else "",
                "Amount": e.amount
            } for e in expenses])
            
            # Display expenses
            st.dataframe(
                df_expenses.style.format({'Amount': '₹{:,.2f}'}),
                use_container_width=True
            )
            
            # Summary statistics
            total_amount = df_expenses['Amount'].sum()
            expense_count = len(df_expenses)
            avg_expense = df_expenses['Amount'].mean()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Amount", f"₹{total_amount:,.2f}")
            with col2:
                st.metric("Number of Expenses", expense_count)
            with col3:
                st.metric("Average Expense", f"₹{avg_expense:,.2f}")
        else:
            st.info("No expenses found with the selected filters.")
    
    with tab3:
        st.subheader("🔍 Category Analysis")
        
        all_expenses = get_all_expenses()
        if all_expenses:
            # Create category summary
            df_cat = pd.DataFrame([{
                "Category": e.category,
                "Amount": e.amount,
                "Month": e.month
            } for e in all_expenses])
            
            # Overall category spending
            category_summary = df_cat.groupby('Category')['Amount'].agg(['sum', 'count', 'mean']).reset_index()
            category_summary.columns = ['Category', 'Total Spent', 'Count', 'Average']
            category_summary = category_summary.sort_values('Total Spent', ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart of category spending
                fig_pie = px.pie(
                    category_summary, 
                    values='Total Spent', 
                    names='Category',
                    title="Total Spending by Category"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Bar chart of category spending
                fig_bar = px.bar(
                    category_summary.head(10), 
                    x='Category', 
                    y='Total Spent',
                    title="Top 10 Categories by Spending"
                )
                fig_bar.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Category summary table
            st.subheader("Category Summary")
            st.dataframe(
                category_summary.style.format({
                    'Total Spent': '₹{:,.2f}',
                    'Average': '₹{:,.2f}'
                }),
                use_container_width=True
            )
            
            # Monthly category breakdown
            st.subheader("Monthly Category Breakdown")
            monthly_cat = df_cat.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
            monthly_cat_pivot = monthly_cat.pivot(index='Category', columns='Month', values='Amount').fillna(0)
            
            if not monthly_cat_pivot.empty:
                fig_heatmap = px.imshow(
                    monthly_cat_pivot.values,
                    labels=dict(x="Month", y="Category", color="Amount"),
                    x=monthly_cat_pivot.columns,
                    y=monthly_cat_pivot.index,
                    aspect="auto",
                    title="Monthly Spending by Category (Heatmap)"
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.info("No expenses available for category analysis.")
    
    with tab4:
        st.subheader("📈 Spending Trends")
        
        all_expenses = get_all_expenses()
        if all_expenses:
            df_trends = pd.DataFrame([{
                "Date": e.date,
                "Month": e.month,
                "Amount": e.amount,
                "Category": e.category
            } for e in all_expenses])
            
            # Daily spending trend
            daily_spending = df_trends.groupby('Date')['Amount'].sum().reset_index()
            daily_spending['Date'] = pd.to_datetime(daily_spending['Date'])
            
            fig_daily = px.line(
                daily_spending, 
                x='Date', 
                y='Amount',
                title="Daily Spending Trend",
                labels={'Amount': 'Amount Spent (₹)', 'Date': 'Date'}
            )
            st.plotly_chart(fig_daily, use_container_width=True)
            
            # Monthly spending trend
            monthly_spending = df_trends.groupby('Month')['Amount'].sum().reset_index()
            monthly_spending['Month'] = pd.to_datetime(monthly_spending['Month'] + '-01')
            
            fig_monthly = px.line(
                monthly_spending, 
                x='Month', 
                y='Amount',
                title="Monthly Spending Trend",
                labels={'Amount': 'Amount Spent (₹)', 'Month': 'Month'}
            )
            st.plotly_chart(fig_monthly, use_container_width=True)
            
            # Spending by day of week
            df_trends['Date'] = pd.to_datetime(df_trends['Date'])
            df_trends['DayOfWeek'] = df_trends['Date'].dt.day_name()
            df_trends['DayOfWeek'] = pd.Categorical(df_trends['DayOfWeek'], 
                                                  categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                                                  ordered=True)
            
            dow_spending = df_trends.groupby('DayOfWeek')['Amount'].sum().reset_index()
            
            fig_dow = px.bar(
                dow_spending, 
                x='DayOfWeek', 
                y='Amount',
                title="Spending by Day of Week",
                labels={'Amount': 'Amount Spent (₹)', 'DayOfWeek': 'Day of Week'}
            )
            st.plotly_chart(fig_dow, use_container_width=True)
        else:
            st.info("No expenses available for trend analysis.")
