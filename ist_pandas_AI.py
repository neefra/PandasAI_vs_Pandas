import os
import pandas as pd
import streamlit as st
import plotly.express as px
from pandasai import SmartDataframe

# Set the API key for PandasAI
os.environ["PANDASAI_API_KEY"] = "$2a$10$zWmz3161O5jKOAisXyP4HeVZmoFtjV.SMm8FMfnVK57mH3kstmBiS"

# Set custom background color using HTML and CSS
st.markdown(
    """
    <style>
    body {
        background-color: #f0f8ff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add a panda image at the top of the page
st.image("https://github.com/neefra/PandasAI_vs_Pandas/blob/main/PandaAi.jpg", width=200)

# Streamlit app title
st.title("Data Analysis & Visualization with PandasAI")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload a CSV file for analysis and visualization", type=['csv'])

if uploaded_file is not None:
    # Load the uploaded file into a DataFrame
    df = pd.read_csv(uploaded_file)
    st.write("Dataset Preview:")
    st.write(df.head())

    # PandasAI Section
    st.header("Prompt-driven Data Analysis")
    prompt = st.text_area("Enter your prompt for analysis:")

    if st.button("Generate Response"):
        if prompt:
            with st.spinner("Generating response..."):
                try:
                    # Convert DataFrame to SmartDataframe and generate response
                    sdf = SmartDataframe(df)
                    response = sdf.chat(prompt)
                    st.success("Response generated!")
                    st.write(response)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a prompt.")

    # Visualization Section
    st.header("Data Visualization")

    # Separate numeric and categorical columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns

    # Sidebar for Visualization Options
    st.sidebar.header("Visualization Options")
    chart_type = st.sidebar.selectbox("Chart Type:", ['Scatter', 'Bar', 'Line', 'Categorical'])

    if chart_type in ['Scatter', 'Bar', 'Line'] and not numeric_columns.empty:
        x_axis = st.sidebar.selectbox("X-axis (Numerical):", options=numeric_columns)
        y_axis = st.sidebar.selectbox("Y-axis (Numerical):", options=numeric_columns)
    elif chart_type == 'Categorical' and not categorical_columns.empty:
        x_axis = st.sidebar.selectbox("X-axis (Categorical):", options=categorical_columns)

    if st.sidebar.button("Generate Chart"):
        if chart_type == 'Scatter' and x_axis and y_axis:
            fig = px.scatter(df, x=x_axis, y=y_axis, title=f"Scatter Plot: {x_axis} vs {y_axis}")
        elif chart_type == 'Bar' and x_axis and y_axis:
            fig = px.bar(df, x=x_axis, y=y_axis, title=f"Bar Plot: {x_axis} vs {y_axis}")
        elif chart_type == 'Line' and x_axis and y_axis:
            fig = px.line(df, x=x_axis, y=y_axis, title=f"Line Plot: {x_axis} vs {y_axis}")
        elif chart_type == 'Categorical' and x_axis:
            category_counts = df[x_axis].value_counts().reset_index()
            category_counts.columns = [x_axis, 'Count']
            fig = px.bar(category_counts, x=x_axis, y='Count', title=f"Count of {x_axis}")
        else:
            st.warning("Please select appropriate columns for the chart.")
            fig = None

        if fig:
            st.plotly_chart(fig)
