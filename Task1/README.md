# Wiki Extractor

This project performs a wikipedia search using a provided keyword, and returns urls of 'n' related Wikipedia pages and a paragraph from each page. The result is returned in the form of a json file.

## Prerequisistes
* Run
    > pip install -r requirements.txt

## How to use
* Run 
    > python wiki_extractor.py --keyword='\<keyword1 keyword2 keyword3\>' --num_urls=\<num_urls\> --output='\<flie.json\>'

## Design details

### Design assumptions
1. Keyword argument is a list of keywords separated by space
2. Maximum number of urls is configured to be 100
3. Skip pages which are considered to be ambiguos for the given keywords

### Implementation approach
Used wikipedia library to:
* To find wiki pages related to given keywords
* From the results find url
* Extract content from the page
* Read the paragraph upto the first newline character
* Update a dictionary with url and first paragraph of the page
* Save the dictionary in the output json file