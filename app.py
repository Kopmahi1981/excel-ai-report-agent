import os
import streamlit as st
import pandas as pd
import plotly.express as px
from analyzer import analyze_data
from ai_agent import generate_ai_report
from exporter import create_pdf_report

st.set_page_config(
    page_title="KRISH AI EXCEL REPORT AGENT PRO",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("🚀 AI Excel Report Agent v4.0")

st.sidebar.caption(
    "Clean • Analyze • Generate AI Reports"
)

st.sidebar.success("Version 4.0 Universal")

st.sidebar.markdown("---")

st.sidebar.markdown("### ✅ Features")

st.sidebar.write("✔ Data Cleaning")
st.sidebar.write("✔ Executive Dashboard")
st.sidebar.write("✓ Universal Charts")
st.sidebar.write("✓ AI Insights")
st.sidebar.write("✓ Ask Questions")
st.sidebar.write("✔ PDF Export")
st.sidebar.write("✔ Dataset Download")

st.sidebar.markdown("---")

st.sidebar.info("🚀 Upload Any Excel or CSV Dataset")
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
        # fig.write_image("chart.png")
        # bar_fig.write_image("barchart.png")
        # pie_fig.write_image("piechart.png")

        st.plotly_chart(fig, use_container_width=True)

    # ==========================
    # Missing Values Chart
    # ==========================

    missing_data = pd.DataFrame({
        "Metric": ["Missing Values"],
        "Count": [df.isnull().sum().sum()]
    })

    missing_fig = px.bar(
        missing_data,
        x="Metric",
        y="Count",
        title="Missing Values Overview"
    )

    st.plotly_chart(
        missing_fig,
        use_container_width=True
    )

    # ==========================
    # Category Chart
    # ==========================

    cat_cols = df.select_dtypes(
        include="object"
    ).columns

    if len(cat_cols) > 0:

        top_col = cat_cols[0]

        category_data = (
            df[top_col]
            .value_counts()
            .head(10)
            .reset_index()
        )

        category_data.columns = [
            top_col,
            "Count"
        ]

        cat_fig = px.bar(
            category_data,
            x=top_col,
            y="Count",
            title=f"Top {top_col} Categories"
        )

        st.plotly_chart(
            cat_fig,
            use_container_width=True
        )

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

        st.success(
    "✅ Analysis Completed Successfully"
)

        st.caption(
        "Dataset cleaned, analyzed and AI report generated successfully."
)

        # ==========================
        # Executive Dashboard
        # ==========================
        
        rows = len(cleaned_df)

        columns = len(cleaned_df.columns)
        missing_values = cleaned_df.isnull().sum().sum()
        duplicate_rows = cleaned_df.duplicated().sum()

        numeric_cols = cleaned_df.select_dtypes(include="number")
        numeric_count = len(numeric_cols.columns)

        numeric_cols = cleaned_df.select_dtypes(include="number")

        numeric_count = len(numeric_cols.columns)

        if numeric_count > 0:
            total_numeric_values = numeric_cols.sum().sum()
            avg_numeric_value = numeric_cols.mean().mean()
        else:
            total_numeric_values = 0
            avg_numeric_value = 0

        before_quality_score = max(
            0,
            round(
                100 - (
                    ((duplicates_found + missing_before) / rows) * 100
                ),
                2
            )
        )

        after_quality_score = max(
            0,
            round(
                100 - (
                    ((duplicate_rows + missing_after) / rows) * 100
                ),
            2
        )
    )
        
        st.subheader("📊 Executive Dashboard")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📄 Records", rows)

        with col2:
            st.metric("📊 Columns", columns)

        with col3:
            st.metric("⚠ Missing", missing_values)

        with col4:
            st.metric("🔁 Duplicates", duplicate_rows)


        col5, col6, col7 = st.columns(3)

        with col5:
            st.metric(
                "🔢 Numeric Fields",
                numeric_count
            )

        with col6:
            st.metric(
                "📈 Avg Numeric Value",
                f"{avg_numeric_value:,.2f}"
            )

        with col7:
            st.metric(
                "🧮 Total Numeric Sum",
                f"{total_numeric_values:,.0f}"
    )

    # ==========================
    # Dataset Profile
    # ==========================

    st.subheader("📋 Dataset Profile")

    numeric_cols = df.select_dtypes(include="number").columns
    text_cols = df.select_dtypes(include="object").columns

    try:
        date_cols = df.select_dtypes(include=["datetime"]).columns
    except:
        date_cols = []

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🔢 Numeric Fields",
            len(numeric_cols)
        )

    with col2:
        st.metric(
            "📝 Text Fields",
            len(text_cols)
        )

    with col3:
        st.metric(
            "📅 Date Fields",
            len(date_cols)
        )

    # col_before, col_after = st.columns(2)

    # with col_before:
    #     st.error(
    #         f"""
    #         BEFORE CLEANING

    #         Duplicates Found: {duplicates_found}

    #         Missing Values: {missing_before}

    #         Quality Score: {before_quality_score}/100
    #         """
    #     )

    # with col_after:
    #     st.success(
    #         f"""
    #         AFTER CLEANING

    #         Duplicates Remaining: {duplicate_rows - duplicates_removed}

    #         Missing Values Remaining: {missing_after}

    #         Quality Score: {after_quality_score}/100
    #         """
    #     )
        
        #st.subheader("🧹 Data Cleaning Audit")

        # st.write("Duplicates Found:", duplicates_found)

        # st.write("Duplicates Removed:", duplicates_removed)

        # st.write("Missing Values Found:", missing_before)

        # st.write("Missing Values Fixed:", missing_fixed)

        # st.write("Remaining Missing Values:", missing_after)

        # st.success("Dataset Cleaned Successfully")
        
    basic_analysis = analyze_data(df)

    try:
        ai_report = f"""
    # Executive Summary

    Dataset contains {df.shape[0]} records and {df.shape[1]} columns.

    # Dataset Overview

    Total Records: {df.shape[0]}
    Total Columns: {df.shape[1]}

    # Data Quality

    Missing Values: {df.isnull().sum().sum()}
    Duplicate Rows: {df.duplicated().sum()}

    # Key Insights

    The dataset has been analyzed successfully.
    Numeric and categorical fields were detected automatically.

    # Recommendations

    1. Review missing values regularly.
    2. Monitor duplicate records.
    3. Standardize data formats.
    4. Use dashboard insights for decision making.
    """
        
        # # ==========================
        # # Ask Questions
        # # ==========================
        # st.markdown("---")

        # st.subheader("💬 Ask Questions About Your Dataset")

        # user_question = st.text_input(
        #     "Ask anything about your uploaded dataset..."
        # )

        # if user_question:

        #     st.info(
        #         f"Question received: {user_question}"
        #     )

        #     st.success(
        #         "🚀 Advanced AI Query Engine Coming In Version 5.0"
        #     )

        st.subheader("🤖 AI Business Insights")

        with st.expander("View AI Analysis", expanded=True):
            st.markdown(ai_report)

    except Exception as e:
        st.error(f"AI REPORT ERROR: {e}")
    avg_numeric_value = 0
    numeric_max = 0
    numeric_min = 0

    pdf_file = create_pdf_report(
        ai_report,
        rows=df.shape[0],
        columns=df.shape[1],
        missing_values=df.isnull().sum().sum(),
        column_names=df.columns.tolist(),
        statistics=df.describe().to_dict(),
        duplicate_rows=df.duplicated().sum(),
        avg_numeric_value=avg_numeric_value,
        numeric_max=numeric_max,
        numeric_min=numeric_min,
        duplicates_found=duplicates_found,
        duplicates_removed=duplicates_removed,
        missing_before=missing_before,
        missing_fixed=missing_fixed,
        missing_after=missing_after
    )

if 'pdf_file' in locals():

    st.success(f"PDF Created: {pdf_file}")

    st.markdown("---")
    st.subheader("📥 Downloads")
    st.success("PDF CREATED")
    with open(pdf_file, "rb") as file:
        st.download_button(
            label="📄 Download AI Report PDF",
            data=file,
            file_name=pdf_file,
            mime="application/pdf"
        )
    with open("cleaned_dataset.xlsx", "rb") as file:
        st.download_button(
            label="📥 Download Cleaned Dataset",
            data=file,
            file_name="cleaned_dataset.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# st.subheader("📈 Basic Analysis")
# st.write(basic_analysis)