#  data sweeper app

import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper 📊", layout='wide')

# Define colors for styling
HEADER_COLOR = '#ff6347'  # Tomato color
TEXT_COLOR = '#2f4f4f'  # Dark Slate

# Sidebar 
st.sidebar.write("<h1 style='font-size: 40px;'>DATA SWEEPER</h1>", unsafe_allow_html=True)
sidebar_option = ["Home", "Data Operations"]
page = st.sidebar.selectbox("select a section ", sidebar_option)
st.sidebar.write("Thanks for choosing **Data Sweeper**! 🚀 Let's transform your data! 🙌")
if page == "Home":
    st.markdown(f"<h1 style='text-align: center; color: {HEADER_COLOR}; font-size: 45px;'>Welcome to Data Sweeper 📊✨</h1>", unsafe_allow_html=True)

    # Introduction Section
    st.subheader("Introduction")
    st.write("""
        Data Sweeper helps you easily clean and visualize your data. Upload your CSV or Excel files, choose from various cleaning options, and visualize them before converting them back to your preferred format.
        You can also download the cleaned data directly!
    """)

    # Features of Data Sweeper Section
    st.subheader("Features of Data Sweeper")
    st.write("""
        - **Easy File Upload**: Upload your CSV or Excel files effortlessly.
        - **Data Cleaning Tools**: Remove duplicates, fill missing values, and choose columns to work with.
        - **Interactive Visualization**: Create bar charts to explore your data.
        - **File Conversion**: Convert your cleaned data back to CSV or Excel format.
    """)

    st.subheader("Why Data Sweeper? 🌟")
    st.write(""
          "Data Sweeper makes data management easy and fast. With an intuitive interface and powerful features, it helps you turn your data into valuable insights with just a few clicks. Whether you're new to data or experienced, Data Sweeper gives you the tools to work efficiently and save time."
         "")
    # Line separator
    st.markdown("<hr style='border: 1px solid #ff6347; margin: 30px 0;'>", unsafe_allow_html=True)

    # Copyright section
    st.markdown(f"<div style='text-align: center; color: {TEXT_COLOR}; font-size: 18px;'>", unsafe_allow_html=True)
    st.write("**Copyright** 2025 | Designed by Kristina | All Rights Reserved")
    
    #  page 2 data sweeper
elif page == "Data Operations":
    st.title("Smart Data Management 📊")

    # Upload files
    st.write("Transfrom your files between CSV and Excel formats with built-in data cleaning and visualization")
    uploaded_files = st.file_uploader("📂Upload Your Data (CSV/Excel):", type=["CSV", "Xlsx"], accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            file_ext = os.path.splitext(file.name)[-1].lower()

            # Handle CSV files
           # Handle file
            if file_ext ==".csv":
               df =pd.read_csv(file)
            elif file_ext ==".xlsx":
               df =pd.read_excel(file)
            else:
               st.error(f"Unsupported file type: {file_ext}")
               continue  
            # Display file info
            st.write(f"📄 File Name: {file.name}")
            st.write(f"💾 File Size: {file.size / 1024:.2f} KB")

            # Show 5 rows 
            st.subheader("👀 Quick Look at Your Data 📊")
            st.dataframe(df.head())

            # Data cleaning options
            st.subheader("💡 Data Transformation Tools")
            if st.checkbox(f" Refine Data for {file.name}"):
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"🚫 Eliminate Duplicates in {file.name}"):
                        df.drop_duplicates(inplace=True)
                        st.write(" ✅ Duplicate Removed!")
                with col2:
                    if st.button(f"✨ Fill Gaps in {file.name}"):
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write(" ✅ Missing values have been filled!")

                # Choose specific columns
                st.subheader("🔢 Select Columns for Analysis")
                columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
                df = df[columns]

                # Data visualization options
                st.subheader("📈 Data Insights & Visualization")
                if st.checkbox(f"Display Visualization for {file.name} 📊"):
                    st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

                # File conversion options
                st.subheader("🔁 File Conversion Choices")
                conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
                if st.button(f"Convert {file.name} 🔄"):
                    buffer = BytesIO()
                    if conversion_type == "CSV":
                        df.to_csv(buffer, index=False)
                        file_name = file.name.replace(file_ext, ".csv")
                        mime_type = "text/csv"
                    elif conversion_type == "Excel":
                        df.to_excel(buffer, index=False)
                        file_name = file.name.replace(file_ext, ".xlsx")
                        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    buffer.seek(0)

                    # Download button
                    st.download_button(
                        label=f"Download {file.name} as {conversion_type} 📥",
                        data=buffer,
                        file_name=file_name,
                        mime=mime_type
                    )

      # success message  
    st.success("✅  All Files Have Been Successfully Processed! ✔️")
