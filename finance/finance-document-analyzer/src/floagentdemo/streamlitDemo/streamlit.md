# Financial Transaction Analyzer - CrewAI

## Overview
The **Financial Transaction Analyzer** is an advanced tool designed to Extract transactions, categorize transactions, analyze trends, cash flow analysis and generate report that summarizes, shows interactive charts and categorized transactions information on streamlit dashboard. It also provides ability to download categorized transactions as CSV/Excel and generate report with summary, analysis and charts as pdf.

### **Key Features**
- **PDF Upload:** Seamlessly upload Bank or Credit card statements in PDF format for analysis.  
- **Automated Data Extraction:** Efficiently extracts transaction details, identifying trends, category based analysis, and key financial metrics.  
- **Insightful Reports:** Provides comprehensive insights into financial transactions, including visualizations and summary statistics.  
- **Downloadable Reports:** Export transaction data as **CSV** and download the complete analysis report as a **PDF** for further use or record-keeping.

---

## Prerequisites
Ensure the following software is installed in the deployment environment:

- **Python:** Version 3.9 or above  
- **uv** using as package manager for the environment

*Note:* If using a virtual environment, ensure it is compatible with Python 3.9+.

---

## Libraries & Dependencies
This project relies on the following Python libraries:  

- **Streamlit:** For building the interactive web interface.  
- **fpdf2:** For generating PDF reports.  
- **Plotly:** For creating advanced data visualizations.  
- **Kaleido:** For exporting Plotly figures as static images.  
- **PyPDF2:** For handling PDF file processing.  
- **Pandas:** For data manipulation and analysis.  

---

## Installation Steps

### 1. Clone the Repository
```bash
git clone <repository_url>
cd <root_folder>
```
### 2. Set Up a Virtual Environment
Command to create virtual environment in macOS:
```bash
 uv venv .venv
```
If uv is not installed, install it using:
```bash
pip install uv
```
### 3. Activate the Virtual Environment
```bash
source .venv/bin/activate
```
You’ll enter the virtual environment after running this command.

### 4. Install Required Dependencies in the virtual environment
```bash
uv pip install -r pyproject.toml  
```
Ensure all necessary libraries are installed before proceeding.

### 5. Running the Application
Start the application using the following command:
```bash
python -m streamlit run src/floagentdemo/streamlitDemo/app.py
```
The application will launch in your default web browser.