import streamlit as st
import pandas as pd
import plotly.express as px
from db_utils import list_balances, get_expenses, get_monthly_summary

def balance_overview_page():
    st.header("📊 Balance Overview")
    
    # Get monthly summary data
    monthly_data = get_monthly_summary()
    
    if monthly_data:
        df_summary = pd.DataFrame(monthly_data)
        
        # Overall statistics
        total_balance = df_summary['total_balance'].sum()
        total_spent = df_summary['total_spent'].sum()
        total_remaining = df_summary['remaining'].sum()
        avg_monthly_spending = df_summary['total_spent'].mean()
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Balance", f"₹{total_balance:,.2f}")
        with col2:
            st.metric("Total Spent", f"₹{total_spent:,.2f}")
        with col3:
            st.metric("Total Remaining", f"₹{total_remaining:,.2f}")
        with col4:
            st.metric("Avg Monthly Spending", f"₹{avg_monthly_spending:,.2f}")
        
        # Create visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Monthly balance vs spending
            fig_balance = px.bar(
                df_summary, 
                x='month', 
                y=['total_balance', 'total_spent'],
                title="Monthly Balance vs Spending",
                labels={'value': 'Amount (₹)', 'month': 'Month'},
                barmode='group'
            )
            fig_balance.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_balance, use_container_width=True)
        
        with col2:
            # Remaining balance by month
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
        
        # Detailed monthly breakdown
        st.subheader("📋 Monthly Breakdown")
        
        # Add spending percentage column
        df_summary['spending_percentage'] = (df_summary['total_spent'] / df_summary['total_balance'] * 100).round(2)
        df_summary['spending_percentage'] = df_summary['spending_percentage'].fillna(0)
        
        # Display detailed table
        st.dataframe(
            df_summary.style.format({
                'total_balance': '₹{:,.2f}',
                'total_spent': '₹{:,.2f}',
                'remaining': '₹{:,.2f}',
                'spending_percentage': '{:.1f}%'
            }),
            use_container_width=True
        )
        
        # Monthly trend analysis
        st.subheader("📈 Monthly Trends")
        
        # Convert month to datetime for better plotting
        df_trends = df_summary.copy()
        df_trends['month_date'] = pd.to_datetime(df_trends['month'] + '-01')
        
        # Create trend line chart
        fig_trends = px.line(
            df_trends, 
            x='month_date', 
            y=['total_balance', 'total_spent', 'remaining'],
            title="Monthly Financial Trends",
            labels={'value': 'Amount (₹)', 'month_date': 'Month'},
            markers=True
        )
        fig_trends.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_trends, use_container_width=True)
        
        # Spending efficiency analysis
        st.subheader("💡 Spending Analysis")
        
        # Calculate spending efficiency metrics
        efficient_months = df_summary[df_summary['spending_percentage'] <= 80]
        overspent_months = df_summary[df_summary['spending_percentage'] > 100]
        well_budgeted_months = df_summary[(df_summary['spending_percentage'] > 80) & (df_summary['spending_percentage'] <= 100)]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Efficient Months (≤80%)", len(efficient_months))
        with col2:
            st.metric("Well Budgeted (80-100%)", len(well_budgeted_months))
        with col3:
            st.metric("Overspent Months (>100%)", len(overspent_months))
        
        if len(overspent_months) > 0:
            st.warning(f"⚠️ You overspent in {len(overspent_months)} month(s): {', '.join(overspent_months['month'].tolist())}")
        
        if len(efficient_months) > 0:
            st.success(f"✅ Great job! You were efficient in {len(efficient_months)} month(s): {', '.join(efficient_months['month'].tolist())}")
    
    else:
        st.info("No balances added yet. Please add from 'Add Monthly Balance' page.")