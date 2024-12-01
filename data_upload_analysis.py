import streamlit as st
import pandas as pd
import chardet

def data_analysis():
    st.subheader("Data Upload & Analysis")

    # File uploader
    uploaded_file = st.file_uploader("Upload your Diwali sales data (CSV)", type=["csv"])

    if uploaded_file is not None:
        # Detect encoding
        rawdata = uploaded_file.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']
        
        # Move the cursor back to the beginning of the file
        uploaded_file.seek(0)

        # Read the data with the detected encoding
        try:
            data = pd.read_csv(uploaded_file, encoding=encoding)
            st.success("File loaded successfully!")

            # Store the DataFrame in session state
            st.session_state.data = data

            # Display the first few rows and columns of the dataframe
            st.write("Preview of the data:")
            st.dataframe(data.head())
            st.write("Columns in the dataset:", data.columns.tolist())

            # Drop empty columns
            empty_columns = data.columns[data.isnull().all()]
            if not empty_columns.empty:
                data.drop(empty_columns, axis=1, inplace=True)
                st.warning(f"Removed empty columns: {list(empty_columns)}")

            # Basic Analysis
            st.subheader("Basic Analysis")
            st.write("Total Number of Entries:", len(data))
            if 'Amount' in data.columns:
                st.write("Total Amount Spent:", data['Amount'].sum())
            if 'Orders' in data.columns:
                st.write("Total Number of Orders:", data['Orders'].sum())
            
            # Filter by Age Group
            if 'Age Group' in data.columns:
                age_group = st.selectbox("Select Age Group", data['Age Group'].unique())
                filtered_data = data[data['Age Group'] == age_group]
                st.write(f"Data for Age Group '{age_group}':")
                st.dataframe(filtered_data)

        except Exception as e:
            st.error(f"Error reading the CSV file: {e}")
            
