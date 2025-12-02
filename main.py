import streamlit as st
import pandas as pd
import plotly.express as px
import json 
import os 

st.set_page_config(page_title="Finance Tracker App", page_icon="💰", layout="wide") 
 




def load_transactions(file):
    try: 
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns]
        df["Amount"] = df["Amount"].str.replace(",", "").astype(float)
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y") 

        st.write(df) 
        return df 
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None 


def main(): 

    st.title("Finance Dashboard 💰")
    st.markdown("Track your income and expenses effortlessly!")
     

    uploaded_file = st.file_uploader("Upload your finance data (CSV) file", type=["csv"])

    if uploaded_file is not None:
        df = load_transactions(uploaded_file)
        if df is not None:
            # Categorize transactions based on merchant/details
            def categorize_details(details: str) -> str:
                d = str(details).lower()
                # simple keyword-based categories (adjust as needed)
                if any(k in d for k in ["lulu", "spinneys", "noon", "amazon", "book", "supermarket", "hypermarket"]):
                    return "Groceries & Shopping"
                if any(k in d for k in ["uber", "taxi", "careem", "metro", "transport"]):
                    return "Transport"
                if any(k in d for k in ["etihad", "booking", "hilton", "airways", "hotel", "flight"]):
                    return "Travel"
                if any(k in d for k in ["netflix", "spotify", "apple.com bill", "subscription"]):
                    return "Subscriptions"
                if any(k in d for k in ["adcb bank fee", "bank fee", "fee"]):
                    return "Bank Fees"
                if any(k in d for k in ["card payment received", "payment received", "refund"]):
                    return "Income"
                if any(k in d for k in ["insurance", "emirates insurance"]):
                    return "Insurance"
                if any(k in d for k in ["zomato", "uber eats", "restaurant", "dining"]):
                    return "Food & Dining"
                # default
                return "Other"

            df["Category"] = df["Details"].apply(categorize_details)

            # Group expenses by category (sum amounts)
            grouped = df.groupby("Category", as_index=False)["Amount"].sum().sort_values("Amount", ascending=False)

            st.subheader("Expenses by Category")
            st.dataframe(grouped)

            # show bar chart
            fig = px.bar(grouped, x="Category", y="Amount", title="Spending by Category", labels={"Amount": "Total Amount (numeric)"})
            st.plotly_chart(fig, use_container_width=True)
main() 



       
        
       



