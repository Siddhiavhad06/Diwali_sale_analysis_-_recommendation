import streamlit as st
import pandas as pd
import chardet

def data_analysis():
    st.title("Data Upload & Analysis")

    uploaded_file = st.file_uploader("Upload your Diwali sales data (CSV)", type=["csv"])

    if uploaded_file is not None:
        rawdata = uploaded_file.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']
        uploaded_file.seek(0)

        try:
            data = pd.read_csv(uploaded_file, encoding=encoding)
            st.success("File loaded successfully!")
            st.session_state.data = data

            st.write("Preview of the data:")
            st.dataframe(data.head())
            st.write("Columns in the dataset:", data.columns.tolist())

            if 'Amount' in data.columns:
                st.write("Total Amount Spent:", data['Amount'].sum())
            if 'Orders' in data.columns:
                st.write("Total Number of Orders:", data['Orders'].sum())
                
        except Exception as e:
            st.error(f"Error reading the CSV file: {e}")
