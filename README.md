<div align="center">
<h1>PDF Invoice processing and Inventory mangement in google sheets</h1>
  
![GitHub contributors](https://img.shields.io/github/contributors/concaption/invoice-processing?color=%2333d679&style=flat-square)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
</div>

![Job Board in django](/screenshot.png)

A FastAPI web application for an Ecommarce that automates the process of invoice data extraction and Google Sheet updating. The web application serves as a central hub for collecting and managing invoice data, providing both automated and manual options for PDF uploads. Created using FastAPI, OAuth2, and a variety of other technologies, the application is robust, secure, and highly automated. It features scheduled email fetching to automate the collection of invoices and offers data validation checks to ensure the consistency and accuracy of the populated data.

### Features

1. **User Authentication**: Secure login mechanism to authenticate users.
2. **PDF Upload**: Interface to upload PDF files manually.
3. **Data Extraction**: Extract specific fields like order code, shipping address, product details, etc., from the uploaded PDF.
4. **Google Sheets Integration**: Populate the extracted data into a Google Sheet.
5. **Scheduled Email Fetching**: Automated function to fetch PDF attachments from a user’s email at scheduled intervals.
6. **Data Validation**: Validation checks to ensure data consistency and accuracy.

### Technology

- Backend: FastAPI
- User Authentication: OAuth2 (admin account only)
- PDF Parsing: PyPDF2 or pdfplumber
- Data Population: Google Sheets API
- Front-end: HTML, CSS, and JavaScript


## Installation steps

Clone the Repo and install the requirements

```
git clone https://github.com/concaption/invoice-processing.git
cd invoice-processing
pip install -r requirements.txt
python main.py
```

## Author
You can get in touch with me on my LinkedIn Profile:

#### Usama Navid
[![LinkedIn Link](https://img.shields.io/badge/Connect-concaption-blue.svg?logo=linkedin&longCache=true&style=social&label=Connect
)](https://www.linkedin.com/in/concaption)

You can also follow my GitHub Profile to stay updated about my latest projects: [![GitHub Follow](https://img.shields.io/badge/Connect-concaption-blue.svg?logo=Github&longCache=true&style=social&label=Follow)](https://github.com/concaption)

If you liked the repo then kindly support it by giving it a star ⭐!

## Contributions Welcome
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](#)[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

If you find any bug in the code or have any improvements in mind then feel free to generate a pull request.