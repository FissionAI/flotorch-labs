from fpdf import FPDF
import io
import pandas as pd
import plotly.io as pio
import os

class PDF(FPDF):
    def header(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        streamlit_demo_dir = os.path.abspath(os.path.join(script_dir, ".."))
        logo_path = os.path.join(streamlit_demo_dir, "flo_torch_logo.png")
        w=30
        margin = 5
        self.image(logo_path, x=210 - w - margin, y=margin, w=w)
        self.ln(10)

    def footer(self):
        pass
    def chapter_title(self, title, font_color, fill_color):
        self.set_fill_color(*fill_color)
        self.set_text_color(*font_color)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=True, align='L')

    def chapter_body(self, body, font_color, fill_color):
        margin = 10
        padding = 2
        line_height = 6
        self.set_fill_color(*fill_color)
        self.set_text_color(*font_color)
        self.set_font('Arial', '', 10)
        w = 210 - 2 * margin
        words = body.split(' ')
        current_line = ''
        num_lines = 0
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if self.get_string_width(test_line) <= w - 2 * padding:
                current_line = test_line
            else:
                num_lines += 1
                current_line = word
        num_lines += 1
        text_height = num_lines * line_height
        if self.get_y() + text_height + 2 * padding + 10 > 297 - margin:
            self.add_page()
        x, y = margin, self.get_y()
        self.rect(x, y, w, text_height + 2 * padding, 'F')
        self.set_xy(x + padding, y + padding)
        self.multi_cell(w - 2 * padding, line_height, body, align='L', border=0)

# Function to get image buffer
def get_image_buffer(image):
    img_buffer = io.BytesIO()
    pio.write_image(image, img_buffer, format="png")
    img_buffer.seek(0)
    return img_buffer

def insert_spending_table(pdf, data):
    # Set font for the table
    pdf.set_font("Arial", "B", size=10)
    margin = 10
    col_widths = [(210 - (2 * margin)) / len(data.columns)] * len(data.columns)
    line_height = 8
    pdf.set_x(margin)
    pdf.set_fill_color(56, 45, 76)
    pdf.set_text_color(228, 231, 245)
    headers = data.columns.tolist()
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], line_height, header.capitalize(), border=1, align='C', fill=True)
    pdf.ln()
    pdf.set_font("Arial", size=10)
    for index, row in data.iterrows():
        pdf.set_x(10)
        if index % 2 != 0:
            fill_color = (245, 245, 245)
            text_color = (114, 114, 114)
        else:
            fill_color = (255, 255, 255)
            text_color = (148, 148, 148)

        pdf.set_fill_color(*fill_color)
        pdf.set_text_color(*text_color)
        
        for i, value in enumerate(row):
            pdf.cell(col_widths[i], line_height, str(value), border=1, fill=True)
        pdf.ln()
    pdf.set_text_color(0, 0, 0)

def add_text_based_output(pdf, insights, font_color, fill_color, insight_name):
    gap_between_ponts = 5
    try:
        for insight in insights:
            for value in insight.values():
                pdf.chapter_body(value, font_color=font_color, fill_color=fill_color)
                pdf.ln(gap_between_ponts)
    except Exception as e:
        pdf.chapter_body(f"Unable to fetch {insight_name}", font_color=font_color, fill_color=fill_color)
        pdf.ln(gap_between_ponts)

# Create PDF function
def generate_pdf(data, chart_info):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Financial Transaction Analysis", ln=True, align="C", border=0)
    pdf.ln(10)
    
    # Summary and Monthly Spending Charts
    summary_chart = chart_info.get("summary_statistics")
    monthly_chart = chart_info.get("monthly_spending")
    
    if summary_chart or monthly_chart:
        if summary_chart and monthly_chart:
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(90, 10, "Summary Statistics", ln=False, align='C')
            pdf.cell(90, 10, "Monthly Spending", ln=True, align='C')
            pdf.image(get_image_buffer(summary_chart), x=10, y=pdf.get_y(), w=90)
            pdf.image(get_image_buffer(monthly_chart), x=110, y=pdf.get_y(), w=90)
            pdf.set_draw_color(229, 233, 235)
            pdf.rect(10, pdf.get_y(), 90, 60)
            pdf.rect(110, pdf.get_y(), 90, 60)
        else:
            single_chart = summary_chart if summary_chart else monthly_chart
            pdf.set_font("Arial", 'B', 12)
            title = "Summary Statistics" if summary_chart else "Monthly Spending"
            pdf.cell(200, 10, title, ln=True, align='C')
            pdf.image(get_image_buffer(single_chart), x=10, y=pdf.get_y(), w=190)
            pdf.set_draw_color(229, 233, 235)
            pdf.rect(10, pdf.get_y(), 190, 60)
        pdf.ln(70)
    # Other charts full width
    for key in ["spending_distribution", "top_spending_categories"]:
        if data.get(key):
            pdf.set_font("Arial", 'B', 12)
            pdf.set_x(10)
            pdf.cell(200, 10, txt=f"{key.replace('_', ' ').title()}", ln=True)
            tableData = pd.DataFrame(data[key])
            insert_spending_table(pdf, tableData)
            pdf.ln(10)

    
    # Insights, Recommendations, and Unusual Spending Patterns
    sections = {
        "insights": ((0, 0, 0), (231, 243, 254)),
        "recommendations": ((0, 0, 0), (212, 237, 218)),
        "unusual_spending_patterns": ((0, 0, 0), (255, 243, 205))
    }
    
    for section, (font_color, fill_color) in sections.items():
        section_title = section.replace('_', ' ').title()
        # pdf.chapter_title(section.replace('_', ' ').title(), font_color, fill_color)
        pdf.chapter_title(section_title, font_color, fill_color)
        pdf.ln(1)
        try:
            add_text_based_output(pdf, data.get(section, []), font_color, fill_color, section_title)
        except Exception as e:
            pdf.chapter_body(f"Unable to fetch {section.replace('_', ' ')}", font_color, fill_color)
    
    pdf_stream = io.BytesIO()
    pdf.output(pdf_stream)
    pdf_stream.seek(0)
    return pdf_stream
