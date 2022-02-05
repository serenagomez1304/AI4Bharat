import getopt, sys
from urllib import response
import wikipedia
import json


def wikiExtractor(keyword, num_urls, output):

    # To find wiki pages related to given keywords
    related_pages = wikipedia.search(keyword, results=2*num_urls+1)
    json_list = []
    processed = 0
    for i in range(1, len(related_pages)):
        try:
            json_obj = {'url': '', 'paragraph': ''}

            # From the results find url
            page = wikipedia.page(related_pages[i])
            json_obj['url'] = page.url
        except:
                print('Skipping an amgiguous related page: ', related_pages[i])
                continue
        try:

            # Extract content from the page
            text = page.content

            # Read the paragraph upto the first newline character
            pos = text.find('\n')
            text = text[:pos]
        except AttributeError: 
            text = page.content
        json_obj['paragraph'] = text

        # Update a dictionary with url and first paragraph of the page
        json_list.append(json_obj)

        # Check number of pages processed
        if processed > num_urls:
            break

        processed += 1

    # Save the dictionary in the output json file
    file_data = json.dumps(json_list)
    with open(output, 'w') as outfile:
        outfile.write(file_data)

def usage():
    print("python wiki_extractor.py --keyword='<keyword1 keyword2 keyword3>' --num_urls=<num_urls> --output='<flie.json>'")

if __name__ == '__main__':
    arg_list = sys.argv[1:]
    options = ['keyword =', 'num_urls =', 'output =']
    if len(arg_list) != 3:
        print('Incorrect number of arguments.')
        usage()
        exit(1)
    try: 
        # Parsing argumnents
        args, values = getopt.getopt(args=arg_list, shortopts='kno:', longopts=options)
        # For each argument
        for cur_arg, cur_val in args:
            cur_arg = cur_arg.strip()
            cur_val = cur_val.strip()
            if cur_arg in ("-k", "--keyword"):
                keyword = cur_val
            elif cur_arg in ('-n', '--num_urls'):
                try:
                    num_urls = int(cur_val)
                    if num_urls > 100:
                        print('num_urls must be an integer less than 100.')
                        exit(1)
                except:
                    print('num_urls must be an integer less than 100.')
                    usage()
                    exit(1)
            elif cur_arg in ('-o', '--output'):
                output = cur_val
        wikiExtractor(keyword, num_urls, output)
    except getopt.error as err:
        print(str(err))
        usage()
