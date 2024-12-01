import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_recommendations():
    st.title("Recommendations")
    
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

def show_recommendations():
    st.subheader("Recommendations")
    
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
