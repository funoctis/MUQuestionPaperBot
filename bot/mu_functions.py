import requests
from bs4 import BeautifulSoup

def get_subjects(url):
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, 'lxml')
    tables = soup.find_all('table')
    subject_list = []
    for table in tables:
        subject_list.append(table.find('thead').find('tr').find('th').text)
    return subject_list


def subject_list_to_message(subject_list):
    message_text = ""
    srno = 1
    for subject in subject_list:
        message_text += "/{srno}. {subject}\n".format(srno = srno, subject = subject)
        srno += 1
    return message_text