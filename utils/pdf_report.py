"""
PDF report generation for contract analysis results.
"""
from typing import Dict, List
from datetime import datetime


class PDFReportGenerator:
    """Generates PDF reports of contract analysis."""
    
    def __init__(self):
        """Initialize PDF report generator."""
        self.report_data = {}
    
    def generate_report(self, analysis_results: Dict) -> bytes:
        """
        Generate PDF report from analysis results.
        
        Args:
            analysis_results: Dictionary containing all analysis data
            
        Returns:
            PDF file as bytes
        """
        try:
            from fpdf import FPDF
            
            pdf = FPDF()
            pdf.add_page()
            
            # Title
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "CONTRACT ANALYSIS REPORT", ln=True, align="C")
            pdf.ln(5)
            
            # Metadata
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
            pdf.cell(0, 8, f"Contract: {analysis_results.get('filename', 'Unknown')}", ln=True)
            pdf.ln(5)
            
            # Contract Type Section
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "1. Contract Type", ln=True)
            pdf.set_font("Arial", "", 10)
            type_info = analysis_results.get("contract_type", {})
            pdf.cell(0, 8, f"Type: {type_info.get('primary_type', 'Unknown')}", ln=True)
            pdf.cell(0, 8, f"Confidence: {type_info.get('confidence', 0):.1f}%", ln=True)
            pdf.ln(3)
            
            # Extracted Entities Section
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "2. Extracted Entities", ln=True)
            pdf.set_font("Arial", "", 9)
            
            entities = analysis_results.get("entities", {})
            if entities.get("parties"):
                pdf.cell(0, 8, f"Parties: {', '.join(entities['parties'][:3])}", ln=True)
            if entities.get("jurisdictions"):
                pdf.cell(0, 8, f"Jurisdictions: {', '.join(entities['jurisdictions'][:3])}", ln=True)
            if entities.get("dates"):
                pdf.cell(0, 8, f"Key Dates: {', '.join(entities['dates'][:2])}", ln=True)
            pdf.ln(3)
            
            # Risk Analysis Section
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "3. Risk Analysis", ln=True)
            pdf.set_font("Arial", "", 10)
            
            risk_score = analysis_results.get("risk_score", 0)
            risk_category = analysis_results.get("risk_category", "Unknown")
            pdf.cell(0, 8, f"Overall Risk Score: {risk_score}/100", ln=True)
            pdf.cell(0, 8, f"Risk Category: {risk_category}", ln=True)
            pdf.ln(3)
            
            # Key Risks
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 8, "Key Risks Identified:", ln=True)
            pdf.set_font("Arial", "", 9)
            risks = analysis_results.get("risks", [])
            for risk in risks[:5]:
                pdf.cell(0, 6, f"- {risk.get('type', 'Unknown')}: {risk.get('risk_level', 'N/A').upper()}", ln=True)
            
            pdf.ln(3)
            
            # Clauses Section
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "4. Extracted Clauses", ln=True)
            pdf.set_font("Arial", "", 9)
            clauses = analysis_results.get("clauses", [])
            for clause in clauses[:3]:
                pdf.cell(0, 6, f"Clause {clause.get('number', '?')}: {clause.get('heading', 'Unknown')[:50]}", ln=True)
            
            pdf.ln(5)
            
            # Recommendations
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "5. Recommendations", ln=True)
            pdf.set_font("Arial", "", 9)
            
            if risk_score >= 70:
                pdf.cell(0, 6, "- HIGH RISK: Seek legal review before signing", ln=True)
                pdf.cell(0, 6, "- Negotiate terms to reduce identified risks", ln=True)
            elif risk_score >= 40:
                pdf.cell(0, 6, "- MEDIUM RISK: Review key clauses carefully", ln=True)
                pdf.cell(0, 6, "- Consider negotiating high-risk clauses", ln=True)
            else:
                pdf.cell(0, 6, "- LOW RISK: Standard contract terms", ln=True)
                pdf.cell(0, 6, "- Proceed with normal review process", ln=True)
            
            pdf.ln(5)
            pdf.set_font("Arial", "", 8)
            pdf.cell(0, 8, "This report is for informational purposes. Consult legal counsel for definitive advice.", ln=True)
            
            return pdf.output(dest='S').encode('latin-1')
        
        except Exception as e:
            return f"[Error generating PDF: {str(e)}]".encode()
