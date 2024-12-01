import streamlit as st
from data_upload_analysis import data_analysis
from visualizations import show_visualizations
from recommendations import show_recommendations

def main():
    st.set_page_config(page_title="Diwali Sales Analysis")

    st.sidebar.title("Dashboard")
    page = st.sidebar.radio("Select Page", ["Data Upload & Analysis", "Visualizations", "Recommendations"])

    if page == "Data Upload & Analysis":
        data_analysis()
    elif page == "Visualizations":
        show_visualizations()
    elif page == "Recommendations":
        show_recommendations()

if __name__ == "__main__":
    main()
