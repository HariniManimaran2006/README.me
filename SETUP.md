# SETUP & DEPLOYMENT GUIDE - Contract Auditor

## Quick Start

### Windows Users

**Option 1: Using Setup Script (Recommended)**
```powershell
# Run the setup script
.\setup.bat
```

**Option 2: Manual Setup**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\Activate.ps1

# If you get an execution policy error, use this instead:
# venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### macOS/Linux Users

**Option 1: Using Setup Script (Recommended)**
```bash
chmod +x setup.sh
./setup.sh
```

**Option 2: Manual Setup**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Storage**: 500MB for dependencies
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

## Dependency Installation

If you encounter issues installing dependencies:

```bash
# For PDF support
pip install PyPDF2 pdfminer.six

# For DOCX support
pip install python-docx

# For PDF report generation
pip install fpdf2

# For Streamlit
pip install streamlit

# All in one go
pip install -r requirements.txt --upgrade
```

## Troubleshooting

### Python Not Found
```
ERROR: Python is not installed or not in PATH
```
**Solution**: Install Python from https://www.python.org/downloads/ and ensure "Add Python to PATH" is checked during installation.

### Streamlit Not Starting
```
ERROR: streamlit command not found
```
**Solution**: Ensure venv is activated and reinstall:
```bash
pip install streamlit --upgrade
```

### Import Errors
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution**: Make sure venv is activated (you should see (venv) in terminal prompt) and run:
```bash
pip install -r requirements.txt
```

### Port 8501 Already in Use
```
ERROR: Port 8501 is already in use
```
**Solution**: Either kill the existing process or specify a different port:
```bash
streamlit run app.py --server.port 8502
```

## File Structure After Setup

```
contract-auditor/
├── venv/                          # Virtual environment (created after setup)
├── app.py                         # Main app
├── requirements.txt               # Dependencies
├── setup.bat                      # Windows setup script
├── setup.sh                       # macOS/Linux setup script
├── README.md                      # Full documentation
├── SETUP.md                       # This file
├── .gitignore                     # Git ignore rules
├── utils/                         # Utility modules
│   ├── text_extraction.py
│   ├── clause_extraction.py
│   ├── ner.py
│   ├── risk_detection.py
│   ├── contract_classifier.py
│   ├── clause_explainer.py
│   └── pdf_report.py
├── sample_contracts/              # Test contracts
│   ├── sample_contract.txt
│   └── lease_agreement.txt
├── templates/                     # HTML templates (future)
└── audit_logs/                    # Generated audit logs
```

## Running the App

### Standard Run
```bash
streamlit run app.py
```

### With Custom Port
```bash
streamlit run app.py --server.port 8502
```

### With Custom Theme
```bash
streamlit run app.py --theme.base dark
```

## Next Steps After Setup

1. **Test the app** by uploading a sample contract from `sample_contracts/` folder
2. **Upload your own contracts** for real analysis
3. **Download audit logs** and PDF reports from the app
4. **Deploy to Streamlit Cloud** (see deployment instructions)

## Deployment to Streamlit Cloud

1. Push project to GitHub (see GitHub setup instructions)
2. Go to https://streamlit.io/cloud
3. Click "New app" and select your repository
4. Set main file path to `app.py`
5. Deploy!

## Performance Tips

- Use modern PDF/DOCX files for best extraction quality
- Large contracts (>50MB) may take longer to process
- Keep audit logs directory clean for faster loading
- Consider archiving old audit logs occasionally

---

For more information, see README.md
