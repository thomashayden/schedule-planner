# This file is designed to requeest the HTML page, and then parse it maybe. I have to see how everything is going to mesh together, and we might end up with one large file or something. Hopefully not though...

import urllib2

def request_data(url):
    response = urllib2.urlopen(url)
    return response.read()

# Creates the URL to the NEU class search with the correct GET data given the subject
def compile_url(subject):
    url = "https://wl11gp.neu.edu/udcprod8/NEUCLSS.p_class_search?"
    # All of the GET data
    params = [
            "sel_day=dummy",
            "stu_term_in=201830",
            "sel_subj=dummy",
            "sel_attr=dummy",
            "sel_schd=dummy",
            "sel_camp=dummy",
            "sel_insm=dummy",
            "sel_ptrm=dummy",
            "sel_levl=dummy",
            "sel_instr=dummy",
            "sel_seat=dummy",
            "sel_attr=%25",
            "sel_levl=%25",
            "sel_schd=%25",
            "sel_insm=%25",
            "sel_camp=%25",
            "sel_ptrm=%25",
            "sel_instr=%25",
            "begin_hh=0",
            "begin_mi=0",
            "begin_ap=a",
            "end_hh=0",
            "end_mi=0",
            "end_ap=a",
            "sel_crse=",
            "sel_title=",
            "sel_subj=" + subject]

    # Loop through the params list and appened everything to the end of the url as GET data
    for p in params:
        url += (p + "&")

    # Remove the last character, which is a trailing '&'
    url = url[:-1]

    return url

# Returns the HTML of the search result page for the given subject
def get_html_for_subject(subject):
    return request_data(compile_url(subject))

print(get_html_for_subject("ACCT"))
