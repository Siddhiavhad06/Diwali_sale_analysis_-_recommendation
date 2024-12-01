import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_visualizations():
    st.title("Visualizations")
    
    if 'data' in st.session_state:
        data = st.session_state.data

        # Example: Show a simple bar chart for Orders distribution
        st.subheader("Orders Distribution")
        order_counts = data['Orders'].value_counts()
        plt.figure(figsize=(10, 5))
        plt.bar(order_counts.index.astype(str), order_counts.values, color='skyblue')
        plt.xlabel('Number of Orders')
        plt.ylabel('Frequency')
        plt.title('Distribution of Orders')
        plt.xticks(rotation=45)
        st.pyplot(plt)
    else:
        st.warning("Please upload a CSV file to see visualizations.")
