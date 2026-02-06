# Contract Auditor

An AI-powered Streamlit application for analyzing contracts, extracting key information, detecting risks, and generating comprehensive reports.

## Features

✅ **File Upload & Text Extraction**
- Support for PDF, DOCX, and TXT formats
- Automatic text extraction and preprocessing

✅ **Clause & Sub-Clause Extraction**
- Structured clause identification and numbering
- Sub-clause detection and organization
- Automated definition extraction

✅ **Named Entity Recognition (NER)**
- Extract parties and stakeholders
- Identify dates and key timelines
- Detect monetary amounts and percentages
- Extract jurisdictions and locations
- Find contact information (email, phone, URLs)

✅ **Risk Detection & Scoring**
- Identify high-risk clauses:
  - Penalty clauses
  - Indemnity obligations
  - Termination conditions
  - Lock-in periods
  - Auto-renewal clauses
  - Arbitration clauses
  - IP assignment clauses
  - Confidentiality requirements
  - Limitation of liability
  - Non-compete clauses
- Risk level classification (Low/Medium/High)
- Overall contract risk score (0-100 scale)

✅ **Contract Classification**
- Automatic contract type detection:
  - Employment Agreement
  - Lease Agreement
  - Service Agreement
  - Vendor Agreement
  - Partnership Agreement
  - NDA/Confidentiality
  - License Agreement
  - Loan Agreement

✅ **Clause Explanation & Suggestions**
- Plain-language explanations for complex clauses
- Alternative clause suggestions for better protection
- Key points and negotiation tips

✅ **PDF Report Generation**
- Comprehensive analysis report
- Risk summary with recommendations
- Extracted entities and clauses overview
- Downloadable PDF export

✅ **Audit Logging**
- JSON logs of all analyses
- Timestamp and filename tracking
- Risk and clause count logging
- Historical analysis review

## Project Structure

```
contract-auditor/
├── app.py                              # Main Streamlit application
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
├── .gitignore                          # Git ignore rules
├── sample_contracts/                   # Sample contract files for testing
│   ├── sample_contract.txt            # Employment agreement sample
│   └── lease_agreement.txt            # Lease agreement sample
├── utils/                             # Utility modules
│   ├── __init__.py
│   ├── text_extraction.py             # PDF/DOCX/TXT extraction
│   ├── clause_extraction.py           # Clause and definition extraction
│   ├── ner.py                         # Named entity recognition
│   ├── risk_detection.py              # Risk analysis engine
│   ├── contract_classifier.py         # Contract type classification
│   ├── clause_explainer.py            # Clause explanation and suggestions
│   └── pdf_report.py                  # PDF report generation
├── templates/                         # HTML/CSS templates (future)
└── audit_logs/                        # Saved analysis logs (generated)
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Windows Setup

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\Activate.ps1
# If using Command Prompt instead:
# venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

### macOS/Linux Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Usage

### 1. Upload a Contract
- Click on "Upload Contract for Analysis" in the sidebar
- Upload a PDF, DOCX, or TXT file

### 2. Review Results
Navigate through the tabs to view:
- **Raw Text**: Extracted and formatted text
- **Clauses & Definitions**: Structured clause breakdown with sub-clauses
- **Entities**: Extracted parties, dates, amounts, jurisdictions, contacts
- **Risk Analysis**: Identified risks with severity levels
- **Classification**: Detected contract type and confidence score
- **Summary & Download**: Generate and export PDF report

### 3. Save & Export
- **Save to Audit Log**: Store analysis results as JSON
- **Generate PDF Report**: Create downloadable PDF report with analysis

### 4. View History
- Check "View Audit Logs" to see previous analyses

## Technology Stack

- **Streamlit**: Interactive web UI framework
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX file processing
- **spaCy**: NLP and entity recognition (optional enhancement)
- **fpdf2**: PDF report generation
- **Python Regex**: Pattern matching for clause and entity extraction

## Key Modules

### `text_extraction.py`
Handles multi-format file input and text extraction.

### `clause_extraction.py`
Uses regex patterns to identify and structure contract clauses and definitions.

### `ner.py`
Named Entity Recognition engine for extracting:
- Parties, dates, amounts
- Jurisdictions, emails, phone, URLs

### `risk_detection.py`
Rule-based risk detection with severity scoring and contract-level risk aggregation.

### `contract_classifier.py`
Classifies contracts by type with confidence scoring.

### `clause_explainer.py`
Provides plain-language explanations and alternative clause suggestions for common contract clauses.

### `pdf_report.py`
Generates comprehensive PDF reports with analysis results and recommendations.

## Configuration

No additional configuration needed. The app works out-of-the-box with default settings.

### Optional: Environment Variables

Create a `.env` file if integrating external APIs:
```
OPENAI_API_KEY=your_key_here
```

## Limitations & Notes

- Clause extraction uses regex patterns (heuristic-based)
- NER uses pattern matching, not deep learning
- Risk detection is rule-based (not ML-trained)
- PDF extraction quality depends on source formatting
- Always verify results with legal counsel

## Future Enhancements

- [ ] LLM integration for better explanations (GPT-4/Claude)
- [ ] Machine learning-based risk scoring
- [ ] Batch contract analysis
- [ ] Custom risk rule templates
- [ ] Multi-language support
- [ ] Integration with document management systems
- [ ] Comparison between multiple contracts
- [ ] Negotiation templates and suggestions

## Testing

Test with sample contracts provided in `sample_contracts/`:
- `sample_contract.txt`: Employment Agreement
- `lease_agreement.txt`: Residential Lease

## Troubleshooting

### "Module not found" error
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Streamlit not running
```bash
# Check Python version
python --version

# Reinstall Streamlit
pip install streamlit --upgrade
```

### PDF extraction issues
- Ensure PDF is not password-protected
- Try converting PDF to text first

## License

This project is provided as-is for educational and commercial use.

## Support & Contact

For issues, questions, or feature requests, please open an issue or contact the development team.

---

**Note**: This tool provides informational analysis only. Always consult with legal counsel before signing any contract. Analysis results are not a substitute for professional legal advice.
