import os
import streamlit as st
import pandas as pd
import plotly.express as px
from analyzer import analyze_data
from ai_agent import generate_ai_report
from exporter import create_pdf_report

st.set_page_config(
    page_title="Excel AI Report Agent",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Excel AI Report Agent")
st.caption(
    "Upload Excel → Analyze Data → Generate AI Insights → Export Professional Reports"
)
st.divider()
with st.sidebar:

    st.title("📊 Excel AI Agent")

    st.success("Version 3.0")

    st.markdown("---")

    st.subheader("Features")

    st.write("✅ Data Cleaning")
    st.write("✅ Executive Dashboard")
    st.write("✅ AI Insights")
    st.write("✅ PDF Export")
    st.write("✅ Dataset Download")

    st.markdown("---")

    st.info(
        "Upload an Excel file to generate AI-powered business insights and reports."
    )
uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx", "xls", "csv"]
)
def generate_fallback_report(df):
    return f"""
# AI Business Insights (Fallback)

Dataset Summary

• Total Rows: {df.shape[0]}
• Total Columns: {df.shape[1]}
• Missing Values: {df.isnull().sum().sum()}
• Duplicate Rows: {df.duplicated().sum()}

Recommendations:
• Review missing values
• Validate critical columns
• Check for data consistency
• Monitor duplicate records

Fallback report generated because AI service was unavailable.
"""

st.set_page_config(page_title="AI Excel Report Agent", layout="wide")

if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    else:
        df = pd.read_excel(uploaded_file)

    # Fix one-column Excel files
    if len(df.columns) == 1:

        df = df[df.columns[0]].str.split(",", expand=True)

        df.columns = [
            "Investor Name",
            "PAN Number",
            "City",
            "Investment Type",
            "Investment Amount",
            "Annual Return %"
        ]

        df["Investment Amount"] = pd.to_numeric(
            df["Investment Amount"],
            errors="coerce"
        )

        df["Annual Return %"] = pd.to_numeric(
            df["Annual Return %"],
            errors="coerce"
        )
    st.success("File uploaded successfully!")

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    st.subheader("📌 Dataset Information")
    st.write(df.describe())

    numeric_columns = df.select_dtypes(include=['number']).columns

    if len(numeric_columns) > 0:

        selected_column = st.selectbox(
            "Select Column for Chart",
            numeric_columns
        )
        fig = px.histogram(
            df,
            x=selected_column,
            title=f"{selected_column} Distribution"
        )

        bar_fig = px.bar(
        df.head(10),
        x="Investor Name",
        y="Investment Amount",
        title="Top Investment Amounts"
        )
        pie_fig = px.pie(
        df,
        names="Investment Type",
        values="Investment Amount",
        title="Investment Type Distribution"
        )
        pie_fig.write_image("piechart.png")
        bar_fig.write_image("barchart.png")
        fig.write_image("chart.png")

        st.plotly_chart(fig, use_container_width=True)

        if st.button("Generate AI Report"):

            with st.spinner("Analyzing data with AI..."):

                basic_analysis = analyze_data(df)

            try:
                ai_report = generate_ai_report(df)
                report_source = "Gemini AI"

            except Exception as e:
                st.warning("Gemini unavailable. Using fallback report.")
                ai_report = generate_fallback_report(df)
                report_source = "Fallback AI"

            st.info(f"Report Source: {report_source}")

            st.subheader("🤖 AI Business Insights")
            st.write(ai_report)

        cleaned_df = df.copy()

        # Remove duplicates
        cleaned_df = cleaned_df.drop_duplicates()

        # Fill missing numeric values with median
        for col in cleaned_df.select_dtypes(include="number").columns:
            cleaned_df[col] = cleaned_df[col].fillna(
                cleaned_df[col].median()
            )

        # Fill missing text values with "Unknown"
        for col in cleaned_df.select_dtypes(include="object").columns:
            cleaned_df[col] = cleaned_df[col].fillna(
                "Unknown"
            )
        duplicates_found = df.duplicated().sum()

        duplicates_removed = duplicates_found

        missing_before = df.isnull().sum().sum()

        missing_after = cleaned_df.isnull().sum().sum()

        missing_fixed = missing_before - missing_after

        # ==========================
        # Executive Dashboard
        # ==========================
        
        rows = len(cleaned_df)

        average_investment = 0
        highest_investment = 0
        lowest_investment = 0

        if "Investment Amount" in cleaned_df.columns:
            average_investment = cleaned_df["Investment Amount"].mean()
            highest_investment = cleaned_df["Investment Amount"].max()
            lowest_investment = cleaned_df["Investment Amount"].min()
            st.subheader("📊 Executive Dashboard")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Records", f"{rows:,}")

            with col2:
                st.metric(
                    "Average Investment",
                    f"₹{average_investment:,.2f}"
                )

            with col3:
                st.metric(
                    "Highest Investment",
                    f"₹{highest_investment:,.2f}"
                )

                
        lowest_investment = cleaned_df["Investment Amount"].min()

        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.metric(
                "Lowest Investment",
                f"₹{0 if 'lowest_investment' not in locals() else lowest_investment:,.2f}"
            )

        with col5:
            st.metric(
                "Duplicates Removed",
                duplicates_removed
        )

        with col6:
            st.metric(
                "Missing Values Fixed",
                missing_fixed
            )
        st.subheader("🧹 Data Cleaning Audit")

        st.write("Duplicates Found:", duplicates_found)

        st.write("Duplicates Removed:", duplicates_removed)

        st.write("Missing Values Found:", missing_before)

        st.write("Missing Values Fixed:", missing_fixed)

        st.write("Remaining Missing Values:", missing_after)

        st.success("Dataset Cleaned Successfully")
        
    basic_analysis = analyze_data(df)

    try:
        ai_report = generate_ai_report(df)

        if ai_report.startswith("AI ERROR:"):
            st.warning("Gemini quota exceeded. Using local fallback report.")

            ai_report = f"""
    Executive Summary
    Dataset contains {df.shape[0]} records and {df.shape[1]} columns.

    Key Trends
    Average Investment: ₹{df['Investment Amount'].mean():,.2f}

    Important Insights
    Highest Investment: ₹{df['Investment Amount'].max():,.2f}
    Lowest Investment: ₹{df['Investment Amount'].min():,.2f}

    Business Recommendations
    1. Review duplicate records.
    2. Monitor missing values regularly.
    3. Focus on high-value investments.
    4. Improve data quality controls.
    """

        else:
            st.success("AI REPORT CREATED")

    except Exception as e:
            st.error(f"AI REPORT ERROR: {e}")
            st.stop()
    try:
        pdf_file = create_pdf_report(
        ai_report,
        rows=df.shape[0],
        columns=df.shape[1],
        missing_values=df.isnull().sum().sum(),
        column_names=df.columns.tolist(),
        statistics=df.describe().to_dict(),
        duplicate_rows=df.duplicated().sum(),
        average_investment=df["Investment Amount"].mean(),
        highest_investment=df["Investment Amount"].max(),
        lowest_investment=df["Investment Amount"].min(),
        
        duplicates_found=duplicates_found,
        duplicates_removed=duplicates_removed,
        missing_before=missing_before,
        missing_fixed=missing_fixed,
        missing_after=missing_after
    )
        st.success(f"PDF CREATED: {pdf_file}")

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="📥 Download AI Report PDF",
                data=file,
                file_name=pdf_file,
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"PDF ERROR: {e}")
        st.stop()

with open("cleaned_dataset.xlsx", "rb") as file:
    st.download_button(
        label="📥 Download Cleaned Dataset",
        data=file,
        file_name="cleaned_dataset.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# st.subheader("📈 Basic Analysis")
# st.write(basic_analysis)