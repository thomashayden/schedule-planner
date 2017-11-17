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
    # These are the markings for where information is. By default everything is -1, which means it isn't there.
    dict_of_info = { assc_term_start : -1,
                     assc_term_end : -1,
                     lvl_start : -1,
                     lvl_end : -1,
                     attr_start : -1,
                     attr_end : -1,
                     instr_start : -1,
                     instr_end : -1,
                     sched_type_start : -1,
                     sched_type_end : -1,
                     instr_method_start : -1,
                     instr_method_end : -1,
                     restr_start : -1,
                     restr_end : -1,
                     preq_start : -1,
                     preq_end : -1,
                     sched_start : -1,
                     sched_end : -1
                     }
    dict_of_info[assc_term_start] = "TEMP"
    print(len(data)) # Print how many lines of data there is. Only for debugging purposes
    print(data) # Also print the data. Also for debugging

# Returns the index of the first found string containing the given string
def search_for_string(str, arr):
    for i in range(0, len(arr)-1):
        if arr[i].contains(str):
            return i
    return -1 # Returns -1 if the string is not found

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
    elif num is 3:
        # Always Instructor(s) (I've only seen a single instructor, so who knows what happens when there are more than one...
        return {value.split(":")[0] : value.split(":").pop(0)}
    elif num is 4:
        # Schedule type
        return {value.split(":")[0] : value.split(":").pop(0)}
    elif num is 5:
        # Instructional method? Just a single value
        return {"Instructional Method" : value}
    elif num is 6:
        print("TEMP")
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
