try:
    import openpyxl
except ImportError as exc:
    raise ImportError(
        "The 'openpyxl' package is required to read Excel files. "
        "Install it with: python -m pip install openpyxl"
    ) from exc
from src.modules.application import Application

def extract_data(file_path):
    # Load the Excel file
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # Extract data from the sheet
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header row
        application_data = {
            "from_email": row[0],
            "candidate_name": row[1],
            "subject": row[2],
            "message": row[3],
            "job_title": row[4]
        }
        data.append(application_data)

    return data