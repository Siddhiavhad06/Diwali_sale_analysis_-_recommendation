import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import chardet

# Title of the dashboard
st.title("Diwali Sales Analysis")

# Display an image
image_path =r"C:\Users\Sanika\OneDrive\Desktop\SEM 7\Big data analaytics\BDAProject\di.jpg"

image = Image.open(image_path)
st.image(image, caption='Celebrating Diwali Sales', width=300)

# Sidebar for navigation
st.sidebar.title("Dashboard")
page = st.sidebar.radio("Select Page", ["Data Upload & Analysis", "Visualizations", "Recommendations"])

if page == "Data Upload & Analysis":
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

        except Exception as e:
            st.error(f"Error reading the CSV file: {e}")
            st.stop()

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


elif page == "Visualizations":
    if 'data' in st.session_state:
        data = st.session_state.data

        # Visualization for Order Amount Distribution
        if 'Amount' in data.columns:
            st.subheader("Order Amount Distribution")
            st.bar_chart(data['Amount'].value_counts())

        # Pie Chart for Amount Distribution by Age Group
        if 'Age Group' in data.columns:
            st.subheader("Amount Distribution by Age Group")
            age_group_amount = data.groupby('Age Group')['Amount'].sum()
            plt.figure(figsize=(10, 6))
            plt.pie(age_group_amount, labels=age_group_amount.index, autopct='%1.1f%%', startangle=140)
            plt.title('Amount Distribution by Age Group')
            st.pyplot(plt)
            
        # Check for necessary columns
        if 'Product_ID' in data.columns and 'Orders' in data.columns:
            product_recommendations = data.groupby('Product_ID')['Orders'].sum().sort_values(ascending=False).head(10)
            plt.figure(figsize=(10, 6))
            wedges, texts, autotexts = plt.pie(product_recommendations, labels=product_recommendations.index,
                                                autopct='%1.1f%%', startangle=140, colors=plt.cm.tab10.colors)

            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)

            plt.tight_layout()
            plt.title('Top 10 Recommended Products Based on Orders')
            st.pyplot(plt)
        else:
            st.warning("The necessary columns 'Product_ID' and 'Orders' are not found in the data.")
    else:
        st.warning("Please upload a CSV file to see visualizations.")

elif page == "Recommendations":
    if 'data' in st.session_state:
        data = st.session_state.data

        # Check for necessary columns
        required_columns = ['Product_ID', 'Product_Category', 'Orders']
        if not all(col in data.columns for col in required_columns):
            st.error("Required columns 'Product_ID', 'Product_Category', or 'Orders' are missing.")
        else:
            # Calculate the total orders for each product
            total_orders = data.groupby('Product_ID')['Orders'].sum().sort_values(ascending=False)
            
            # Display the product selection for recommendations
            product_id = st.selectbox("Select a Product ID", total_orders.index)

            # Get the product category of the selected product
            selected_product_category = data.loc[data['Product_ID'] == product_id, 'Product_Category'].values[0]

            # Recommend products within the same category, excluding the selected product
            recommendations = data[data['Product_Category'] == selected_product_category]
            recommendations = recommendations[recommendations['Product_ID'] != product_id]

            if not recommendations.empty:
                st.subheader(f"Recommended Products in the '{selected_product_category}' Category")
                recommended_products = recommendations[['Product_ID', 'Product_Category', 'Orders']].sort_values(by='Orders', ascending=False)
                st.write(recommended_products)
            else:
                st.write("No recommendations available for this product.")

    else:
        st.warning("Please upload a CSV file to see recommendations.")
