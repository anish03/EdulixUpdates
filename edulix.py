from urllib import urlopen
from urllib2 import HTTPError
from BeautifulSoup import BeautifulSoup

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

def get_updates():
    forums_page = start_scraping(base_url + 'forumdisplay.php?fid=148')
    tables = forums_page.findAll('table')
    rows = BeautifulSoup(str(tables[1])).findAll('tr')

    split_val = get_split(rows,0)

    for row in rows[split_val:-1]:
        soup = BeautifulSoup(str(row))
        latest_post = soup.find('span',{'class':'lastpost smalltext'})
        if str(latest_post).__contains__(vars[0]) or str(latest_post).__contains__(vars[1]):
            updates.append(soup.find('a',{'class':' subject_new'}).text)

    for update in updates:
        print update
        print '\n'

if __name__ == '__main__':
    get_updates()

