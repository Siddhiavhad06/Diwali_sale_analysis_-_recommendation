import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_visualizations():
    st.title("Visualizations")
    
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
