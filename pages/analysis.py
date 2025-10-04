import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from db_utils import list_expense_months, get_expenses, get_all_expenses, get_monthly_summary

def analysis_page():
    st.header("📈 Expense Analysis")
    
    # Create tabs for different analysis views
    tab1, tab2, tab3 = st.tabs(["📅 Single Month Analysis", "📊 Multi-Month Comparison", "🔍 Category Deep Dive"])
    
    with tab1:
        st.subheader("📅 Single Month Analysis")
        months = list_expense_months()
        if months:
            selected_month = st.selectbox("Select Month for Analysis", months, key="single_month_analysis")
            expenses = get_expenses(selected_month)
            if expenses:
                df_month = pd.DataFrame([{
                    "Date": e.date,
                    "Category": e.category,
                    "Amount": e.amount
                } for e in expenses])
                
                # Monthly summary metrics
                total_spent = df_month['Amount'].sum()
                expense_count = len(df_month)
                avg_expense = df_month['Amount'].mean()
                max_expense = df_month['Amount'].max()
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Spent", f"₹{total_spent:,.2f}")
                with col2:
                    st.metric("Number of Expenses", expense_count)
                with col3:
                    st.metric("Average Expense", f"₹{avg_expense:,.2f}")
                with col4:
                    st.metric("Highest Expense", f"₹{max_expense:,.2f}")
                
                # Visualizations
                col1, col2 = st.columns(2)
                
                with col1:
                    # Pie chart for category distribution
                    pie_chart = px.pie(
                        df_month, 
                        names="Category", 
                        values="Amount", 
                        title=f"Expense Distribution for {selected_month}"
                    )
                    st.plotly_chart(pie_chart, use_container_width=True)
                
                with col2:
                    # Bar chart for daily spending
                    daily_spending = df_month.groupby("Date")["Amount"].sum().reset_index()
                    bar_chart = px.bar(
                        daily_spending, 
                        x="Date", 
                        y="Amount", 
                        title=f"Daily Expenses in {selected_month}"
                    )
                    bar_chart.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(bar_chart, use_container_width=True)
                
                # Category summary table
                st.subheader("📋 Category Summary")
                summary = df_month.groupby("Category")["Amount"].sum().reset_index().sort_values("Amount", ascending=False)
                summary['Percentage'] = (summary['Amount'] / summary['Amount'].sum() * 100).round(2)
                st.dataframe(
                    summary.style.format({
                        'Amount': '₹{:,.2f}',
                        'Percentage': '{:.1f}%'
                    }),
                    use_container_width=True
                )
            else:
                st.info("No expenses recorded for this month.")
        else:
            st.info("No expenses added yet. Go to 'Add Expenses' page first.")
    
    with tab2:
        st.subheader("📊 Multi-Month Comparison")
        months = list_expense_months()
        if len(months) >= 2:
            selected_months = st.multiselect(
                "Select Months to Compare", 
                months, 
                default=months[:3] if len(months) >= 3 else months,
                key="multi_month_comparison"
            )
            
            if selected_months:
                # Get data for selected months
                comparison_data = []
                for month in selected_months:
                    expenses = get_expenses(month)
                    if expenses:
                        df_month = pd.DataFrame([{
                            "Date": e.date,
                            "Category": e.category,
                            "Amount": e.amount
                        } for e in expenses])
                        
                        # Calculate monthly metrics
                        total_spent = df_month['Amount'].sum()
                        expense_count = len(df_month)
                        avg_expense = df_month['Amount'].mean()
                        
                        comparison_data.append({
                            'Month': month,
                            'Total Spent': total_spent,
                            'Expense Count': expense_count,
                            'Average Expense': avg_expense
                        })
                
                if comparison_data:
                    df_comparison = pd.DataFrame(comparison_data)
                    
                    # Monthly spending comparison
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig_spending = px.bar(
                            df_comparison, 
                            x='Month', 
                            y='Total Spent',
                            title="Monthly Spending Comparison",
                            labels={'Total Spent': 'Amount Spent (₹)', 'Month': 'Month'}
                        )
                        fig_spending.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig_spending, use_container_width=True)
                    
                    with col2:
                        fig_count = px.bar(
                            df_comparison, 
                            x='Month', 
                            y='Expense Count',
                            title="Number of Expenses by Month",
                            labels={'Expense Count': 'Number of Expenses', 'Month': 'Month'}
                        )
                        fig_count.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig_count, use_container_width=True)
                    
                    # Comparison table
                    st.subheader("📋 Monthly Comparison Table")
                    st.dataframe(
                        df_comparison.style.format({
                            'Total Spent': '₹{:,.2f}',
                            'Average Expense': '₹{:,.2f}'
                        }),
                        use_container_width=True
                    )
                    
                    # Category comparison across months
                    st.subheader("🔍 Category Comparison Across Months")
                    category_comparison = []
                    for month in selected_months:
                        expenses = get_expenses(month)
                        if expenses:
                            df_month = pd.DataFrame([{
                                "Category": e.category,
                                "Amount": e.amount
                            } for e in expenses])
                            category_summary = df_month.groupby('Category')['Amount'].sum().reset_index()
                            category_summary['Month'] = month
                            category_comparison.append(category_summary)
                    
                    if category_comparison:
                        df_cat_comparison = pd.concat(category_comparison, ignore_index=True)
                        
                        # Pivot for better visualization
                        pivot_data = df_cat_comparison.pivot(index='Category', columns='Month', values='Amount').fillna(0)
                        
                        # Show top categories
                        top_categories = df_cat_comparison.groupby('Category')['Amount'].sum().nlargest(10).index
                        pivot_top = pivot_data.loc[top_categories]
                        
                        fig_heatmap = px.imshow(
                            pivot_top.values,
                            labels=dict(x="Month", y="Category", color="Amount"),
                            x=pivot_top.columns,
                            y=pivot_top.index,
                            aspect="auto",
                            title="Top 10 Categories - Monthly Comparison"
                        )
                        st.plotly_chart(fig_heatmap, use_container_width=True)
            else:
                st.info("Please select at least one month for comparison.")
        else:
            st.info("Need at least 2 months of data for comparison. Add more expenses to see multi-month analysis.")
    
    with tab3:
        st.subheader("🔍 Category Deep Dive")
        all_expenses = get_all_expenses()
        if all_expenses:
            df_all = pd.DataFrame([{
                "Date": e.date,
                "Month": e.month,
                "Category": e.category,
                "Amount": e.amount
            } for e in all_expenses])
            
            # Category selection
            categories = sorted(df_all['Category'].unique())
            selected_categories = st.multiselect(
                "Select Categories to Analyze", 
                categories, 
                default=categories[:5] if len(categories) >= 5 else categories,
                key="category_deep_dive"
            )
            
            if selected_categories:
                # Filter data for selected categories
                df_filtered = df_all[df_all['Category'].isin(selected_categories)]
                
                # Category spending over time
                monthly_cat = df_filtered.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
                
                fig_trends = px.line(
                    monthly_cat, 
                    x='Month', 
                    y='Amount', 
                    color='Category',
                    title="Category Spending Trends Over Time",
                    labels={'Amount': 'Amount Spent (₹)', 'Month': 'Month'}
                )
                fig_trends.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_trends, use_container_width=True)
                
                # Category statistics
                st.subheader("📊 Category Statistics")
                cat_stats = df_filtered.groupby('Category')['Amount'].agg(['sum', 'count', 'mean', 'std']).reset_index()
                cat_stats.columns = ['Category', 'Total Spent', 'Count', 'Average', 'Std Dev']
                cat_stats = cat_stats.sort_values('Total Spent', ascending=False)
                
                st.dataframe(
                    cat_stats.style.format({
                        'Total Spent': '₹{:,.2f}',
                        'Average': '₹{:,.2f}',
                        'Std Dev': '₹{:,.2f}'
                    }),
                    use_container_width=True
                )
                
                # Monthly category breakdown
                st.subheader("📅 Monthly Category Breakdown")
                monthly_breakdown = df_filtered.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
                monthly_breakdown_pivot = monthly_breakdown.pivot(index='Month', columns='Category', values='Amount').fillna(0)
                
                fig_breakdown = px.bar(
                    monthly_breakdown_pivot,
                    title="Monthly Spending by Selected Categories",
                    labels={'value': 'Amount Spent (₹)', 'index': 'Month'}
                )
                fig_breakdown.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_breakdown, use_container_width=True)
            else:
                st.info("Please select at least one category for analysis.")
        else:
            st.info("No expenses available for category analysis.")