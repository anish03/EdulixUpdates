from urllib import urlopen
from urllib2 import HTTPError
from BeautifulSoup import BeautifulSoup
import re

base_url = 'http://www.edulix.com/forum/'
updates = []
vars = ['Today','Yesterday']

def start_scraping(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print e
    try:
        soup = BeautifulSoup(html.read())
    except AttributeError as e:
        print e
        return None
    return soup

def get_split(rows,count):
    for item in rows:
        soup = BeautifulSoup(str(item))
        count += 1
        data = soup.find('td',text='Normal Threads')
        if data != None:
            return count

def get_posts(url):
    post_page = urlopen(base_url+url)
    post_soup = BeautifulSoup(post_page)
    title = post_soup.find('title')
    posts = post_soup.findAll('div',{'id':re.compile('^(pid)')})

    counter = 0
    for post in posts:
        if str(post).__contains__('CS') or str(post).__contains__('Computer Science'):
            counter += 1
    if counter > 0:
        print title.text + ': This Thread has Computer Science(CS) Admits/Rejects\n'

def get_updates():
    forums_page = start_scraping(base_url + 'forumdisplay.php?fid=148')
    tables = forums_page.findAll('table')
    rows = BeautifulSoup(str(tables[1])).findAll('tr')

    split_val = get_split(rows,0)

    for row in rows[split_val:-1]:
        soup = BeautifulSoup(str(row))
        latest_post = soup.find('span',{'class':'lastpost smalltext'})
        if str(latest_post).__contains__(vars[0]) or str(latest_post).__contains__(vars[1]):
            updates.append(soup.find('a',{'class':' subject_new'})['href'])

    for update in updates:
        get_posts(update)

if __name__ == '__main__':
    get_updates()
    raw_input('Press Enter to Exit')
