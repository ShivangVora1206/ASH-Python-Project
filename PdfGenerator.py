from tkinter.filedialog import asksaveasfilename
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image

class PdfGen:
    def __init__(self, db_ref):
        self.db_ref = db_ref
    
    def generate_pdf(self, selected_game_mode):
        result = self.db_ref.evaluate_result(selected_game_mode)
        if not result:
            return

        # Open a file dialog to choose the location and filename for the PDF
        pdf_filename = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_filename:
            return  # User cancelled the file dialog

        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        custom_style = ParagraphStyle(
            name='CustomStyle',
            parent=styles['Normal'],
            fontSize=18,
            leading=22,
            alignment=1,  # Center alignment
            fontName='Helvetica-Bold'
        )
        custom_style_1 = ParagraphStyle(
            name='CustomStyle1',
            parent=styles['Normal'],
            fontSize=12,
            leading=22,
            alignment=1,  # Center alignment
            fontName='Helvetica-Bold'
        )

        
        logo_path = "logo.png"  # Path to the logo image
        elements.append(Image(logo_path, width=472, height=92))
        elements.append(Paragraph(f"Test Scores and User Level Estimation", custom_style))
        # Add the table with column titles and data
        data = [["German", "English", "Level", "Answered","Score"]]
        for card in result['cards']:
            data.append([card['German'], card['English'], card['level'],'Y' if card['flag'] else 'N', card['score']])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)

        elements.append(Paragraph("<br/><br/>", styles['Normal']))
        
        for level, score in result['scores'].items():
            elements.append(Paragraph(f"Total Score for {level}: {score}", custom_style_1))
        elements.append(Paragraph("<br/><br/>", styles['Normal']))  # Add some space before the next page
        elements.append(Paragraph(f"Total Normalized Score: {result['total_score']}", custom_style))
        elements.append(Paragraph(f"Predicted Level: {result['predicted_level']}", custom_style))


        doc.build(elements)
        print(f"PDF generated: {pdf_filename}")
