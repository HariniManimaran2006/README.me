"""
Main Streamlit application for Contract Auditor.
"""
import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path

# Import utility modules
from utils.text_extraction import extract_text_from_file
from utils.clause_extraction import extract_clauses, extract_definitions
from utils.ner import ContractNER
from utils.risk_detection import RiskDetectionEngine
from utils.contract_classifier import ContractClassifier
from utils.clause_explainer import ClauseExplainer

# Safe import for PDF report (may fail if numpy unavailable)
try:
    from utils.pdf_report import PDFReportGenerator
    PDF_AVAILABLE = True
except Exception as e:
    PDF_AVAILABLE = False
    st.warning(f"PDF export unavailable: {str(e)}")


def initialize_session_state():
    """Initialize session state variables."""
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    if "raw_text" not in st.session_state:
        st.session_state.raw_text = ""
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = {}


def save_audit_log(filename: str, analysis_results: dict):
    """Save analysis results to audit log."""
    os.makedirs("audit_logs", exist_ok=True)
    
    audit_entry = {
        "filename": filename,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "contract_type": analysis_results.get("contract_type", {}),
        "risk_score": analysis_results.get("risk_score", 0),
        "risk_category": analysis_results.get("risk_category", ""),
        "entities_count": len(analysis_results.get("entities", {})),
        "clauses_count": len(analysis_results.get("clauses", [])),
        "risks_count": len(analysis_results.get("risks", []))
    }
    
    # Create safe filename
    safe_name = Path(filename).stem.replace(" ", "_")
    log_path = f"audit_logs/{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(audit_entry, f, indent=2, ensure_ascii=False)
    
    return log_path


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Contract Auditor",
        page_icon="📋",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("📋 Contract Auditor")
    st.markdown("*AI-powered contract analysis and risk detection*")
    
    # Sidebar
    with st.sidebar:
        st.header("Options")
        action = st.radio(
            "Select action:",
            ["Upload & Analyze", "View Audit Logs", "About"]
        )
    
    # Main content
    if action == "Upload & Analyze":
        st.header("Upload Contract for Analysis")
        
        uploaded_file = st.file_uploader(
            "Upload a contract file (PDF, DOCX, TXT)",
            type=["pdf", "docx", "txt"],
            help="Supported formats: PDF, DOCX, TXT"
        )
        
        if uploaded_file:
            st.session_state.uploaded_file = uploaded_file
            
            with st.spinner("Extracting text..."):
                st.session_state.raw_text = extract_text_from_file(uploaded_file)
            
            # Tabs for different views
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "Raw Text",
                "Clauses & Definitions",
                "Entities",
                "Risk Analysis",
                "Classification",
                "Summary & Download"
            ])
            
            # TAB 1: Raw Extracted Text
            with tab1:
                st.subheader("Extracted Raw Text")
                st.text_area(
                    "Content:",
                    value=st.session_state.raw_text,
                    height=400,
                    disabled=True
                )
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copy to Clipboard"):
                        st.write("Text copied (use browser copy)")
                with col2:
                    st.download_button(
                        "⬇️ Download Raw Text",
                        data=st.session_state.raw_text,
                        file_name=f"{uploaded_file.name}_extracted.txt",
                        mime="text/plain"
                    )
            
            # TAB 2: Clauses & Definitions
            with tab2:
                st.subheader("Extracted Clauses & Definitions")
                
                with st.spinner("Extracting clauses..."):
                    clauses = extract_clauses(st.session_state.raw_text)
                    definitions = extract_definitions(st.session_state.raw_text)
                
                # Store in results
                st.session_state.analysis_results["clauses"] = clauses
                st.session_state.analysis_results["definitions"] = definitions
                
                # Display clauses
                st.write(f"**Found {len(clauses)} clauses**")
                
                for clause in clauses:
                    with st.expander(f"Clause {clause['number']}: {clause['heading']}"):
                        st.write(clause["full_content"][:500])
                        if clause["subclauses"]:
                            st.write("**Sub-clauses:**")
                            for sub in clause["subclauses"]:
                                st.write(f"- {sub['number']}: {sub['content']}")
                
                # Display definitions
                if definitions:
                    st.write(f"\n**Definitions Found ({len(definitions)})**")
                    for term, definition in list(definitions.items())[:10]:
                        st.write(f'- **"{term}"**: {definition}')
            
            # TAB 3: Named Entity Recognition
            with tab3:
                st.subheader("Extracted Entities")
                
                with st.spinner("Extracting entities..."):
                    ner = ContractNER()
                    entities = ner.extract_entities(st.session_state.raw_text)
                
                st.session_state.analysis_results["entities"] = entities
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Parties:**")
                    if entities.get("parties"):
                        for party in entities["parties"]:
                            st.write(f"- {party}")
                    else:
                        st.write("No parties identified")
                    
                    st.write("\n**Jurisdictions:**")
                    if entities.get("jurisdictions"):
                        for jurisdiction in entities["jurisdictions"]:
                            st.write(f"- {jurisdiction}")
                    else:
                        st.write("No jurisdictions identified")
                
                with col2:
                    st.write("**Key Dates:**")
                    if entities.get("dates"):
                        for date in entities["dates"][:10]:
                            st.write(f"- {date}")
                    else:
                        st.write("No dates identified")
                    
                    st.write("\n**Monetary Amounts:**")
                    if entities.get("amounts"):
                        for amount, atype in entities["amounts"][:10]:
                            st.write(f"- {amount} ({atype})")
                    else:
                        st.write("No amounts identified")
            
            # TAB 4: Risk Analysis
            with tab4:
                st.subheader("Risk Detection & Analysis")
                
                with st.spinner("Analyzing risks..."):
                    risk_engine = RiskDetectionEngine()
                    risks = risk_engine.detect_risks(st.session_state.raw_text)
                    score, category = risk_engine.calculate_risk_score(risks)
                
                st.session_state.analysis_results["risks"] = risks
                st.session_state.analysis_results["risk_score"] = score
                st.session_state.analysis_results["risk_category"] = category
                
                # Display risk score
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Overall Risk Score", f"{score}/100", delta=None)
                with col2:
                    st.metric("Risk Category", category)
                with col3:
                    st.metric("Risks Identified", len(risks))
                
                # Risk gauge
                st.progress(score / 100, text=f"{score}% Risk Level")
                
                # High-risk clauses
                st.write("\n**Identified Risks:**")
                high_risks = [r for r in risks if r["risk_level"] == "high"]
                medium_risks = [r for r in risks if r["risk_level"] == "medium"]
                
                if high_risks:
                    st.error(f"🔴 **HIGH RISK ({len(high_risks)})**")
                    for risk in high_risks[:5]:
                        with st.expander(risk["type"]):
                            st.write(f"**Description:** {risk['description']}")
                            st.write(f"**Evidence:** {risk['evidence']}")
                
                if medium_risks:
                    st.warning(f"🟡 **MEDIUM RISK ({len(medium_risks)})**")
                    for risk in medium_risks[:5]:
                        with st.expander(risk["type"]):
                            st.write(f"**Description:** {risk['description']}")
                            st.write(f"**Evidence:** {risk['evidence']}")
            
            # TAB 5: Contract Classification
            with tab5:
                st.subheader("Contract Type Classification")
                
                with st.spinner("Classifying contract..."):
                    classifier = ContractClassifier()
                    classification = classifier.classify_contract(st.session_state.raw_text)
                
                st.session_state.analysis_results["contract_type"] = classification
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Primary Type", classification["primary_type"])
                with col2:
                    st.metric("Confidence", f"{classification['confidence']:.1f}%")
                
                st.write(f"**Description:** {classification['description']}")
                
                if classification["all_matches"]:
                    st.write("\n**All Matching Types:**")
                    for ctype, matches in classification["all_matches"].items():
                        st.write(f"- {ctype}: {matches} matches")
            
            # TAB 6: Summary & Download
            with tab6:
                st.subheader("Analysis Summary & Export")
                
                # Overall summary
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    risk_score = st.session_state.analysis_results.get("risk_score", 0)
                    st.metric("Risk Score", f"{risk_score}/100")
                with col2:
                    clauses = st.session_state.analysis_results.get("clauses", [])
                    st.metric("Clauses Found", len(clauses))
                with col3:
                    entities = st.session_state.analysis_results.get("entities", {})
                    party_count = len(entities.get("parties", []))
                    st.metric("Parties", party_count)
                with col4:
                    contract_type = st.session_state.analysis_results.get("contract_type", {}).get("primary_type", "?")
                    st.metric("Type", contract_type)
                
                # Save audit log
                st.write("\n**Save Analysis**")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("💾 Save to Audit Log"):
                        st.session_state.analysis_results["filename"] = uploaded_file.name
                        log_path = save_audit_log(uploaded_file.name, st.session_state.analysis_results)
                        st.success(f"Saved to {log_path}")
                
                # Generate PDF report
                with col2:
                    if PDF_AVAILABLE and st.button("📄 Generate PDF Report"):
                        pdf_generator = PDFReportGenerator()
                        st.session_state.analysis_results["filename"] = uploaded_file.name
                        pdf_bytes = pdf_generator.generate_report(st.session_state.analysis_results)
                        st.download_button(
                            "⬇️ Download PDF Report",
                            data=pdf_bytes,
                            file_name=f"{uploaded_file.name}_report.pdf",
                            mime="application/pdf"
                        )
                    elif not PDF_AVAILABLE:
                        st.info("📄 PDF export not available in this environment")
    
    elif action == "View Audit Logs":
        st.header("Audit Logs")
        
        audit_dir = Path("audit_logs")
        if audit_dir.exists():
            log_files = list(audit_dir.glob("*.json"))
            
            if log_files:
                st.write(f"Found {len(log_files)} audit log entries")
                
                for log_file in sorted(log_files, reverse=True)[:20]:
                    with open(log_file, "r") as f:
                        log_data = json.load(f)
                    
                    with st.expander(f"{log_data['filename']} - {log_data['timestamp']}"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**Risk Score:** {log_data['risk_score']}")
                        with col2:
                            st.write(f"**Clauses:** {log_data['clauses_count']}")
                        with col3:
                            st.write(f"**Risks:** {log_data['risks_count']}")
            else:
                st.info("No audit logs found yet")
        else:
            st.info("No audit logs directory found")
    
    else:  # About
        st.header("About Contract Auditor")
        st.markdown("""
        **Contract Auditor** is an AI-powered tool for analyzing contracts and identifying risks.
        
        ### Features:
        - 📄 **File Upload**: Support for PDF, DOCX, and TXT formats
        - 📋 **Text Extraction**: Automatic text extraction from documents
        - 🔤 **Clause Extraction**: Identify and structure contract clauses
        - 👥 **Entity Recognition**: Extract parties, dates, amounts, jurisdictions
        - ⚠️ **Risk Detection**: Identify high-risk clauses and terms
        - 📊 **Risk Scoring**: Generate overall contract risk score
        - 📑 **Classification**: Detect contract type (Employment, Lease, etc.)
        - 📄 **PDF Export**: Download analysis report as PDF
        - 📝 **Audit Logs**: Track all analyses performed
        
        ### Disclaimer:
        This tool provides informational analysis only. Always consult with legal counsel before signing any contract.
        """)


if __name__ == "__main__":
    main()
