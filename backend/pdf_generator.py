from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from typing import Dict, List, Any
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue,
            borderWidth=1,
            borderColor=colors.lightgrey,
            borderPadding=5
        ))
        
        # Company header style
        self.styles.add(ParagraphStyle(
            name='CompanyHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
    
    def generate_pdf(self, data: Dict[str, Any], output_path: Path):
        """Generate PDF from processed data"""
        try:
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            story = []
            
            # Add company header
            story.append(Paragraph("FINANCIAL DOCUMENT PROCESSOR", self.styles['CustomTitle']))
            story.append(Paragraph("Professional Estimates & Financial Statements", self.styles['CompanyHeader']))
            story.append(Spacer(1, 20))
            
            # Add file information
            story.append(Paragraph(f"<b>Source File:</b> {data['file_name']}", self.styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Process estimates
            if data['estimates']:
                story.append(Paragraph("ESTIMATES", self.styles['SectionHeader']))
                for estimate in data['estimates']:
                    story.extend(self._create_estimate_section(estimate))
                story.append(Spacer(1, 20))
            
            # Process financial statements
            if data['financial_statements']:
                story.append(Paragraph("FINANCIAL STATEMENTS", self.styles['SectionHeader']))
                for financial in data['financial_statements']:
                    story.extend(self._create_financial_section(financial))
                story.append(Spacer(1, 20))
            
            # Add summary
            if data['summary']:
                story.extend(self._create_summary_section(data['summary']))
            
            # Build PDF
            doc.build(story)
            logger.info(f"PDF generated successfully: {output_path}")
            
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            raise
    
    def _create_estimate_section(self, estimate: Dict[str, Any]) -> List:
        """Create estimate section for PDF"""
        elements = []
        
        # Estimate title
        elements.append(Paragraph(f"<b>{estimate['title']}</b>", self.styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        # Create table for estimate items
        if estimate['items']:
            table_data = [['Description', 'Quantity', 'Unit Price', 'Total']]
            
            for item in estimate['items']:
                table_data.append([
                    item['description'],
                    f"{item['quantity']:.2f}",
                    f"${item['unit_price']:.2f}",
                    f"${item['total']:.2f}"
                ])
            
            # Add total row
            table_data.append(['', '', '<b>TOTAL:</b>', f"<b>${estimate['total']:.2f}</b>"])
            
            table = Table(table_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, -1), (-1, -1), 12),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ]))
            
            elements.append(table)
        else:
            elements.append(Paragraph("No estimate items found.", self.styles['Normal']))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _create_financial_section(self, financial: Dict[str, Any]) -> List:
        """Create financial statement section for PDF"""
        elements = []
        
        # Financial statement title
        elements.append(Paragraph(f"<b>{financial['title']}</b>", self.styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        # Process sections
        for section in financial['sections']:
            elements.append(Paragraph(f"<b>{section['name']}</b>", self.styles['Heading3']))
            
            if section['items']:
                table_data = [['Description', 'Amount']]
                
                for item in section['items']:
                    table_data.append([
                        item['description'],
                        f"${item['amount']:.2f}"
                    ])
                
                table = Table(table_data, colWidths=[4*inch, 2*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                
                elements.append(table)
            else:
                elements.append(Paragraph("No items found in this section.", self.styles['Normal']))
            
            elements.append(Spacer(1, 12))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _create_summary_section(self, summary: Dict[str, Any]) -> List:
        """Create summary section for PDF"""
        elements = []
        
        elements.append(Paragraph("SUMMARY", self.styles['SectionHeader']))
        
        summary_data = [
            ['Total Estimates', str(summary['total_estimates'])],
            ['Total Financial Statements', str(summary['total_financial_statements'])],
            ['Total Sheets Processed', str(summary['total_sheets'])],
            ['Grand Total', f"${summary['grand_total']:.2f}"]
        ]
        
        table = Table(summary_data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 14),
            ('BACKGROUND', (0, -1), (-1, -1), colors.darkblue),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
