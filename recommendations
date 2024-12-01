import streamlit as st
import pandas as pd

def show_recommendations():
    st.title("Recommendations")
    
    if 'data' in st.session_state:
        data = st.session_state.data
        
        product_id = st.selectbox("Select a Product ID", data['Product_ID'].unique())
        selected_category = data.loc[data['Product_ID'] == product_id, 'Product_Category'].values[0]

        recommendations = data[data['Product_Category'] == selected_category]
        recommendations = recommendations[recommendations['Product_ID'] != product_id]

        st.subheader("Recommended Products")
        if not recommendations.empty:
            st.write(recommendations[['Product_ID', 'Product_Category', 'Orders']])
        else:
            st.write("No recommendations available for this product.")
    else:
        st.warning("Please upload a CSV file to see recommendations.")
