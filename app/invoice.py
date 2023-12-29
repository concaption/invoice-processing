"""
path: main/invoice.py
author: @concaption
date: 2023-10-18
description: A class used to represent an invoice. It extracts information
from a PDF invoice and stores it in a pandas DataFrame.
"""
import os
import re
from collections import defaultdict
import logging
import traceback
import pdfplumber
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class Invoice:
    """
    A class used to represent an invoice. It extracts information from a PDF
    invoice and stores it in a pandas DataFrame.

    Attributes
    ----------
    pdf_path : str
        The path to the PDF invoice file
    text : str
        The text extracted from the PDF invoice
    order_info : pandas.DataFrame
        A DataFrame containing general order information
    sku_details_df : pandas.DataFrame
        A DataFrame containing SKU and product details
    to_dataframe : pandas.DataFrame
        A DataFrame containing general order information and SKU and product details

    Methods
    -------
    extract_text()
        Extract text from PDF file
    extract_order_info()
        Extract general order information from text
    extract_sku_details()
        Extract SKU and product details from text
    _to_dataframe()
        Combine general order information and SKU and product details into a single DataFrame
    """

    def __init__(self, pdf_path):
        if not pdf_path.endswith(".pdf"):
            logger.error(
                "Invalid file path. Only PDF files are supported. %s", pdf_path)
        if not os.path.exists(pdf_path):
            logger.error("File not found. Please check the file path. %s", pdf_path)
        self.pdf_path = pdf_path
        self.text = self.extract_text()
        self.order_info = self.extract_order_info()
        self.sku_details_df = self.extract_sku_details()
        self.to_dataframe = self._to_dataframe()

    def extract_text(self):
        """
        Extract text from PDF file

        Returns
        -------
        str
            The text extracted from the PDF invoice

        Raises
        ------
        ValueError
            If the PDF file is invalid
        """
        text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text = text + "\n" + page.extract_text()
        logger.info("Text extracted from PDF file. %s", self.pdf_path)
        return text

    def extract_order_info(self):
        """Extract general order information from text"""
        order_info = defaultdict(list)

        patterns = {
            "Order Number": r"Invoice [a-zA-Z0-9, ]+",
            "Invoice Date": r"(\d{2}/\d{2}/\d{4}), \d{2}:\d{2} Invoice",
            "Order Date": r"Order Date: ([a-zA-Z0-9, ]+)",
            "Shipping Address": r"SHIPPING ADDRESS\n([\s\S]+?)\nActive Memberships",
            "Membership Type": r"Active Memberships when order placed: ([a-zA-Z0-9, ]+)",
            "Email": r"✉ ([\w\.-]+@[\w\.-]+)",
            "Phone": r"\uf095 ?\+?([\d-]+)",
            # "Phone": r"\uf095 ([\d-]+)",
            "Subtotal": r"Subtotal: \$([^\n\r]*)",
            "Discount": r"Discount: -\$([^\n\r]*)",
            "Shipping": r"Shipping: ([^\n\r]*)",
            "Payment Method": r"Payment method: ([a-zA-Z ]+)",
            "Total": r"Total: \$([^\n\r]*)",
        }

        for field, pattern in patterns.items():
            try:
                match = re.search(pattern, self.text)
                if match:
                    order_info[field] = (
                        match.group(1) if match.groups() else match.group(0)
                    )
                else:
                    logger.warning("%s not found. Adding null value.", field)
                    print(f"{field} not found. Adding null value.")
                    order_info[field] = None
            except Exception as e:
                logger.error("Failed to extract %s from invoice. %s", field, e)
                traceback.print_exc()
        try:
            sections = self.text.split("\n")
            coupons = [
                section[2:] for section in sections if section.startswith("\uf02b")
            ]
            order_info["Coupon"] = coupons
        except Exception as e:
            logger.warning("Coupon not found. Adding null value. %s", e)
            print("Coupon not found. Adding null value.")
            order_info["Coupon"] = None

        # Create DataFrame for general order information
        general_order_df = pd.DataFrame([order_info])
        general_order_df["Shipping Address"] = general_order_df[
            "Shipping Address"
        ].str.replace("\n", ", ")
        logger.info("General order information extracted from invoice.")
        general_order_df['Invoice Date'] = pd.to_datetime(general_order_df['Invoice Date'],
                                                          format='%d/%m/%Y').dt.strftime('%m/%d/%Y')
        return general_order_df

    def extract_sku_details(self):
        """
        Extract SKU and product details from text

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing SKU and product details

        Raises
        ------
        ValueError
            If the invoice does not contain SKU and product details
        """
        # Split the text into sections based on known delimiters
        sections = self.text.split("\n")

        try:
            # Find the index where SKU and product details start and end
            start_idx = sections.index("SKU Product Quantity Price") + 1
            end_idx = len(sections)
        except ValueError:
            print("The invoice does not contain SKU and product details.")
            logger.error("The invoice does not contain SKU and product details.")

        # Extract the SKU and product details from the relevant section
        sku_details_text = "\n".join(sections[start_idx:end_idx])

        # Initialize lists to store product information
        order_info = defaultdict(list)

        # Split the SKU details text into lines
        lines = sku_details_text.split("\n")

        # Initialize variables to hold the current product type and other details
        current_product_type = None

        # Loop through each line to extract SKU and product details
        keywords_to_skip = [
            "DOSAGE",
            "Subtotal:",
            "Discount:",
            "Shipping:",
            "Payment method:",
            "Total:",
            "coupon used:",
        ]
        for line in lines:
            # Skip lines that don't contain SKU and product details
            if any(keyword in line for keyword in keywords_to_skip):
                continue
            elif re.match(r"^[A-Z][a-zA-Z ]+$", line):
                current_product_type = line
            else:
                parts = line.split()
                # Check if the line contains enough parts to be valid SKU and product details
                if len(parts) >= 4:
                    order_info["SKU Name"].append(parts[0])
                    order_info["Quantity"].append(parts[-2])
                    order_info["Price"].append(parts[-1])
                    order_info["Product Name"].append(" ".join(parts[1:-2]))
                    order_info["Product Type"].append(current_product_type)

        # Create a DataFrame from the extracted order_info dictionary
        sku_details_df = pd.DataFrame(order_info)

        # Convert 'Quantity' column to numeric, drop rows with null quantity
        sku_details_df["Quantity"] = pd.to_numeric(
            sku_details_df["Quantity"], errors="coerce"
        )
        sku_details_df.dropna(subset=["Quantity"], inplace=True)
        sku_details_df["Quantity"] = sku_details_df["Quantity"].astype(int)

        # Replace "SKU Product Quantity Price" in 'Product Type' with NaN
        sku_details_df["Product Type"] = sku_details_df["Product Type"].replace(
            "SKU Product Quantity Price", np.nan
        )

        # Forward-fill NaN values in 'Product Type'
        sku_details_df["Product Type"].ffill(inplace=True)

        # Reset the index
        sku_details_df.reset_index(drop=True, inplace=True)
        return sku_details_df

    def _to_dataframe(self):
        """
        Combine general order information and SKU and product details into a single DataFrame

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing general order information and SKU and product details
        """
        # Repeat order_info to match the number of rows in sku_details_df
        order_info_repeated = pd.concat(
            [self.order_info] * len(self.sku_details_df), ignore_index=True
        )
        # Concatenate the repeated order_info with sku_details_df along axis 1
        result = pd.concat([order_info_repeated, self.sku_details_df], axis=1)
        result = result.replace(np.nan, '', regex=True) # added latter
        result = result.replace("nan", '', regex=True) # added latter
        result = result.replace({None: ''}) # added latter
        return result
