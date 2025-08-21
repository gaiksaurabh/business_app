# jobs/excel_loader.py
import os
import pandas as pd
from django.conf import settings

# Correct path to Excel file (kept in project root where manage.py is located)
EXCEL_FILE = os.path.join(settings.BASE_DIR, "July MAIN.xlsx")

def load_dropdown_data():
    """
    Loads all sheet names from the Excel file and returns them
    as dropdown options.
    """
    try:
        # Get all sheet names in the Excel file
        xls = pd.ExcelFile(EXCEL_FILE)
        sheet_names = xls.sheet_names  

        # Format as list of tuples for Django form dropdowns
        dropdown_options = [(name, name) for name in sheet_names]

        return dropdown_options

    except FileNotFoundError:
        print(f"❌ Excel file not found at {EXCEL_FILE}")
        return []

    except Exception as e:
        print(f"⚠️ Error reading Excel file: {e}")
        return []
