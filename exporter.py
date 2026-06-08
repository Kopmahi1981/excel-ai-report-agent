from fpdf import FPDF
from datetime import datetime

from streamlit import pdf

class PDF(FPDF):

    def footer(self):

        self.set_y(-15)

        self.set_font("Arial", "I", 10)

        self.cell(
            0,
            10,
            f"KRISH AI Excel Report Agent | Page {self.page_no()}",
            0,
            0,
            "C"
        )

def create_pdf_report(
    ai_report,
    rows,
    columns,
    missing_values,
    column_names,
    statistics,
    duplicate_rows,
    average_investment,
    highest_investment,
    lowest_investment,
    duplicates_found,
    duplicates_removed,
    missing_before,
    missing_fixed,
    missing_after
):

    pdf = PDF()
    pdf.set_font("Arial", "B", 16)

    # KPI Calculations
    completeness = (
        ((rows * columns) - missing_values)
        / (rows * columns)
    ) * 100

    duplicate_percentage = (
    duplicate_rows / rows
    ) * 100

    quality_score = round(
    max(0, completeness - duplicate_percentage),
    2
    )

    if quality_score >= 90:
            health_status = "Excellent"

    elif quality_score >= 70:
            health_status = "Good"

    elif quality_score >= 50:
            health_status = "Warning"

    else:
            health_status = "Critical"

    if quality_score >= 90:
        risk_level = "Low"

    elif quality_score >= 70:
        risk_level = "Moderate"

    elif quality_score >= 50:
        risk_level = "High"

    else:
        risk_level = "Very High"        

    # Cover Page
    pdf.add_page()
    pdf.set_font("Arial", "B", 24)

    pdf.ln(40)

    pdf.cell(
        0,
        15,
        "KRISH AI EXCEL REPORT",
        ln=True,
        align="C"
    )
    pdf.ln(15)

    pdf.set_font("Arial", "I", 14)

    pdf.cell(
        0,
        10,
        "Professional Data Analysis Report",
        ln=True,
        align="C"
    )

    pdf.ln(40)

    pdf.set_font("Arial", "", 12)

    pdf.cell(
        0,
        8,
        f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        ln=True,
        align="C"
    )

    pdf.cell(
        0,
        8,
        "Prepared By: AI Excel Report Agent",
        ln=True,
        align="C"
    )

    pdf.cell(
        0,
        8,
        "Version: V3.0",
        ln=True,
        align="C"
    )

    pdf.cell(
        0,
        8,
        "Powered By: Gemini AI",
        ln=True,
        align="C"
    )

    pdf.ln(20)

    pdf.set_font("Arial", "I", 12)

    pdf.cell(
        0,
        10,
        "Investment Data Intelligence Report",
        ln=True,
        align="C"
    )

    pdf.add_page()

    pdf.set_font("Arial", "B", 16)

    pdf.cell(
        0,
        10,
        "EXECUTIVE SUMMARY",
        ln=True
    )

    pdf.ln(5)

    pdf.set_font("Arial", "", 11)

    summary_text = (
        f"This dataset contains {rows} records and {columns} columns.\n\n"
        f"The dataset is {round(completeness,2)}% complete.\n\n"
        f"Data quality score is {quality_score}/100.\n\n"
        f"The average investment amount is Rs.{average_investment:,.2f}.\n\n"
        f"Immediate action is recommended to improve overall data quality."
    )
    
    pdf.multi_cell(
        0,
        8,
        summary_text
    )

    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)

    pdf.add_page()

    # KPI Dashboard

    pdf.cell(
        0,
        8,
        "====================================",
        ln=True,
        align="C"
    )

    pdf.ln(3)

    pdf.set_font("Arial", "B", 16)

    pdf.cell(
        0,
        10,
        "KPI DASHBOARD",
        ln=True,
        align="C"
    )

    pdf.ln(5)

    pdf.cell(
        0,
        8,
        "-" * 50,
        ln=True,
        align="C"
    )

    pdf.ln(3)

    pdf.set_font("Arial", "", 12)

    pdf.cell(
        0,
        10,
        f"Total Records        : {rows}",
        ln=True,
        align="C"
    )

    pdf.cell(
        0,
        10,
        f"Missing Values      : {missing_values}",
        ln=True,
        align="C"
    )

    pdf.cell(
        0,
        10,
        f"Duplicate Rows      : {duplicate_rows}",
        ln=True,
        align="C"
    )

    pdf.cell(
        0,
        10,
        f"Data Completeness   : {round(completeness,2)}%",
        ln=True,
        align="C"
    )

    pdf.cell(
        0,
        10,
        f"Quality Score       : {quality_score}/100",
        ln=True,
        align="C"
    )

    pdf.cell(
        0,
        10,
        f"Dataset Health      : {health_status}",
        ln=True,
        align="C"
    )

    pdf.cell(
        0,
        10,
        f"Risk Level : {risk_level}",
        ln=True,
        align="C"
    )

    pdf.ln(5)

    pdf.set_font("Arial", "B", 14)

    pdf.cell(
        0,
        8,
        "Executive Assessment",
        ln=True
    )

    pdf.ln(3)

    pdf.set_font("Arial", "", 11)

    pdf.multi_cell(
        0,
        8,
        f"""
    The dataset currently contains {duplicate_rows} duplicate records.

    Data completeness is {round(completeness,2)}%.

    Overall health status is {health_status} with a {risk_level} risk profile.

    Management attention is recommended before using this dataset for strategic decision-making.
    """
    )

    pdf.ln(10)

    pdf.add_page()

    # Dataset Summary

    pdf.set_font("Arial", "B", 14)

    pdf.cell(
        0,
        8,
        "Dataset Summary",
        ln=True
    )

    pdf.ln(2)

    pdf.set_font("Arial", "", 11)
    pdf.cell(
        0,
        8,
        f"Total Records: {rows}",
        ln=True
    )

    pdf.cell(
        0,
        8,
        f"Total Columns: {columns}",
        ln=True
    )

    pdf.cell(
        0,
        8,
        f"Average Investment: {round(average_investment, 2)}",
        ln=True
    )

    pdf.cell(
        0,
        8,
        f"Highest Investment: {round(highest_investment, 2)}",
        ln=True
    )

    pdf.cell(
        0,
        8,
        f"Lowest Investment: {round(lowest_investment, 2)}",
        ln=True
    )

    pdf.ln(5)
    
    pdf.ln(2)

    pdf.set_font("Arial", "", 11)

    pdf.cell(
        0,
        8,
        f"Rows: {rows}",
        ln=True
    )

    pdf.cell(
        0,
        8,
        f"Columns: {columns}",
        ln=True
    )

    pdf.cell(
        0,
        8,
        f"Missing Values: {missing_values}",
        ln=True
    )

    pdf.ln(3)

    # Data Quality Report
    
    pdf.set_font("Arial", "B", 14)

    pdf.add_page()

    pdf.cell(
        0,
        8,
        "Data Quality Report",
        ln=True
    )
    pdf.ln(2)

    pdf.set_font("Arial", "", 11)

    if quality_score < 0:
        quality_score = 0

    pdf.cell(
        0,
        8,
        f"Duplicate Rows: {duplicate_rows}",
        ln=True
    )

    pdf.ln(5)

    pdf.cell(
        0,
        8,
        f"Data Completeness: {round(completeness, 2)}%",
        ln=True
    )

    pdf.ln(5)

    pdf.cell(
        0,
        8,
        f"Quality Score : {round(quality_score,2)}/100",
        ln=True
    )

    pdf.ln(5)

    # Dataset Health Status
    pdf.cell(
        0,
        10,
        f"Risk Level          : {risk_level}",
        ln=True
    )

    pdf.cell(
        0,
        8,
        f"Dataset Health: {health_status}",
        ln=True
    )
    pdf.ln(5)

    # Column Names
    pdf.set_font("Arial", "B", 12)

    pdf.cell(
        0,
        8,
        "Column Names:",
        ln=True
    )

    pdf.set_font("Arial", "", 11)

    for column in column_names:
        pdf.cell(
            0,
            8,
            f"- {column}",
            ln=True
        )

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)

    pdf.cell(
        0,
        8,
        "Dataset Statistics",
        ln=True
    )

    pdf.ln(5)

    pdf.set_font("Arial", "", 11)

    pdf.ln(3)

    pdf.set_font("Arial", "", 11)

    for column, values in statistics.items():

        pdf.cell(
            0,
            8,
            f"{column}",
            ln=True
        )

        pdf.cell(
            0,
            8,
            f"Mean: {round(values['mean'], 2)}",
            ln=True
        )

        pdf.cell(
            0,
            8,
            f"Min: {round(values['min'], 2)}",
            ln=True
        )

        pdf.cell(
            0,
            8,
            f"Max: {round(values['max'], 2)}",
            ln=True
        )

    pdf.ln(2)

    pdf.ln(5)

    pdf.add_page()

    pdf.set_font("Arial", "B", 16)

    pdf.cell(
        0,
        10,
        "KEY FINDINGS",
        ln=True
    )

    pdf.ln(5)

    pdf.set_font("Arial", "", 11)

    pdf.multi_cell(
        0,
        8,
        f"""
    1. Dataset contains {rows} records.

    2. Data completeness is {round(completeness,2)}%.

    3. Duplicate records found: {duplicate_rows}.

    4. Average investment amount is Rs.{average_investment:,.2f}.

    5. Dataset health status is {health_status}.
    """
    )

    pdf.ln(5)

    pdf.set_font("Arial", "B", 14)

    pdf.cell(
        0,
        8,
        "Business Impact",
        ln=True
    )

    pdf.ln(3)

    pdf.set_font("Arial", "", 11)

    pdf.multi_cell(
        0,
        8,
        f"""
    1. The presence of {duplicate_rows} duplicate records can affect reporting accuracy.

    2. Improving data quality can increase confidence in business decisions.

    3. The current quality score of {round(quality_score, 2)}/100 suggests immediate attention is required.
    4. The average investment amount of Rs.{average_investment:,.2f} indicates significant financial activity that requires accurate data for analysis.
    """
    )

    pdf.ln(5)

    pdf.cell(
        0,
        8,
        "=" * 40,
        ln=True,
        align="C"
    )
    

    # Chart Visualization
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)

    pdf.cell(
        0,
        8,
        "Chart Visualization",
        ln=True
    )

    pdf.ln(3)

    pdf.image(
        "chart.png",
        x=10,
        w=180
    )

    pdf.set_font("Arial", "B", 14)

    pdf.add_page()

    pdf.cell(
        0,
        8,
        "Additional Visualizations",
        ln=True
    )

    pdf.ln(5)

    pdf.image(
        "barchart.png",
        x=10,
        w=180
    )

    pdf.ln(10)

    pdf.image(
        "piechart.png",
        x=10,
        w=150
    )

    pdf.ln(10)
    pdf.set_x(10)

    pdf.ln(5)

    pdf.add_page()

    # AI Recommendations
    pdf.set_font("Arial", "B", 14)

    pdf.cell(
        0,
        8,
        "AI Recommendations",
        ln=True
    )

    pdf.ln(3)

    pdf.set_font("Arial", "", 11)

    recommendations = []

    if duplicate_rows > 0:
        recommendations.append(
            f"HIGH PRIORITY: Remove {duplicate_rows} duplicate records to improve reporting accuracy and decision-making reliability."
    )

    if quality_score < 50:
        recommendations.append(
            "HIGH PRIORITY: Perform data cleansing and validation to improve overall dataset quality."
    )

    if average_investment > 300000:
        recommendations.append(
            "MEDIUM PRIORITY: Analyze top-performing investment categories and optimize portfolio allocation."
    )

    if completeness >= 95:
        recommendations.append(
            "POSITIVE: Dataset completeness is excellent and suitable for advanced business analysis."
    )

    if len(recommendations) == 0:
        recommendations.append(
            "No major issues detected. Continue monitoring data quality regularly."
    )
    for recommendation in recommendations:
        pdf.cell(
            0,
            8,
            f"- {recommendation}",
            ln=True
        )

    pdf.ln(5)

    pdf.set_font("Arial", "B", 14)

    pdf.cell(
        0,
        8,
    "AI Business Insights",
        ln=True
    )

    pdf.ln(3)

    executive_text = (
    f"The dataset contains {rows} investment records with a completeness level of {round(completeness,2)}%.\n\n"
    
    f"A total of {duplicate_rows} duplicate records were identified, which may affect reporting accuracy and business decision-making.\n\n"
    
    f"The average investment amount is Rs.{average_investment:,.2f}, indicating the overall scale of investment activity.\n\n"
    
    f"Current data quality score is {quality_score}/100 and the dataset health status is classified as {health_status}.\n\n"
    
    "Strategic Recommendation:\n"
    "Organizations should prioritize data quality improvements before relying on this dataset for critical business decisions.\n\n"
    
    "Risk Assessment:\n"
    "Current risk level is HIGH due to the large number of duplicate records.\n\n"
    
    "Expected Outcome:\n"
    "Removing duplicates and validating data quality can significantly improve reporting accuracy and decision-making confidence."
)

    pdf.set_font("Arial", "", 12)

    pdf.multi_cell(
        0,
        8,
        executive_text
    )

    pdf.ln(5)

    # Data Cleaning Audit

    pdf.add_page()

    pdf.set_font("Arial", "B", 16)

    pdf.cell(
        0,
        10,
        "Data Cleaning Audit",
        ln=True
    )

    pdf.ln(5)

    pdf.set_font("Arial", "", 12)

    pdf.cell(
        0,
        8,
        f"Duplicates Found: {duplicates_found}",
        ln=True
    )

    pdf.cell(
        0,
        8,
        f"Duplicates Removed: {duplicates_removed}",
        ln=True
    )

    pdf.cell(
        0,
        8,
        f"Missing Values Found: {missing_before}",
        ln=True
    )

    pdf.cell(
        0,
        8,
        f"Missing Values Fixed: {missing_fixed}",
        ln=True
    )

    pdf.cell(
        0,
        8,
        f"Remaining Missing Values: {missing_after}",
        ln=True
    )

    pdf.ln(5)

    pdf.multi_cell(
        0,
        8,
        "Dataset was automatically cleaned by removing duplicate records and fixing missing values."
    )

    pdf.output("AI_Report.pdf")

    return "AI_Report.pdf"