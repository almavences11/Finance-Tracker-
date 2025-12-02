import streamlit as st
import pandas as pd
import plotly.express as px 

# Set Streamlit page configuration
st.set_page_config(page_title="Finance Tracker App", page_icon="💰", layout="wide") 
 



# function to load and process transactions 
def load_transactions(file):

    # Loads the CSV file, categorizes transactions, and returns a DataFrame. 
    # If an error occurs, shows a message and returns None. 

    
    try: 
        # Load CSV file into a DataFrame
        df = pd.read_csv(file)

        # Clean column names (removes extra spaces)
        df.columns = [col.strip() for col in df.columns]

        #Convert 'Date' to datetime format
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y") 

        #Categorize transactions based on predefined mapping
        
        # Map categories/merchant names to broader groups
        category_map = {
            "Grocery": "Shopping",
            "Amazon": "Shopping", 
            "Card Payment": "Shopping",
            "Coffee Shop": "Food & Drink",
            "Uber": "Transport", 
            "Internet": "Bills",
            "Health Insurance": "Bills",
            "Netflix": "Entertainment",
            "Ventra": "Transport",
        }  

        # apply mapping to create a new column 'Category_Group'
        df["Category_Group"] = df["Category"].map(category_map)


        # Display the cleaned and categorized DataFrame
        st.subheader("All Transactions")
        st.dataframe(df)

        # return the processed DataFrame
        return df 
    except Exception as e:
        # If an error occurs, show a friendly error message and return None
        st.error(f"Error loading file: {str(e)}")
        return None 


# main function to run the Streamlit app 
def main(): 

    st.title("Finance Dashboard 💰")
    st.markdown("Track your income and expenses effortlessly!")
     
    # File uploader widget 
    uploaded_file = st.file_uploader("Upload your finance data (CSV) file", type=["csv"])

    # only process if a file is uploaded
    if uploaded_file is not None:
        df = load_transactions(uploaded_file) # calls the function to load and process transactions from the CSV 

        # only continue if the file was loaded successfully 
        if df is not None:

            #Group Expenses by category 
            grouped = df.groupby("Category_Group")["Amount"].sum().reset_index()


            st.subheader("Total Expenses by Category")
            st.dataframe(grouped) # show the grouped totals 

            # Plot a pie chart of expenses by category 
            fig = px.pie(grouped, names="Category_Group", values="Amount", title="Expenses by Category")
            st.plotly_chart(fig)
               
# run the app
main() 



       
        
       



