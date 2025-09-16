import os
import uuid
from flask import (
    Blueprint,
    request,
    render_template,
    send_from_directory,
    send_file,
    current_app,
    redirect,
    url_for,
    flash,
    abort,
)
from werkzeug.utils import secure_filename
from .extractor import process_document, list_outputs
from .utils import validate_upload_file, get_file_info

main = Blueprint("main", __name__)

ALLOWED_EXT = {"pdf", "docx"}


@main.route("/", methods=["GET"])
def index():
    outputs = list_outputs(current_app.config["OUTPUT_FOLDER"])
    # Log the outputs for debugging
    current_app.logger.info(f"Available output files: {outputs}")
    return render_template("index.html", outputs=outputs)


@main.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    extract_text = bool(request.form.get("extract_text"))
    extract_tables = bool(request.form.get("extract_tables"))
    desired_fields = request.form.get("fields", "")  # comma-separated fields user wants
    out_format = request.form.get("format", "csv")  # csv or excel

    # Validate file
    if not file or not file.filename:
        flash("No file selected", "danger")
        return redirect(url_for("main.index"))

    # Validate file type
    is_valid, error_msg = validate_upload_file(file.filename, ALLOWED_EXT)
    if not is_valid:
        flash(error_msg, "danger")
        return redirect(url_for("main.index"))

    # Check if at least one extraction option is selected
    if not extract_text and not extract_tables:
        flash("Please select at least one extraction option (text or tables)", "danger")
        return redirect(url_for("main.index"))

    filename = secure_filename(file.filename)
    uid = uuid.uuid4().hex
    upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{uid}_{filename}")

    # Ensure upload directory exists
    os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(current_app.config["OUTPUT_FOLDER"], exist_ok=True)

    try:
        file.save(upload_path)

        # Process the document
        out_path = process_document(
            upload_path,
            output_folder=current_app.config["OUTPUT_FOLDER"],
            extract_text=extract_text,
            extract_tables=extract_tables,
            desired_fields=[f.strip() for f in desired_fields.split(",") if f.strip()],
            out_format=out_format,
        )

        # Clean up uploaded file
        if os.path.exists(upload_path):
            os.remove(upload_path)

        # Log all generated files for debugging
        output_files = list_outputs(current_app.config["OUTPUT_FOLDER"])
        current_app.logger.info(f"Files after processing: {output_files}")

        if out_path and os.path.exists(out_path):
            flash(
                f"✅ File processed successfully: {os.path.basename(out_path)}",
                "success",
            )
            current_app.logger.info(f"Primary output file: {out_path}")
        else:
            flash(
                "⚠️ File processed but no primary output generated. Check generated files below.",
                "warning",
            )

    except Exception as e:
        # Clean up uploaded file on error
        if os.path.exists(upload_path):
            os.remove(upload_path)
        flash(f"❌ Processing failed: {str(e)}", "danger")
        current_app.logger.error(f"Processing error: {str(e)}")

    return redirect(url_for("main.index"))


@main.route("/download/<filename>")
def download(filename):
    """Download generated files"""
    try:
        output_dir = current_app.config.get("OUTPUT_FOLDER", "outputs")
        file_path = os.path.join(output_dir, filename)

        # Log for debugging
        current_app.logger.info(f"Download request for: {filename}")
        current_app.logger.info(f"Looking in directory: {output_dir}")
        current_app.logger.info(f"Full file path: {file_path}")
        current_app.logger.info(f"File exists: {os.path.exists(file_path)}")

        if not os.path.exists(file_path):
            current_app.logger.error(f"File not found: {file_path}")
            flash(f"File '{filename}' not found.", "danger")
            return redirect(url_for("main.index"))

        # List all files in output directory for debugging
        output_files = list_outputs(output_dir)
        current_app.logger.info(f"Available output files: {output_files}")

        # Use absolute path to avoid redirect issues
        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception as e:
        current_app.logger.error(f"Download error: {str(e)}")
        flash(f"Error downloading file: {str(e)}", "danger")
        return redirect(url_for("main.index"))


@main.route("/preview/<path:filename>")
def preview(filename):
    """Preview generated files in browser"""
    try:
        output_dir = current_app.config.get("OUTPUT_FOLDER", "outputs")
        file_path = os.path.join(output_dir, filename)

        # Log for debugging
        current_app.logger.info(f"Preview request for: {filename}")
        current_app.logger.info(f"Looking in directory: {output_dir}")
        current_app.logger.info(f"Full file path: {file_path}")
        current_app.logger.info(f"File exists: {os.path.exists(file_path)}")

        if not os.path.exists(file_path):
            current_app.logger.error(f"File not found: {file_path}")
            flash(f"File '{filename}' not found.", "danger")
            return redirect(url_for("main.index"))

        # List all files for debugging
        output_files = list_outputs(output_dir)
        current_app.logger.info(f"Available output files: {output_files}")

        # Handle different file types
        if filename.endswith(".json"):
            import json

            with open(file_path, "r") as f:
                content = json.load(f)
            return render_template(
                "preview.html", filename=filename, content=content, file_type="json"
            )

        elif filename.endswith(".csv"):
            import pandas as pd

            df = pd.read_csv(file_path)
            return render_template(
                "preview.html",
                filename=filename,
                content=df.to_dict("records"),
                file_type="csv",
                headers=df.columns.tolist(),
            )

        elif filename.endswith(".xlsx"):
            import pandas as pd

            df = pd.read_excel(file_path)
            return render_template(
                "preview.html",
                filename=filename,
                content=df.to_dict("records"),
                file_type="excel",
                headers=df.columns.tolist(),
            )

        elif filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return render_template(
                "preview.html", filename=filename, content=content, file_type="text"
            )

        else:
            # For other file types, use send_file with absolute path
            return send_file(file_path, as_attachment=False)

    except Exception as e:
        current_app.logger.error(f"Preview error: {str(e)}")
        flash(f"Error previewing file: {str(e)}", "danger")
        return redirect(url_for("main.index"))


@main.route("/debug/files")
def debug_files():
    """Debug route to show available files and their details"""
    import os

    output_folder = current_app.config["OUTPUT_FOLDER"]
    files_info = []

    if os.path.exists(output_folder):
        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)
            if os.path.isfile(file_path):
                stat_info = os.stat(file_path)
                files_info.append(
                    {
                        "name": filename,
                        "size": stat_info.st_size,
                        "modified": stat_info.st_mtime,
                        "path": file_path,
                        "exists": True,
                    }
                )

    return render_template("debug.html", files=files_info, output_folder=output_folder)
