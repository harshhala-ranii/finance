import streamlit as st
import datetime

categories = [
    "harshala", "rani", "yoga", "Outside food", "groceries", "fruits", "vegetables",
    "hair color", "TV Recharge", "ACT", "Electricity bill", "Gas", "Parlour", "flower",
    "dairy", "Spotify", "Petrol", "Self care", "makeup", "Clothes", "footwear", 
    "Dance", "Gym", "snacks", "medicines", "Repair", "Outing"
]

page = st.sidebar.radio(
    "📌 Navigate", 
    ["💵 Add Monthly Balance", "📊 Balance Overview", "📝 Add Expenses", "📈 Analysis"]
)

from pages.add_balance import add_balance_page
from pages.balance_overview import balance_overview_page
from pages.add_expenses import add_expenses_page
from pages.analysis import analysis_page

if page == "💵 Add Monthly Balance":
    add_balance_page(categories)
elif page == "📊 Balance Overview":
    balance_overview_page()
elif page == "📝 Add Expenses":
    add_expenses_page(categories)
elif page == "📈 Analysis":
    analysis_page()