# 📄 Document Extractor

A powerful web-based tool for extracting text, tables, and specific fields from PDF and DOCX documents. Built with Flask and featuring advanced PDF processing capabilities.

## ✨ Features

- **Multi-format Support**: Extract data from PDF and DOCX files
- **Text Extraction**: Full text content extraction with clean formatting
- **Table Extraction**: Advanced table detection and extraction using `pdfplumber` and `camelot-py`
- **Field Extraction**: Smart field detection for specific data points (e.g., "Invoice Number", "Date", "Total Amount")
- **Multiple Output Formats**: Export as CSV, Excel, JSON, or plain text
- **Web Interface**: User-friendly web interface for easy file uploads and downloads
- **Local Processing**: All processing happens locally - your documents never leave your machine

## 🚀 Quick Start

### Option 1: Local Development Setup (Recommended)

#### Prerequisites

Make sure you have Python 3.8+ installed on your system.

#### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/WangodaFrancis667/DataExtractionTool.git
   cd DataExtractionTool
   ```

2. **Install system dependencies (platform-specific)**

   **macOS:**
   ```bash
   # Install required system libraries
   brew install libmagic poppler ghostscript
   
   # For M1/M2 Macs, you might also need:
   brew install pkg-config
   ```

   **Ubuntu/Debian Linux:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y libmagic1 libmagic-dev poppler-utils ghostscript
   
   # For table extraction with camelot-py:
   sudo apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1
   ```

   **CentOS/RHEL/Fedora:**
   ```bash
   # For RHEL/CentOS:
   sudo yum install -y file-libs file-devel poppler-utils ghostscript
   
   # For Fedora:
   sudo dnf install -y file-libs file-devel poppler-utils ghostscript
   ```

   **Windows:**
   ```powershell
   # Install using conda (recommended for Windows):
   conda install -c conda-forge libmagic poppler
   
   # Or use chocolatey:
   choco install ghostscript
   # Note: You may need to manually install libmagic for Windows
   ```

3. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   # Make the run script executable (macOS/Linux):
   chmod +x run_local.py
   ./run_local.py
   
   # Or run directly with Python:
   python run_local.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

### Option 2: Docker Setup

#### Prerequisites
- Docker and Docker Compose installed

#### Quick Docker Setup
```bash
# Build and run with Docker
docker compose build
docker compose up -d

# Access the application
open http://localhost:8000
```

**Note**: The Docker setup may have issues with camelot-py dependencies. Use the local setup for full functionality.

## 📖 Usage Guide

### Basic Usage

1. **Upload a Document**
   - Navigate to the web interface
   - Click "Choose file" and select a PDF or DOCX file
   - Select extraction options (text, tables, or both)

2. **Configure Extraction Options**
   - **Extract Text**: Gets all readable text from the document
   - **Extract Tables**: Detects and extracts tabular data
   - **Specific Fields**: Enter comma-separated field names to extract specific data points

3. **Choose Output Format**
   - **CSV**: Best for tabular data and field extraction
   - **Excel**: Multiple sheets for different tables

4. **Download Results**
   - Files are automatically processed and available for download
   - Multiple output files may be generated depending on your selections

### Field Extraction Examples

The tool can intelligently extract specific fields from documents. Here are some examples:

```
# Invoice Processing
Fields: "Invoice Number, Date, Total Amount, Customer Name"

# Contract Analysis  
Fields: "Contract ID, Effective Date, Expiration Date, Party Names"

# Receipt Processing
Fields: "Store Name, Transaction Date, Total, Payment Method"
```

## 🛠️ Troubleshooting

### Common Installation Issues

#### macOS Issues

**Problem**: `ImportError: failed to find libmagic`
```bash
# Solution:
brew install libmagic
```

**Problem**: `camelot-py` installation fails
```bash
# Try installing without cv extras first:
pip install camelot-py==0.10.1
pip install opencv-python==4.8.1.78
```

#### Linux Issues

**Problem**: `ImportError: libGL.so.1: cannot open shared object file`
```bash
# Ubuntu/Debian:
sudo apt-get install libgl1-mesa-glx

# CentOS/RHEL:
sudo yum install mesa-libGL
```

**Problem**: Permission denied errors
```bash
# Make sure you have proper permissions:
chmod +x run_local.py
```

#### Windows Issues

**Problem**: `python-magic` not working
```powershell
# Install with conda (recommended):
conda install -c conda-forge python-magic

# Or try the Windows-specific version:
pip install python-magic-bin
```

**Problem**: `camelot-py` dependencies
```powershell
# Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Then install dependencies:
pip install opencv-python==4.8.1.78
```

### Runtime Issues

**Problem**: "No secret key set" error
- This should be automatically handled in the latest version
- If you see this error, restart the application

**Problem**: Upload fails
- Check file size (limit: 50MB)
- Ensure file is PDF or DOCX format
- Check file permissions

**Problem**: Table extraction not working
- Try different PDF files (some PDFs have complex layouts)
- Ensure `camelot-py` is properly installed
- Check that system dependencies are installed

### Performance Issues

**Large Files**: 
- Files over 10MB may take longer to process
- Consider splitting large documents
- Increase system memory if processing fails

**Complex Tables**:
- Some complex table layouts may not extract perfectly
- Try both CSV and Excel output formats
- Manual post-processing may be required

## 🔧 Development

### Project Structure
```
DataExtractionTool/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # Web routes and handlers
│   ├── extractor.py         # Document processing logic
│   ├── utils.py             # Utility functions
│   ├── templates/
│   │   └── index.html       # Web interface
│   └── static/
│       └── style.css        # Styling
├── uploads/                 # Temporary file uploads
├── outputs/                 # Generated output files
├── requirements.txt         # Python dependencies
├── docker-compose.yml       # Docker configuration
├── Dockerfile              # Docker image definition
└── run_local.py            # Local development server
```

### Adding New Features

To extend the application:

1. **Add new file formats**: Modify `extractor.py` to support additional formats
2. **Improve field extraction**: Enhance pattern matching in `extract_fields_from_text()`
3. **Add authentication**: Implement user management in `routes.py`
4. **Add job queuing**: Integrate Celery for background processing

## 📋 Requirements

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: 2GB RAM minimum (4GB+ recommended for large files)
- **Storage**: 1GB free space
- **OS**: macOS 10.14+, Ubuntu 18.04+, Windows 10+

### Python Dependencies
- Flask 2.3.3
- pdfplumber 0.8.0
- camelot-py 0.10.1
- python-docx 0.8.11
- pandas 2.2.0
- openpyxl 3.1.2
- python-magic 0.4.27

See `requirements.txt` for complete list.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Search existing [GitHub Issues](https://github.com/WangodaFrancis667/DataExtractionTool/issues)
3. Create a new issue with:
   - Your operating system
   - Python version
   - Error messages
   - Steps to reproduce

## 🎯 Roadmap

- [ ] OCR support for scanned PDFs
- [ ] API endpoints for programmatic access
- [ ] Batch processing capabilities
- [ ] User authentication and file management
- [ ] Cloud deployment options
- [ ] Advanced table extraction algorithms
- [ ] Support for more file formats (Excel, Word, etc.)

---

**Happy Document Extracting! 🚀**
