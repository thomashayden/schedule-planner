# This file is desgined to parse the HTML data recieved by request_data.py into a form ready to be put into the database

from bs4 import BeautifulSoup
from request_data import get_html_for_subject
import unicodedata

# Returns the raw string of information from the header of the class
def pull_data_from_header(tr):
    return tr.th.a.text

# Parses the header string into individual bits of data
def parse_header_string(hs):
    hs_list = hs.split(' - ')
    # hs_list[0] = Course Name
    # hs_list[1] = CRN
    # hs_list[2] = Course Number
    # hs_list[3] = Number of that Class Amongst other of the Same Class?
    return hs_list

# Returns a list of information from the body of the class
def pull_data_from_body(tr):
    rest_cont = tr.td
    data = rest_cont.get_text().encode('ascii', 'ignore').split('\n')
    for i in range(0,len(data)-1):
        if data[i].isspace():
            del data[i]
    while '' in data:
        data.remove('')
    print(len(data))
    print(data)

bs_html = BeautifulSoup(get_html_for_subject("CS"), 'lxml')

parsed_stuff = bs_html.body
parsed_stuff = parsed_stuff.find('div', attrs={'class' : 'pagebodydiv'})
parsed_stuff = parsed_stuff.table

# Loop through all the <tr> tags, of which two make up each class. The first one is the class name and number, the next one is the actual information. The need to be analyzed in pairs.
temp_storage = None
for tr in parsed_stuff.findAll('tr', recursive=False):
    if temp_storage is None:
        temp_storage = tr
    else:
        print(parse_header_string(pull_data_from_header(temp_storage)))
        print('+++++++++++++++++++++++++++++++++++++++++++++')
        print(pull_data_from_body(tr))
        print('=============================================')
        temp_storage = None



print('done parsing')
