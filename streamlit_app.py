import streamlit as st
import pandas as pd

# Function to load data
@st.cache_data
def load_data(filepath):
    data = pd.read_csv(filepath, parse_dates=['Date'], dayfirst=True)
    # Ensure the Date column is in datetime format
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce').dt.date
    return data

# Load data
data_path = 'fake_data.csv'  # Update this to your actual data file path
data = load_data(data_path)

# Streamlit app design
st.title("Expense Tracking App")
st.write("This app shows the total amount spent and estimates the savings based on user input for category, date range, location, and merchant.")

# Sidebar inputs
st.sidebar.header("Filter Options")

# Category selection
category = st.sidebar.selectbox("Category", options=["All"] + list(data['Category'].unique()))

# Location selection
location = st.sidebar.selectbox("Location", options=["All"] + list(data['Location'].unique()))

# Merchant selection
merchant = st.sidebar.selectbox("Merchant", options=["All"] + list(data['Merchant'].unique()))

# Date range selection
start_date = st.sidebar.date_input("Start Date", value=min(data['Date']))
end_date = st.sidebar.date_input("End Date", value=max(data['Date']))

# Account balance input
account_balance = st.sidebar.number_input("Account Balance", value=0.0)

# Filter data based on inputs
filtered_data = data[
    (data['Date'] >= start_date) &
    (data['Date'] <= end_date)
]

if category != "All":
    filtered_data = filtered_data[filtered_data['Category'] == category]

if location != "All":
    filtered_data = filtered_data[filtered_data['Location'] == location]

if merchant != "All":
    filtered_data = filtered_data[filtered_data['Merchant'] == merchant]

# Calculate total amount spent
total_amount_spent = filtered_data['Amount'].sum()

# Calculate savings
savings = account_balance - total_amount_spent

# Display results
st.header("Total Amount Spent and Estimated Savings")
st.write(f"From {start_date} to {end_date},")
st.write(f"Category: {category if category != 'All' else 'All'}")
st.write(f"Location: {location if location != 'All' else 'All'}")
st.write(f"Merchant: {merchant if merchant != 'All' else 'All'}")
st.write(f"Total Amount Spent: ₹{total_amount_spent:.2f}")
st.write(f"Account Balance: ₹{account_balance:.2f}")
st.write(f"Estimated Savings: ₹{savings:.2f}")

# Optional: Display filtered data table
if st.checkbox("Show Filtered Data"):
    st.write(filtered_data)
