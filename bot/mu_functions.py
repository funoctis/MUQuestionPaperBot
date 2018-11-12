import requests
from bs4 import BeautifulSoup

def get_page(url):
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, 'lxml')
    return soup


def get_subjects(soup):
    tables = soup.find_all('table')
    subject_list = []
    for table in tables:
        subject_list.append(table.find('thead').find('tr').find('th').text)
    return subject_list


def subject_list_to_message(subject_list):
    message_text = ""
    srno = 0
    for subject in subject_list:
        message_text += "/{srno}. {subject}\n".format(srno = srno, subject = subject)
        srno += 1
    return message_text


def get_links_for_subject(soup, table_no):
    download_links = []
    tables = soup.find_all('table')
    all_links = tables[table_no].find_all('a')
    for link in all_links:
        download_links.append("https://muquestionpapers.com/" + link.get('href'))
    return download_links 
        