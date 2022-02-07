import pandas as pd
import requests

import json
import os

from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from bs4 import BeautifulSoup

# Save the pdf file from the response object
def write_file(file, response):
    with open(file, 'wb') as f:
        f.write(response.content)
    f.close()

# Convert the pdf file into images, and save in temp file locations
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
    for i in range(1, filelimit + 1):
        filename = "./temp/page_"+str(i)+".jpg"
        print("processing file " + filename)
        text = str(((pytesseract.image_to_string(Image.open(filename), lang='mar+hin', config='--psm 6'))))
        text = text.replace(u'-\n', '')      # remove the blank pages
        text = text.replace(u'\n\n', '\n')   # replace unnecessary repeated newlines
        text = text.replace(u'\n \n', '\n')  # replace unnecessary repeated newlines
        # add a page seperator
        text = text + u"\n============================\n"
        pdf_content += text
    return pdf_content

# Delete temp jpg files from the folder
def delete_jpg(folder_path):
    test = os.listdir(folder_path)
    for images in test:
        if images.endswith('.jpg'):
            os.remove(os.path.join(folder_path, images))

# Prepare the output json file, in the following format
# {
#    'page-url': '',   # specified in the input file (google sheet)
#    'pdf-url': '',    # the redirected URL, for the pdf file
#    'pdf-content': '' # actual pdf content
# }
def create_json(df, temp_df):
    json_list = []
    for index, entry in df.iterrows():
        # print(len(entry))
        json_obj = {'page-url': '', 'pdf-url': '', 'pdf-content': ''}
        url = entry[0]
        if url.endswith('.pdf'):
            page_url = url
            pdf_url = url
            response = requests.get(url)
        else:
            print('processing non pdf url')
            page_url = url
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            url_list = set()
            for a in soup.find_all('a', href=True):
                if a['href'].endswith('.pdf'):
                    base = soup.find('ia-topnav', basehost=True)['basehost']
                    url_list.add(base+a['href'])
            url_list = list(url_list)
            pdf_url = url_list[0]
            print(pdf_url)
            response = requests.get(pdf_url)

        print("writing temp pdf")
        write_file(temp_df, response)

        pdf_content = convert_pdf_to_image()

        json_obj['page-url'] = page_url
        json_obj['pdf-url'] = pdf_url
        json_obj['pdf-content'] = pdf_content
        json_list.append(json_obj)

        delete_jpg(folder_path)

    file_data = json.dumps(json_list, ensure_ascii=False)
    with open('pdf_extract.json', 'w', encoding='utf-8') as outfile:
        outfile.write(file_data)
    outfile.close()

# The main program...
if __name__ == '__main__':
    df = pd.read_csv('https://docs.google.com/spreadsheets/d/1I7hziCQGd0uKzh4RMnZtpkTspaE-1_bIL0FcGU_Y1DU/export?format=csv')
    folder_path = os.getcwd()+'/temp'
    temp_pdf = './temp/temp.pdf'
    create_json(df, temp_pdf)