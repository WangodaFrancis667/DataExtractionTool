# Document Extractor

## Run locally (with Docker)
1. Build: `docker compose build`
2. Run: `docker compose up -d`
3. Open: http://localhost:8000

Uploaded files are stored in `./uploads`, outputs in `./outputs`.

## Notes
- Camelot may need extra system packages (ghostscript/poppler). See the Camelot docs for platform-specific install instructions.
- This is an MVP. You can extend the GUI to add fine-grained field selection, OCR for scanned PDFs, job queueing (Celery + Redis) for large files, and authentication.
