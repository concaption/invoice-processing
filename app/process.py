"""
path: app/services/process.py
author: @concaption
date: 2023-10-18
description: This module contains functions for processing files.
"""

import os
import logging
from fastapi import UploadFile
from app.invoice import Invoice
from app.sheet import SheetsClient
from app.config import settings

logger = logging.getLogger(__name__)

def process_file(file: UploadFile, sheets_client: SheetsClient):
    """
    Processes the file and uploads the data to the spreadsheet.
    """
    try:
        if not os.path.exists(settings.PDF_DIR):
            os.makedirs(settings.PDF_DIR)
        file_name = os.path.join(settings.PDF_DIR, file.filename)
        with open(file_name, "wb") as buffer:
            buffer.write(file.file.read())
        try:
            invoice = Invoice(file_name)
            sheets_client.add_dataframe(
                data_frame=invoice.to_dataframe,
                sheet_name=settings.SHEET_NAME,
                spreadsheet_name=settings.SPREADSHEET_NAME
                )
            # Delete the file from the tempdir
            os.remove(file_name)
            logger.info("File %s processed successfully.", file.filename)
            print(f"File {file.filename} processed successfully.")
        except:
            os.remove(file_name)
    except Exception as e:
        print(e)
        print(f"Error processing file: {file.filename}")
        logger.error("Error processing file: %s", file.filename)
        
