"""
Utility functions for the document extraction tool.
"""

import os
import re
from typing import List, Dict, Any


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing or replacing invalid characters.
    """
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
    # Remove leading/trailing whitespace and dots
    filename = filename.strip(" .")
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[: 255 - len(ext)] + ext
    return filename


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format.
    """
    if size_bytes == 0:
        return "0B"

    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.1f}{size_names[i]}"


def get_file_info(filepath: str) -> Dict[str, Any]:
    """
    Get file information including size, modification time, etc.
    """
    if not os.path.exists(filepath):
        return {}

    stat = os.stat(filepath)
    return {
        "size": stat.st_size,
        "size_formatted": format_file_size(stat.st_size),
        "modified": stat.st_mtime,
        "extension": os.path.splitext(filepath)[1].lower(),
    }


def validate_upload_file(filename: str, allowed_extensions: set) -> tuple[bool, str]:
    """
    Validate if uploaded file is allowed.
    Returns (is_valid, error_message)
    """
    if not filename:
        return False, "No file selected"

    # Check if file has extension
    if "." not in filename:
        return False, "File must have an extension"

    ext = filename.rsplit(".", 1)[1].lower()
    if ext not in allowed_extensions:
        return (
            False,
            f"File type '{ext}' not allowed. Allowed types: {', '.join(allowed_extensions)}",
        )

    return True, ""


def clean_extracted_text(text: str) -> str:
    """
    Clean extracted text by removing excessive whitespace and formatting.
    """
    if not text:
        return ""

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)
    # Remove leading/trailing whitespace
    text = text.strip()
    # Remove common OCR artifacts
    text = re.sub(r"[^\w\s\.,;:!?()-]", "", text)

    return text
