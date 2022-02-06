# PDF Extractor

This project performs a extraction of text from a pdf; and the page url, pdf url and pdf content for each pdf. The result is returned in the form of a json file.

## Prerequisistes
* Install tessearct
    > brew install tessearct
* Install poppler
    > brew install poppler
* Run
    > pip install -r requirements.txt
* Download tesseract [traineddata files](https://github.com/tesseract-ocr/tessdata/releases)
* Add enviroment variable TESSDATA_PREFIX="/<path to tessdata-4.1.0/>/tessdata-4.1.0/"

## How to use
* Run 
    > python pdf_extractor.py

## Design details

### Design assumptions
1. All pdf files contain marathi text.

### Implementation approach
Used wikipedia library to:
* Read google sheet into dataframe
* For each entry in the dataframe that ends with '.pdf':
    * page_url = pdf_url
    * download the pdf file
* For each entry in the dataframe that does not end with '.pdf:
    * Use BeautifulSoup to download the html
    * Parse the html for the basehost and href to the pdf file to prepare a pdf_url
    * Download the pdf file
* Convert each page of the pdf into a jpg image, which is stored locally
* Use OCR (tesseract) to read text from image using the mar.traineddata into pdf_content
* Update a dictionary with page_url, pdf_url and pdf_content
* Save dictionary in the pdf_extract.json file in utf-8 format
