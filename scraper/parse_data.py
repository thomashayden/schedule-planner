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

# Merge two dictionary's into one
def merge_two_dicts(d1, d2):
    z = d1.copy()
    z.update(d2)
    return z

# Returns a list of information from the body of the class
def pull_data_from_body(tr):
    rest_cont = tr.td
    data = rest_cont.get_text().encode('ascii', 'ignore').split('\n') # Encode the content, and split it into an array of indiviudal lines
    for i in range(0,len(data)-1): # Loop through the lines of data
        if data[i].isspace(): # If a line of data is a completely blank, remove it
            del data[i]
    while '' in data: # Loop through and remove any completely empty lines
        data.remove('')
    dict_of_info = {}
    for line_number in range(0,len(data)-1):
        dict_of_info = merge_two_dicts(dict_of_info, interpret_data_from_body(line_number, data[line_number])) 
    print(len(dict_of_info)) # Print how many lines of data there is. Only for debugging purposes
    print(dict_of_info) # Also print the data. Also for debugging

def interpret_data_from_body(num,value):
    if num is 0:
        # Always the associated term
        return {value.split(":")[0] : value.split(":").pop(0)}
    elif num is 1:
        # Always the levels
        return {value.split(":")[0] : value.split(":").pop(0)}
    elif num is 2:
        # Always attributes
        return {value.split(":")[0] : value.split(":").pop(0)}
    else:
        # Anything else at the moment
        tmp = {}
        tmp[num] = [value]
        return tmp

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
