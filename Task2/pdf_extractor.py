import pandas as pd
import requests

import json
import os

from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from bs4 import BeautifulSoup


def write_file(file, response):
    with open(file, 'wb') as f:
        f.write(response.content)
    f.close()

# Convert each page of the pdf into a jpg image, which is stored locally
def convert_pdf_to_image():
    print("reading temp.pdf")
    pages = convert_from_path(temp_pdf)

    image_counter = 1

    print("forming images")
    for page in pages:
        filename = "./temp/page_"+str(image_counter)+".jpg"
        page.save(filename, 'JPEG')
        image_counter += 1
    
    print("forming .txt file")
    filelimit = image_counter-1
    
    pdf_content = ''
    #  Use OCR (tesseract) to read text from image using the mar.traineddata into pdf_content
    for i in range(1, filelimit + 1):
        filename = "./temp/page_"+str(i)+".jpg"
        print("processing file " + filename)
        text = str(((pytesseract.image_to_string(Image.open(filename), lang='mar'))))
        text = text.replace(u'-\n', '') 
        text = text + u"\n============================\n"
        pdf_content += text
    return pdf_content

def delete_jpg(folder_path):
    test = os.listdir(folder_path)
    for images in test:
        if images.endswith('.jpg'):
            os.remove(os.path.join(folder_path, images))

def create_json(df, temp_df):
    json_list = []
    for index, entry in df.iterrows():
        json_obj = {'page-url': '', 'pdf-url': '', 'pdf-content': ''}
        url = entry[0]

        # For each entry in the dataframe that ends with '.pdf'
        if url.endswith('.pdf'):

            # page_url = pdf_url
            page_url = url
            pdf_url = url

            # download the pdf file
            response = requests.get(url)

        # For each entry in the dataframe that does not end with '.pdf:
        else:
            print('processing non pdf url')
            page_url = url
            r = requests.get(url)

            # Use BeautifulSoup to download the html
            soup = BeautifulSoup(r.text, 'html.parser')

            # Parse the html for the basehost and href to the pdf file to prepare a pdf_url
            url_list = set()
            for a in soup.find_all('a', href=True):
                if a['href'].endswith('.pdf'):
                    base = soup.find('ia-topnav', basehost=True)['basehost']
                    url_list.add(base+a['href'])
            url_list = list(url_list)
            pdf_url = url_list[0]

            # Download the pdf file
            response = requests.get(pdf_url)

        print("writing temp pdf")
        write_file(temp_df, response)

        # Convert each page of the pdf into a jpg image, which is stored locally
        pdf_content = convert_pdf_to_image()

        # Update a dictionary with page_url, pdf_url and pdf_content
        json_obj['page-url'] = page_url
        json_obj['pdf-url'] = pdf_url
        json_obj['pdf-content'] = pdf_content
        json_list.append(json_obj)

        delete_jpg(folder_path)

    # Save dictionary in the pdf_extract.json file in utf-8 format
    file_data = json.dumps(json_list, ensure_ascii=False)
    with open('pdf_extract.json', 'w', encoding='utf-8') as outfile:
        outfile.write(file_data)
    outfile.close()

if __name__ == '__main__':
    
    # Read google sheet into dataframe
    df = pd.read_csv('https://docs.google.com/spreadsheets/d/1I7hziCQGd0uKzh4RMnZtpkTspaE-1_bIL0FcGU_Y1DU/export?format=csv')
    folder_path = os.getcwd()+'/temp'
    temp_pdf = './temp/temp.pdf'
    create_json(df, temp_pdf)