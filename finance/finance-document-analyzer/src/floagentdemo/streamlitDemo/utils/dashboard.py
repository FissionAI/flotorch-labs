import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.io as pio
from utils.generatePdf import generate_pdf
from utils.transform import transform_data

def apply_styles_for_table(): 
  # Apply Custom CSS
  st.markdown("""
      <style>
          .scrollable-table-container {
              min-height: 400px;
              max-height: 400px;
              overflow-y: auto;
          }
          .stDownloadButton {
            text-align: right;
          }
          .description-box {
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
            margin-bottom: 16px;
          }
          .warning-alert {
            background-color: #fff3cd;
            color: #856404;  
          }
          .scroll-box {
            min-height: 416px;
            max-height: 416px;
            overflow-y: auto;
          }
          .recommendation-alert {
            background-color: #d4edda;
            color: #155724;
          }
          .insight-alert {
            background-color: #e7f3fe;
            color: #0c5460 !important;
          }
          table {
              width: 100%;
              border-collapse: collapse;
          }
          th {
              background-color: rgb(56, 45, 76) !important;
              color: rgb(228, 231, 245) !important;
              text-align: center !important;
              padding: 8px;
              text-transform: capitalize;
          }
          td {
              padding: 8px;
              text-align: left;
          }
          tbody tr:nth-child(even) {
            background-color: rgb(245, 245, 245) !important;
            color: rgb(114, 114, 114) !important
          }
          tbody tr:nth-child(odd) {
            background-color: rgb(255, 255, 255) !important;
            color: rgb(148, 148, 148) !important
          }
      </style>
  """, unsafe_allow_html=True)

def get_html_text_group(value, className, noDataMessage):
  warnings_html = "<div class='scroll-box'>"
  if value:
    for spending in value:
      warnings_html += f"<div class='description-box {className}'>{spending.get('description')}</div>"
  else:
    warnings_html += f"<div>{noDataMessage}</div>"
  warnings_html += "</div>"
  return warnings_html

def build_dashboard(response, transactions):
  # Dynamically create columns based on data keys
  # Always show download button at top if PDF is ready
  if not st.session_state.get("pdf_buffer"):
    st.session_state.pdf_buffer = None
    # st.session_state.chart_info = None

  if st.session_state.get("pdf_buffer"):
      st.download_button(
        label="📄 Download Full Report",
        data=st.session_state.pdf_buffer,
        file_name="financial_analysis_report.pdf",
        mime="application/pdf",
        key="top_download_button"
      )
  data = transform_data(response)
  keys = list(data.keys())
  num_columns = min(2, len(keys))  # Ensure a maximum of 2 columns dynamically
  columns = st.columns(num_columns, gap="large")  # Dynamic columns with large gap
  chart_info = {key: None for key in keys}
  try:
    for i, key in enumerate(keys):
      if not data.get(key):
        continue
      col = columns[i % num_columns]
      with col:
        with st.container(border=True):
          if key != 'spending_distribution':
            st.subheader(key.replace('_', ' ').title())
          else:
            sub_column_one, sub_column_two = st.columns([3, 2])  # Adjust the ratio if needed
            with sub_column_one:
              st.subheader(key.replace('_', ' ').title())
            with sub_column_two:
              download_csv_for_transactions(transactions)  # Button aligned to the right
          if key == "summary_statistics":
              summary_data = pd.DataFrame.from_dict(data[key], orient='index', columns=["Amount"])
              summary_data.reset_index(inplace=True)
              summary_data.rename(columns={"index": "Metric", "Amount": "amount"}, inplace=True)
              summary_data['Metric'] = summary_data['Metric'].apply(lambda x: ' '.join([word.capitalize() for word in x.split('_')]))
              summary_chart = px.pie(summary_data, names="Metric", values="amount", color_discrete_sequence=px.colors.qualitative.Set2)
              summary_chart.update_layout(height=400)
              st.plotly_chart(summary_chart, use_container_width=True, config={"displayModeBar": False})
              chart_info[key] = summary_chart

          elif key == "monthly_spending":
            monthly_trends = go.Figure()
            if data[key]:
              monthly_data = pd.DataFrame(data[key])
              monthly_trends.add_trace(go.Scatter(x=monthly_data['month'], y=monthly_data['income'], mode='lines+markers', name='Income', line=dict(color='blue')))
              monthly_trends.add_trace(go.Scatter(x=monthly_data['month'], y=monthly_data['expenses'], mode='lines+markers', name='Expenses', line=dict(color='red')))
              monthly_trends.update_layout(height=400)
              st.plotly_chart(monthly_trends, use_container_width=True, config={"displayModeBar": False})
              chart_info[key] = monthly_trends

          elif key == "spending_distribution":
            if data[key]:
              spending_data = pd.DataFrame(data[key])
              spending_data_reset = spending_data.reset_index(drop=True)
              # colorScale = [[0, "black"], [0.5, "white"], [1, "#f2f2f2"]]
              table_html = spending_data_reset.to_html(index=False, escape=False)
              apply_styles_for_table();
              st.markdown(f'<div class="scrollable-table-container">{table_html}</div>', unsafe_allow_html=True)
          elif key == "top_spending_categories":
            if data[key]:
              topSpending_data = pd.DataFrame(data[key])
              top_spending_data_reset = topSpending_data.reset_index(drop=True)
              # colorScale = [[0, "black"], [0.5, "white"], [1, "#f2f2f2"]]
              top_spending_table_html = top_spending_data_reset.to_html(index=False, escape=False)
              apply_styles_for_table();
              st.markdown(f'<div class="scrollable-table-container">{top_spending_table_html}</div>', unsafe_allow_html=True)
          elif key == 'unusual_spending_patterns':
            warning_box = st.empty()
            warning_html = get_html_text_group(data[key], "warning-alert", "No unusual spending")
            warning_box.markdown(warning_html, unsafe_allow_html=True)
          elif key == 'insights':
            insights_box = st.empty()
            inSights_html = get_html_text_group(data[key], "insight-alert", 'No insights')
            insights_box.markdown(inSights_html, unsafe_allow_html=True)
          elif key == 'recommendations':
            recommendation_box = st.empty()
            recommendation_html = get_html_text_group(data[key], "recommendation-alert", 'No Recommendations')
            recommendation_box.markdown(recommendation_html, unsafe_allow_html=True)

    if not st.session_state.get('pdf_buffer') and chart_info:
      st.session_state.pdf_buffer = generate_pdf(data, chart_info)
      st.rerun()  # Force streamlit to re-render which shows the button at the Top
  finally:
    st.session_state["processing_file"] = False

      
  
def download_csv_for_transactions(transactions):
   transactions_list = pd.DataFrame(transactions)
   csv_data = transactions_list.to_csv(index=False)
   st.download_button(
    label="Download transactions",
    data=csv_data,
    file_name="transactions.csv",
    mime="text/csv"
)