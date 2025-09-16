import os
import uuid
from flask import (
    Blueprint,
    request,
    render_template,
    send_from_directory,
    current_app,
    redirect,
    url_for,
    flash,
)
from werkzeug.utils import secure_filename
from .extractor import process_document, list_outputs
from .utils import validate_upload_file, get_file_info

bp = Blueprint("main", __name__)

ALLOWED_EXT = {"pdf", "docx"}


@bp.route("/", methods=["GET"])
def index():
    outputs = list_outputs(current_app.config["OUTPUT_FOLDER"])
    return render_template("index.html", outputs=outputs)


@bp.route("/upload", methods=["POST"])
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

        if out_path and os.path.exists(out_path):
            flash(
                f"✅ File processed successfully: {os.path.basename(out_path)}",
                "success",
            )
        else:
            flash(
                "⚠️ File processed but no output generated. Check your extraction options.",
                "danger",
            )

    except Exception as e:
        # Clean up uploaded file on error
        if os.path.exists(upload_path):
            os.remove(upload_path)
        flash(f"❌ Processing failed: {str(e)}", "danger")
        current_app.logger.error(f"Processing error: {str(e)}")

    return redirect(url_for("main.index"))


@bp.route("/outputs/<path:filename>")
def download(filename):
    return send_from_directory(
        current_app.config["OUTPUT_FOLDER"], filename, as_attachment=True
    )
