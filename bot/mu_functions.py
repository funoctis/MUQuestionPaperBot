import requests
from bs4 import BeautifulSoup

def get_page(url):
    """
    Gets the particular webpage to parse.
    """
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, 'lxml')
    return soup


def get_subjects(soup):
    """
    Gets the list of subjects for the semester.  
    """
    tables = soup.find_all('table')
    subject_list = []
    for table in tables:
        subject_list.append(table.find('thead').find('tr').find('th').text)
    return subject_list


def subject_list_to_message(subject_list):
    """
    Converts the list of subjects into a string to send the user.
    """
    message_text = ""
    srno = 0
    for subject in subject_list:
        message_text += "/{srno}. {subject}\n".format(srno = srno, subject = subject)
        srno += 1
    return message_text
        