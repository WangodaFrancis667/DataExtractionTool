#!/usr/bin/env python3
"""
Local development server for the Document Extraction Tool
"""

import os
from app import create_app

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    app = create_app()
    app.config['UPLOAD_FOLDER'] = './uploads'
    app.config['OUTPUT_FOLDER'] = './outputs'
    
    # Run in debug mode for development
    app.run(debug=True, host='0.0.0.0', port=8000)